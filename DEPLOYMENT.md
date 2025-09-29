# 🚀 Streamlit Cloud Deployment Guide

## Quick Setup for Streamlit Cloud

### 1. **Push to GitHub**
```bash
# Initialize git repository
git init
git add .
git commit -m "Initial commit: Crypto Bull/Bear Dashboard"

# Add your GitHub remote
git remote add origin https://github.com/yourusername/crypto-bullbear-dashboard
git push -u origin main
```

### 2. **Deploy to Streamlit Cloud**
1. Go to **https://share.streamlit.io/**
2. Click **"New app"**
3. Connect your GitHub repository
4. Set main file path: `app.py`
5. Click **"Deploy"**

### 3. **Add Your API Key** (Important!)
1. In Streamlit Cloud, go to **App settings** → **Secrets**
2. Add this content:
```toml
COINGECKO_API_KEY = "CG-t6UpP9dK7Ek1JCgaswnWrigo"
```

### 4. **Files to Upload to GitHub**
✅ Upload these files:
- `app.py` (main Streamlit app)
- `coingecko_api.py` (API integration)
- `trend_analyzer.py` (EMA analysis)
- `chart_visualizer.py` (charts)
- `requirements.txt` (dependencies)
- `README.md` (documentation)

❌ Don't upload these (already in .gitignore):
- `.env` (contains your API key)
- `test_app.py`
- `simple_dashboard.py`
- `web_dashboard.py`

## Why This Works
- ✅ **Streamlit Cloud** has proper SSL certificates
- ✅ **No Windows Store Python issues**
- ✅ **Professional hosting** with automatic updates
- ✅ **Secrets management** for API keys
- ✅ **Custom URLs** like `yourapp.streamlit.app`

## Your Dashboard Features
- 📊 **Bitcoin, Ethereum, Solana** trend analysis
- 📈 **EMA 12/21 crossover** bull/bear signals
- ⏰ **Multiple timeframes** (4H to 1W)
- 🔄 **Auto-refresh** every 30 seconds
- 📱 **Mobile responsive** design
- 🎯 **Interactive charts** with crossover markers