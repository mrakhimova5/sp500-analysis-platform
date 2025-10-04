# Heroku Deployment Guide

Complete guide to deploy your S&P 500 Analysis Platform on Heroku with GitHub auto-deploy.

## Prerequisites

- GitHub account
- Heroku account (free tier available)
- Git installed on your computer
- Heroku CLI installed

## Step 1: Install Heroku CLI

### macOS:
```bash
brew tap heroku/brew && brew install heroku
```

### Windows:
Download from: https://devcenter.heroku.com/articles/heroku-cli

### Verify installation:
```bash
heroku --version
```

## Step 2: Prepare Your Repository

### 2.1 Initialize Git (if not already done)
```bash
cd "/Users/malikam/Desktop/python/Google copy"
git init
```

### 2.2 Create .gitignore (already created)
```bash
# Already included in your project
```

### 2.3 Add all files
```bash
git add .
git commit -m "Initial commit - S&P 500 Analysis Platform"
```

### 2.4 Create GitHub Repository
1. Go to https://github.com/new
2. Name it: `sp500-analysis-platform`
3. Don't initialize with README (you already have files)
4. Click "Create repository"

### 2.5 Push to GitHub
```bash
git remote add origin https://github.com/YOUR-USERNAME/sp500-analysis-platform.git
git branch -M main
git push -u origin main
```

## Step 3: Login to Heroku

```bash
heroku login
```

This will open your browser for authentication.

## Step 4: Create Heroku App

### Option A: Via CLI
```bash
heroku create sp500-analysis-app
```

### Option B: Via Dashboard
1. Go to https://dashboard.heroku.com/new-app
2. App name: `sp500-analysis-app` (must be unique)
3. Region: Choose closest to you (United States or Europe)
4. Click "Create app"

## Step 5: Set Environment Variables

### Via CLI:
```bash
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=$(openssl rand -hex 32)
heroku config:set MAX_CONTENT_LENGTH=52428800
heroku config:set DEBUG=False
heroku config:set CORS_ORIGINS=*
```

### Via Dashboard:
1. Go to your app: https://dashboard.heroku.com/apps/sp500-analysis-app
2. Click "Settings" tab
3. Click "Reveal Config Vars"
4. Add each variable:
   - `FLASK_ENV` = `production`
   - `SECRET_KEY` = (generate random string)
   - `MAX_CONTENT_LENGTH` = `52428800`
   - `DEBUG` = `False`
   - `CORS_ORIGINS` = `*`

## Step 6: Connect GitHub for Auto-Deploy

### 6.1 Via Heroku Dashboard (Recommended)
1. Go to your app: https://dashboard.heroku.com/apps/sp500-analysis-app
2. Click "Deploy" tab
3. Under "Deployment method", click "GitHub"
4. Click "Connect to GitHub"
5. Search for: `sp500-analysis-platform`
6. Click "Connect"

### 6.2 Enable Automatic Deploys
1. Scroll to "Automatic deploys"
2. Select branch: `main`
3. Click "Enable Automatic Deploys"
4. ✅ Now every push to GitHub will auto-deploy!

### 6.3 Manual Deploy (First Time)
1. Scroll to "Manual deploy"
2. Select branch: `main`
3. Click "Deploy Branch"
4. Wait for build to complete (~2-3 minutes)

## Step 7: Deploy (if using CLI)

```bash
git push heroku main
```

Watch the deployment logs:
```bash
heroku logs --tail
```

## Step 8: Open Your App

### Via CLI:
```bash
heroku open
```

### Via Browser:
```
https://sp500-analysis-app.herokuapp.com
```

## Step 9: Update Frontend URL

After deployment, update your frontend to use the Heroku URL:

Edit `frontend.html` and change:
```javascript
const API_URL = 'https://sp500-analysis-app.herokuapp.com';
```

Then commit and push:
```bash
git add frontend.html
git commit -m "Update API URL for production"
git push origin main
```

(Auto-deploy will update Heroku automatically!)

## Step 10: Host Frontend

### Option A: Same Heroku App
Your frontend.html is already accessible at:
```
https://sp500-analysis-app.herokuapp.com/frontend.html
```

But you need to add a route. Add this to `backend_app.py`:

```python
@app.route('/frontend')
def frontend():
    return send_file('frontend.html')
```

### Option B: Separate Static Hosting (Recommended)
Deploy frontend to:
- **Netlify**: https://netlify.com (Free)
- **Vercel**: https://vercel.com (Free)
- **GitHub Pages**: https://pages.github.com (Free)

Steps:
1. Create folder: `frontend/`
2. Move `frontend.html` to `frontend/index.html`
3. Update API_URL in the file
4. Deploy to Netlify/Vercel

## Monitoring & Maintenance

### View Logs
```bash
heroku logs --tail
```

### Restart App
```bash
heroku restart
```

### Check App Status
```bash
heroku ps
```

### Open Dashboard
```bash
heroku open
```

### Scale Workers (if needed)
```bash
heroku ps:scale web=1
```

## Troubleshooting

### Issue: Application Error
**Solution:** Check logs
```bash
heroku logs --tail
```

### Issue: Port Binding Error
**Solution:** Make sure you're using `PORT` environment variable:
```python
port = int(os.getenv('PORT', 5001))
```
✅ Already configured in your code!

### Issue: Timeout Errors
**Solution:** Increase timeout in `Procfile`:
```
web: gunicorn backend_app:app --bind 0.0.0.0:$PORT --workers 4 --timeout 300
```
✅ Already set to 300 seconds!

### Issue: Memory Errors
**Solution:** Upgrade dyno:
```bash
heroku ps:resize web=standard-1x
```
Cost: $25/month

### Issue: File Upload Fails
**Solution:** Heroku has ephemeral filesystem. Files are deleted when dyno restarts.
For production, use:
- AWS S3 for file storage
- Cloudinary for images
- Heroku add-on: `heroku addons:create bucketeer`

## Cost Estimation

### Free Tier
- ✅ 550-1000 dyno hours/month (enough for one app 24/7)
- ✅ Apps sleep after 30 min inactivity
- ✅ 30-second startup time after sleep
- ❌ Limited to 512MB RAM

### Hobby Tier ($7/month)
- ✅ No sleeping
- ✅ 512MB RAM
- ✅ Free SSL
- ✅ Custom domains

### Standard Tier ($25-50/month)
- ✅ 1-2GB RAM
- ✅ Horizontal scaling
- ✅ Metrics
- ✅ Better performance

## Future Improvements

### Add Database (Optional)
```bash
heroku addons:create heroku-postgresql:mini
```

### Add Redis Cache (Optional)
```bash
heroku addons:create heroku-redis:mini
```

### Add S3 Storage (For Production)
```bash
heroku addons:create bucketeer:hobbyist
```

### Custom Domain
```bash
heroku domains:add www.yourdomain.com
```

## Auto-Deploy Workflow

Now your workflow is:

1. Make changes locally
2. Test locally: `python3 backend_app.py`
3. Commit: `git commit -am "Your message"`
4. Push: `git push origin main`
5. ✅ Heroku auto-deploys!
6. Check: `heroku logs --tail`

## Success Checklist

- [ ] Heroku CLI installed
- [ ] GitHub repository created
- [ ] Code pushed to GitHub
- [ ] Heroku app created
- [ ] Environment variables set
- [ ] GitHub connected to Heroku
- [ ] Auto-deploy enabled
- [ ] First deployment successful
- [ ] App opens in browser
- [ ] Test analysis works
- [ ] Frontend connects to backend

## Your App URLs

- **Backend API**: https://sp500-analysis-app.herokuapp.com
- **Health Check**: https://sp500-analysis-app.herokuapp.com/health
- **API Docs**: https://sp500-analysis-app.herokuapp.com/

## Need Help?

- Heroku Docs: https://devcenter.heroku.com/
- Heroku Support: https://help.heroku.com/
- Status: https://status.heroku.com/

---

**Deployment Status:** Ready ✅  
**Auto-Deploy:** Enabled 🚀  
**Production:** Ready 🎉
