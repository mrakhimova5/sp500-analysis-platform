# S&P 500 Company Analysis Platform

Full-stack web application for analyzing S&P 500 company 10-K filings using keyword analysis.

## 🚀 Live Demo

**URL**: https://sp500-analysis.onrender.com

## ✨ Features

- Upload 5 HTML files (10-K filings for consecutive years)
- Keyword frequency analysis across years
- 8 comprehensive visualizations (300 DPI)
- Export results as CSV and JSON
- Download all outputs as ZIP package
- Word-boundary matching for accurate detection

## 📊 Output Files (12 total)

1. `keywords_dictionary.json` - Keywords used in analysis (your input)
2. `keyword_counts.json` - Raw keyword counts by year
3. `strategy_analysis.csv` - Category totals with YoY growth
4. `keyword_counts_detailed.csv` - Individual keyword counts
5-12. PNG visualizations (trends, heatmaps, growth charts, top keywords by year)

## �� Tech Stack

- **Backend**: Flask 3.0.0 REST API
- **Frontend**: HTML/CSS/JavaScript
- **Processing**: BeautifulSoup4, Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn (300 DPI)
- **Deployment**: Render.com (Free Tier)

## 🎯 Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python backend_app.py
```

Visit: http://localhost:5000

### Docker

```bash
docker-compose up
```

## 📝 Usage

1. **Enter company name**
2. **Paste keywords** (Python dictionary format):
   ```python
   {
       "AI & Technology": ["ai", "artificial intelligence", "machine learning"],
       "Cloud": ["cloud computing", "data centers"]
   }
   ```
3. **Upload 5 HTML files** (10-K filings, oldest → newest)
4. **Click "Analyze"**
5. **Download results** (ZIP with 12 files)

## 🌐 API Endpoints

- `GET /` - Frontend interface
- `POST /analyze` - Process 10-K files
- `GET /health` - Health check
- `GET /download/<company>` - Download ZIP

## �� Project Structure

```
sp500-analysis-platform/
├── backend_app.py          # Flask API
├── frontend.html           # Web interface
├── requirements.txt        # Dependencies
├── render.yaml            # Render config
├── docker-compose.yml     # Docker
└── Dockerfile             # Container
```

## 📄 License

MIT
