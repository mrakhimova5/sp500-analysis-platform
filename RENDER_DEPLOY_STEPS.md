# 🚀 Deploy to Render - Step by Step

## ✅ Code Ready on GitHub
Repository: `mrakhimova5/sp500-analysis-platform`
Branch: `main`
Latest commit: Migrated to Render.com with free deployment config

---

## 📋 STEP-BY-STEP DEPLOYMENT

### Step 1: Sign Up / Login to Render
1. **Open browser** → Go to: https://dashboard.render.com/
2. **Sign up with GitHub** (recommended) or email
3. Click **"Get Started"** or **"Login"**

### Step 2: Create New Web Service
1. Click **"New +"** button (top right)
2. Select **"Web Service"**

### Step 3: Connect GitHub Repository
1. If first time: Click **"Connect GitHub"**
   - Authorize Render to access your GitHub
2. Find repository: **"sp500-analysis-platform"**
3. Click **"Connect"**

### Step 4: Configure Deployment Settings

Render will auto-detect most settings from `render.yaml`, but verify:

**Basic Settings:**
- **Name:** `sp500-analysis` (or your preferred name)
- **Region:** `Oregon (US West)` ← FREE region
- **Branch:** `main`
- **Runtime:** `Python 3`

**Build & Deploy:**
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn backend_app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 300`

**Instance Type:**
- **Plan:** Select **"FREE"** ⚠️ IMPORTANT!

### Step 5: Add Environment Variables

Click **"Environment"** tab and add these:

```
FLASK_ENV = production
DEBUG = False
MAX_CONTENT_LENGTH = 52428800
CORS_ORIGINS = *
SECRET_KEY = [Click "Generate" to create random key]
```

⚠️ For `SECRET_KEY`: Click the "Generate" button - Render creates a secure random key

### Step 6: Create Web Service

1. Review all settings
2. Click **"Create Web Service"** (bottom)
3. **Wait 3-5 minutes** while Render:
   - Builds your app
   - Installs dependencies
   - Starts the server

### Step 7: Get Your App URL

Once deployment succeeds:
1. You'll see **"Live"** status (green)
2. Your app URL: `https://sp500-analysis.onrender.com`
   - (Or whatever name you chose: `https://YOUR-NAME.onrender.com`)

---

## 🔄 Step 8: Update Frontend URL

Your frontend needs to point to the new Render URL:

1. **Copy your Render URL**: `https://YOUR-APP.onrender.com`

2. **Edit `frontend.html`** - Find this line (around line 27):
```javascript
const API_URL = 'https://p500-analysis-app-762febe7cbc8.herokuapp.com';
```

3. **Change to your Render URL**:
```javascript
const API_URL = 'https://sp500-analysis.onrender.com';  // ← Your new URL
```

4. **Save and push**:
```bash
cd "/Users/malikam/Desktop/python/Google copy"
git add frontend.html
git commit -m "Update API URL to Render"
git push origin main
```

5. **Wait 1-2 minutes** - Render auto-deploys!

---

## ✅ Step 9: Test Your Deployment

1. **Visit your Render URL**: `https://sp500-analysis.onrender.com`
2. **You should see the frontend** with the upload form
3. **Test an analysis**:
   - Enter company name: `Test Company`
   - Paste keywords (example):
   ```python
   {
       "AI & Technology": ["artificial intelligence", "machine learning", "cloud"],
       "Finance": ["revenue", "profit", "investment"]
   }
   ```
   - Upload 5 HTML files
   - Click "Analyze"
   - Download results ZIP

---

## 🎯 Expected Results

**Deployment Time:** 3-5 minutes first time  
**Auto-Deploy:** Yes (on every git push)  
**Cost:** $0/month  
**URL:** https://YOUR-APP.onrender.com  
**SSL:** Free (automatic)  

---

## ⚠️ Important Notes

### Free Tier Limitations:
- ✅ **750 hours/month free** (more than enough)
- ⚠️ **Sleeps after 15 minutes** of inactivity
- ⚠️ **~30 second cold start** when waking up
- ✅ **512MB RAM** (sufficient for your app)
- ✅ **100GB bandwidth/month** (plenty)

### Cold Start Behavior:
- First request after sleep: ~30 seconds
- Subsequent requests: Fast (normal)
- To keep awake: Use UptimeRobot (optional, see DEPLOY_FREE.md)

---

## 📊 Monitoring Your App

**In Render Dashboard:**
- **Logs:** Click "Logs" tab - see real-time application logs
- **Metrics:** View requests, CPU, memory usage
- **Events:** See deployment history
- **Settings:** Change environment variables, rebuild

---

## 🔧 Troubleshooting

### Build Failed?
1. Check "Logs" tab in Render
2. Verify `requirements.txt` has all dependencies
3. Ensure Python 3.9+ compatibility

### App Not Starting?
1. Check logs for errors
2. Verify start command: `gunicorn backend_app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 300`
3. Check environment variables set correctly

### Frontend Not Loading?
1. Clear browser cache
2. Check API_URL in frontend.html matches Render URL
3. Check CORS settings in environment variables

### 502 Bad Gateway?
- App is cold starting (wait 30 seconds)
- Or check logs for startup errors

---

## 🎉 Success Checklist

- [ ] Render account created
- [ ] GitHub repository connected
- [ ] Web service created with FREE plan
- [ ] Environment variables set
- [ ] Deployment shows "Live" (green)
- [ ] App URL accessible in browser
- [ ] Frontend loads correctly
- [ ] API_URL updated in frontend.html
- [ ] Changes pushed to GitHub
- [ ] Auto-deploy working
- [ ] Test analysis completed successfully

---

## 🚀 You're Live!

Once all steps are complete:
- **Your app:** https://sp500-analysis.onrender.com
- **GitHub:** https://github.com/mrakhimova5/sp500-analysis-platform
- **Auto-deploy:** Enabled (every git push)
- **Cost:** $0/month forever

**Share your live app URL in your portfolio!** 🎊

---

## 📞 Need Help?

- **Render Docs:** https://render.com/docs/web-services
- **Render Status:** https://status.render.com/
- **Community:** https://community.render.com/

---

**Ready? Go to: https://dashboard.render.com/** 🚀
