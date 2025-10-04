"""
S&P 500 Company 10-K Analysis Backend
Flask API for analyzing company 10-K HTML documents with keyword tracking and visualization
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from bs4 import BeautifulSoup
import os
import re
import json
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter, defaultdict
from datetime import datetime
import io
import base64
from werkzeug.utils import secure_filename
import zipfile

app = Flask(__name__)

# CORS Configuration - Allow all origins in production (or specify your frontend domain)
CORS(app, resources={r"/*": {"origins": os.getenv('CORS_ORIGINS', '*')}})

# Configuration from environment variables
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
OUTPUT_FOLDER = os.getenv('OUTPUT_FOLDER', 'outputs')
ALLOWED_EXTENSIONS = {'html', 'htm'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 52428800))  # 50MB default
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_html(file_path):
    """Extract text from HTML file using BeautifulSoup"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text
        text = soup.get_text()
        
        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    except Exception as e:
        raise Exception(f"Error extracting text from HTML: {str(e)}")


def get_year_from_filename(filename):
    """Extract year from filename"""
    # Try to find 4-digit year in filename
    match = re.search(r'(20\d{2})', filename)
    if match:
        return match.group(1)
    return None


def count_keywords_in_text(text, keywords_dict):
    """Count occurrences of keywords in text"""
    results = {}
    
    # Convert text to lowercase for case-insensitive matching
    text_lower = text.lower()
    
    for category, terms in keywords_dict.items():
        category_count = 0
        term_counts = {}
        
        for term in terms:
            term_lower = term.lower()
            
            # For multi-word terms
            if ' ' in term_lower:
                count = text_lower.count(term_lower)
            else:
                # For single words, use regex with word boundaries
                pattern = r'\b' + re.escape(term_lower) + r'\b'
                count = len(re.findall(pattern, text_lower))
            
            if count > 0:
                term_counts[term] = count
                category_count += count
        
        results[category] = {
            'total': category_count,
            'terms': term_counts
        }
    
    return results


def create_category_trends_plot(df, company_name):
    """Create line chart showing category trends across years"""
    plt.figure(figsize=(15, 10))
    
    for category in df.index:
        plt.plot(df.columns, df.loc[category], marker='o', linewidth=2, label=category)
    
    plt.title(f'{company_name} Strategic Focus Areas (2020-2024)', fontsize=18)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Mentions in 10-K Report', fontsize=14)
    plt.legend(fontsize=12, loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=0)
    plt.tight_layout()
    
    # Save to BytesIO
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=300)
    img_buffer.seek(0)
    plt.close()
    
    return img_buffer


def create_category_heatmap(df, company_name):
    """Create heatmap showing relative importance of categories by year"""
    plt.figure(figsize=(14, 10))
    
    # Normalize the data for better visualization
    normalized_df = df.div(df.sum(axis=0), axis=1)
    
    sns.heatmap(
        normalized_df, 
        annot=True, 
        cmap='YlGnBu', 
        fmt='.3f',
        linewidths=.5, 
        cbar_kws={'label': 'Relative Focus (% of mentions)'}
    )
    
    plt.title(f'{company_name} Strategic Focus Areas - Relative Importance (2020-2024)', fontsize=18)
    plt.ylabel('Category', fontsize=14)
    plt.xlabel('Year', fontsize=14)
    plt.tight_layout()
    
    # Save to BytesIO
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=300)
    img_buffer.seek(0)
    plt.close()
    
    return img_buffer


def create_top_terms_plot(yearly_keyword_counts, year, company_name, top_n=15):
    """Create bar chart showing top terms for a specific year"""
    # Get all terms and their counts for the year
    all_terms = []
    
    for category, data in yearly_keyword_counts[year].items():
        for term, count in data['terms'].items():
            all_terms.append({
                'term': term, 
                'count': count, 
                'category': category
            })
    
    # Sort by count and get top N
    top_terms = sorted(all_terms, key=lambda x: x['count'], reverse=True)[:top_n]
    
    if not top_terms:
        # Return empty buffer if no terms
        plt.figure(figsize=(12, 8))
        plt.text(0.5, 0.5, 'No keywords found', ha='center', va='center', fontsize=16)
        plt.axis('off')
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        return img_buffer
    
    # Create DataFrame for plotting
    df_top_terms = pd.DataFrame(top_terms)
    
    # Plot
    plt.figure(figsize=(12, 8))
    
    # Create a categorical colormap
    categories = df_top_terms['category'].unique()
    colors = plt.cm.tab10(np.linspace(0, 1, len(categories)))
    category_color = {cat: colors[i] for i, cat in enumerate(categories)}
    
    # Create horizontal bar chart
    bars = plt.barh(
        y=df_top_terms['term'],
        width=df_top_terms['count'],
        color=[category_color[cat] for cat in df_top_terms['category']],
        height=0.6
    )
    
    # Add labels
    plt.title(f'Top {top_n} Keywords in {company_name} 10-K ({year})', fontsize=16)
    plt.xlabel('Number of Mentions', fontsize=14)
    plt.tight_layout()
    
    # Add category labels as legend
    handles = [plt.Rectangle((0,0),1,1, color=category_color[cat]) for cat in category_color]
    plt.legend(handles, category_color.keys(), loc='lower right')
    
    # Adjust y-axis to show most frequent terms at the top
    plt.gca().invert_yaxis()
    
    # Save to BytesIO
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=300)
    img_buffer.seek(0)
    plt.close()
    
    return img_buffer


def create_growth_chart(df, company_name, start_year, end_year):
    """Create growth chart showing changes from start_year to end_year"""
    # Calculate the percentage change, handling division by zero
    growth_pct = pd.Series(index=df.index, dtype=float)
    
    for category in df.index:
        start_val = df.loc[category, start_year]
        end_val = df.loc[category, end_year]
        
        if start_val == 0 and end_val == 0:
            growth_pct[category] = 0
        elif start_val == 0:
            # If starting from zero, show as 100% or use absolute change
            growth_pct[category] = 100  # New category
        else:
            growth_pct[category] = ((end_val - start_val) / start_val * 100)
    
    # Sort from highest growth to lowest
    growth_pct = growth_pct.sort_values(ascending=False)
    
    plt.figure(figsize=(12, 8))
    colors = ['g' if x >= 0 else 'r' for x in growth_pct]
    
    plt.barh(growth_pct.index, growth_pct, color=colors, height=0.6)
    plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    plt.title(f'{company_name} - Change in Strategic Focus Areas ({start_year} to {end_year})', fontsize=16)
    plt.xlabel('Percentage Change (%)', fontsize=14)
    plt.tight_layout()
    
    # Save to BytesIO
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=300)
    img_buffer.seek(0)
    plt.close()
    
    return img_buffer


@app.route('/')
def index():
    """Serve the frontend HTML"""
    return send_file('frontend.html')


@app.route('/api')
def api_info():
    """API information endpoint"""
    return jsonify({
        'message': 'S&P 500 10-K Analysis API',
        'version': '1.0',
        'endpoints': {
            '/': 'GET - Frontend interface',
            '/api': 'GET - API information',
            '/analyze': 'POST - Analyze 10-K documents',
            '/health': 'GET - Health check',
            '/download/<company_name>': 'GET - Download analysis results'
        }
    })


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})


@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Analyze 10-K documents for a company
    
    Expected form data:
    - company_name: str
    - keywords: JSON string (dict of category: [keywords])
    - files: HTML files (year_2020.html, year_2021.html, etc.)
    """
    try:
        # Get company name
        company_name = request.form.get('company_name')
        if not company_name:
            return jsonify({'error': 'Company name is required'}), 400
        
        # Get keywords
        keywords_json = request.form.get('keywords')
        if not keywords_json:
            return jsonify({'error': 'Keywords are required'}), 400
        
        try:
            keywords = json.loads(keywords_json)
        except json.JSONDecodeError:
            return jsonify({'error': 'Invalid keywords JSON format'}), 400
        
        # Get uploaded files
        files = request.files.getlist('files')
        if not files or len(files) == 0:
            return jsonify({'error': 'No files uploaded'}), 400
        
        # Create company-specific output directory
        company_folder = os.path.join(app.config['OUTPUT_FOLDER'], 
                                     secure_filename(company_name.replace(' ', '_')))
        os.makedirs(company_folder, exist_ok=True)
        
        # Process each file
        yearly_texts = {}
        yearly_keyword_counts = {}
        
        for file in files:
            if file and allowed_file(file.filename):
                # Save file temporarily
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                
                # Extract year from filename
                year = get_year_from_filename(filename)
                if not year:
                    # Try to get year from form data for this file
                    year_field = f'year_{filename}'
                    year = request.form.get(year_field)
                
                if year:
                    # Extract text from HTML
                    text = extract_text_from_html(file_path)
                    yearly_texts[year] = text
                    
                    # Count keywords
                    yearly_keyword_counts[year] = count_keywords_in_text(text, keywords)
                
                # Clean up uploaded file
                os.remove(file_path)
        
        if not yearly_texts:
            return jsonify({'error': 'No valid documents processed. Please ensure filenames contain years (e.g., 2020, 2021)'}), 400
        
        # Save raw keyword counts to JSON
        json_path = os.path.join(company_folder, 'keyword_counts.json')
        with open(json_path, 'w') as f:
            json.dump(yearly_keyword_counts, f, indent=4)
        
        # Create DataFrame for category totals
        categories = list(keywords.keys())
        years = sorted(yearly_keyword_counts.keys())
        
        df_categories = pd.DataFrame(index=categories, columns=years)
        
        for year, data in yearly_keyword_counts.items():
            for category, counts in data.items():
                df_categories.loc[category, year] = counts['total']
        
        # Ensure data is numeric
        df_categories = df_categories.astype(float)
        
        # Save category totals CSV
        csv_path = os.path.join(company_folder, 'strategy_analysis.csv')
        df_categories.to_csv(csv_path)
        
        # Create detailed keyword counts CSV
        detailed_rows = []
        for year in years:
            for category in categories:
                category_data = yearly_keyword_counts[year][category]
                # Add row for each keyword with its count
                for keyword, count in category_data['terms'].items():
                    detailed_rows.append({
                        'Year': year,
                        'Category': category,
                        'Keyword': keyword,
                        'Count': count
                    })
        
        df_detailed = pd.DataFrame(detailed_rows)
        detailed_csv_path = os.path.join(company_folder, 'keyword_counts_detailed.csv')
        df_detailed.to_csv(detailed_csv_path, index=False)
        
        # Generate visualizations
        visualizations = {}
        
        # 1. Category trends
        trends_buffer = create_category_trends_plot(df_categories, company_name)
        trends_path = os.path.join(company_folder, 'strategic_trends.png')
        with open(trends_path, 'wb') as f:
            f.write(trends_buffer.getvalue())
        visualizations['trends'] = base64.b64encode(trends_buffer.getvalue()).decode('utf-8')
        
        # 2. Category heatmap
        heatmap_buffer = create_category_heatmap(df_categories, company_name)
        heatmap_path = os.path.join(company_folder, 'strategic_heatmap.png')
        with open(heatmap_path, 'wb') as f:
            f.write(heatmap_buffer.getvalue())
        visualizations['heatmap'] = base64.b64encode(heatmap_buffer.getvalue()).decode('utf-8')
        
        # 3. Top terms for each year
        visualizations['top_terms'] = {}
        for year in years:
            top_terms_buffer = create_top_terms_plot(yearly_keyword_counts, year, company_name)
            top_terms_path = os.path.join(company_folder, f'top_terms_{year}.png')
            with open(top_terms_path, 'wb') as f:
                f.write(top_terms_buffer.getvalue())
            visualizations['top_terms'][year] = base64.b64encode(top_terms_buffer.getvalue()).decode('utf-8')
        
        # 4. Growth chart
        if len(years) >= 2:
            first_year = min(years)
            last_year = max(years)
            growth_buffer = create_growth_chart(df_categories, company_name, first_year, last_year)
            growth_path = os.path.join(company_folder, f'strategic_growth_{first_year}_to_{last_year}.png')
            with open(growth_path, 'wb') as f:
                f.write(growth_buffer.getvalue())
            visualizations['growth'] = base64.b64encode(growth_buffer.getvalue()).decode('utf-8')
        
        # Create summary statistics
        summary = {
            'company_name': company_name,
            'years_analyzed': years,
            'categories_tracked': len(categories),
            'total_keywords': sum(len(terms) for terms in keywords.values()),
            'category_summary': {}
        }
        
        for category in categories:
            summary['category_summary'][category] = {
                'total_mentions': int(df_categories.loc[category].sum()),
                'average_per_year': float(df_categories.loc[category].mean()),
                'trend': 'increasing' if df_categories.loc[category, years[-1]] > df_categories.loc[category, years[0]] else 'decreasing'
            }
        
        # Create a zip file with all outputs
        zip_path = os.path.join(company_folder, f'{company_name.replace(" ", "_")}_analysis.zip')
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(json_path, 'keyword_counts.json')
            zipf.write(csv_path, 'strategy_analysis.csv')
            zipf.write(detailed_csv_path, 'keyword_counts_detailed.csv')
            zipf.write(trends_path, 'strategic_trends.png')
            zipf.write(heatmap_path, 'strategic_heatmap.png')
            for year in years:
                top_terms_path = os.path.join(company_folder, f'top_terms_{year}.png')
                zipf.write(top_terms_path, f'top_terms_{year}.png')
            if len(years) >= 2:
                zipf.write(growth_path, f'strategic_growth_{first_year}_to_{last_year}.png')
        
        return jsonify({
            'success': True,
            'summary': summary,
            'visualizations': visualizations,
            'download_url': f'/download/{secure_filename(company_name.replace(" ", "_"))}'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download/<company_name>')
def download(company_name):
    """Download the analysis results as a zip file"""
    try:
        company_folder = os.path.join(app.config['OUTPUT_FOLDER'], company_name)
        zip_path = os.path.join(company_folder, f'{company_name}_analysis.zip')
        
        if not os.path.exists(zip_path):
            return jsonify({'error': 'Analysis results not found'}), 404
        
        return send_file(zip_path, 
                        as_attachment=True, 
                        download_name=f'{company_name}_analysis.zip',
                        mimetype='application/zip')
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Get port from environment variable (for Heroku/Cloud deployment)
    port = int(os.getenv('PORT', 5001))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    host = os.getenv('HOST', '0.0.0.0')
    
    print("Starting S&P 500 10-K Analysis API...")
    print(f"Server running on http://{host}:{port}")
    print(f"Debug mode: {debug}")
    
    app.run(debug=debug, host=host, port=port)
