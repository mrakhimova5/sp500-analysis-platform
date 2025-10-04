# S&P 500 Company 10-K Analysis Platform

Professional platform for analyzing S&P 500 company 10-K reports using custom keyword tracking and visualization.

## Features

✅ **Flexible Keyword Analysis** - Paste your own Python dictionary of keywords  
✅ **Multi-Year Tracking** - Analyze 5 years of data (2020-2024)  
✅ **Professional Visualizations** - 300 DPI charts ready for presentations  
✅ **Detailed Reports** - JSON, CSV, and PNG outputs  
✅ **Word-Boundary Matching** - Accurate keyword detection (e.g., "ai" won't match "said")  

## Quick Start

### 1. Install Dependencies

```bash
pip install -r backend_requirements.txt
```

### 2. Start Backend

```bash
./start_backend.sh
```

Or manually:
```bash
python3 backend_app.py
```

The backend will run on **http://localhost:5001**

### 3. Open Frontend

```bash
open frontend.html
```

Or double-click `frontend.html` in Finder.

## Usage

### Step 1: Enter Company Name
Example: `Apple Inc.`, `Microsoft Corporation`, `3M Company`

### Step 2: Paste Keywords Dictionary

Use this format:
```python
categories = {
    "ai_ml": [
        "artificial intelligence", "machine learning", "deep learning"
    ],
    "cloud_computing": [
        "cloud", "cloud services", "AWS", "Azure", "data center"
    ],
    "cybersecurity": [
        "cybersecurity", "data privacy", "encryption", "security"
    ]
}
```

### Step 3: Upload HTML Files

Upload 5 HTML files (10-K reports for 2020-2024). 

**Important:** Filenames must contain the year (e.g., `apple_2020.html`, `10k_2021.html`)

### Step 4: Analyze

Click **"🚀 Analyze Documents"** and wait for processing (usually 1-2 minutes).

### Step 5: Download Results

Click **"📥 Download Complete Analysis"** to get a ZIP file with all outputs.

## Output Files

Your analysis includes **11 files**:

### Data Files
1. **keyword_counts.json** - Raw keyword counts in JSON format
2. **strategy_analysis.csv** - Category totals by year
3. **keyword_counts_detailed.csv** - Individual keyword counts for every term

### Visualizations (300 DPI)
4. **strategic_trends.png** - Multi-line chart showing trends across categories
5. **strategic_heatmap.png** - Heatmap of category focus over time
6. **top_terms_2020.png** - Top 15 keywords in 2020
7. **top_terms_2021.png** - Top 15 keywords in 2021
8. **top_terms_2022.png** - Top 15 keywords in 2022
9. **top_terms_2023.png** - Top 15 keywords in 2023
10. **top_terms_2024.png** - Top 15 keywords in 2024
11. **strategic_growth_2020_to_2024.png** - Year-over-year growth chart

## Technical Details

### Word Boundary Matching
Keywords use regex word boundaries (`\b`), so:
- ✅ "ai" matches "AI", "ai", "A.I."
- ❌ "ai" does NOT match "said", "email", "train"

### Year-over-Year Growth
- Calculates percentage change: `((end - start) / start) × 100`
- Handles zero values: If start = 0 and end > 0, shows 100% growth
- Color-coded: Green for growth, Red for decline

### Top 15 Keywords
Shows top 15 keywords **across all categories** (not per category), sorted by total mentions.

### CSV Outputs

**strategy_analysis.csv** (Category totals):
```csv
,2020,2021,2022,2023,2024
ai_ml,15.0,23.0,34.0,45.0,67.0
cloud_computing,89.0,102.0,156.0,178.0,201.0
```

**keyword_counts_detailed.csv** (Individual keywords):
```csv
Year,Category,Keyword,Count
2020,ai_ml,artificial intelligence,8
2020,ai_ml,machine learning,7
2020,cloud_computing,AWS,45
```

## Requirements

- **Python 3.8+**
- **Flask 3.0.0**
- **BeautifulSoup4 4.12.2**
- **Pandas 2.1.3**
- **Matplotlib 3.8.2**
- **Seaborn 0.13.0**

See `backend_requirements.txt` for complete list.

## File Structure

```
.
├── backend_app.py              # Flask API server
├── frontend.html               # Web interface
├── backend_requirements.txt    # Python dependencies
├── start_backend.sh           # Startup script
├── README.md                  # This file
├── outputs/                   # Analysis results (auto-created)
└── uploads/                   # Temporary file storage (auto-created)
```

## Tips

### Getting 10-K HTML Files
1. Go to SEC EDGAR: https://www.sec.gov/edgar/searchedgar/companysearch.html
2. Search for your company
3. Find 10-K filings for each year
4. Click on the filing, then the document link
5. Right-click → "Save As" → Save as HTML

### Creating Keyword Lists
- Use industry-specific terminology
- Include variations: "AI", "artificial intelligence", "A.I."
- Use both acronyms and full terms: "ML", "machine learning"
- Include multi-word phrases: "cloud computing", "data privacy"
- Test with small lists first, then expand

### Performance
- Processing time: ~30 seconds per file
- 5 files take ~2-3 minutes total
- Large files (>10MB) may take longer

## Troubleshooting

**"Error connecting to server"**
- Make sure backend is running: `python3 backend_app.py`
- Check that port 5001 is not in use
- Refresh the browser page

**"No valid documents processed"**
- Ensure filenames contain years (2020-2024)
- Check files are HTML format (.html or .htm)
- Verify files uploaded correctly

**"Invalid dictionary format"**
- Use Python dictionary syntax: `{"category": ["keyword1", "keyword2"]}`
- Make sure to use double quotes or single quotes consistently
- Check for missing commas or brackets

## License

MIT License - Free to use for academic and commercial purposes.

## Support

For issues or questions, check that:
1. Backend is running on port 5001
2. Files are in HTML format with years in filenames
3. Keywords dictionary is valid JSON/Python format

---

**Version:** 1.0  
**Last Updated:** October 3, 2025  
**Status:** Production Ready ✅
