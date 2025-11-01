# 🚀 Deploy to Render - Quick Guide

The **fastest and easiest** way to deploy your FPL Optimizer to the web!

## ⏱️ Time Required: ~5 minutes

---

## 📋 Prerequisites

- GitHub account
- Git installed locally
- Your code pushed to GitHub

---

## 🎯 Step-by-Step Instructions

### Step 1: Push to GitHub (if not already done)

```bash
cd /Users/zkutlow/fpl-optimizer-1

# Initialize git if needed
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - FPL Optimizer"

# Create repository on GitHub (https://github.com/new)
# Then push:
git remote add origin https://github.com/YOUR_USERNAME/fpl-optimizer.git
git branch -M main
git push -u origin main
```

### Step 2: Create Render Account

1. Go to **https://render.com**
2. Click **"Get Started"**
3. Sign up with your **GitHub account** (recommended for easier integration)

### Step 3: Create New Web Service

1. Once logged in, click **"New +"** button (top right)
2. Select **"Web Service"**
3. Click **"Connect Account"** if needed to link GitHub
4. Find and select your **`fpl-optimizer`** repository
5. Click **"Connect"**

### Step 4: Configure Service

Fill in these settings:

| Setting | Value |
|---------|-------|
| **Name** | `fpl-optimizer` (or your choice) |
| **Region** | Select closest to you |
| **Branch** | `main` |
| **Root Directory** | Leave empty |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app --bind 0.0.0.0:$PORT` |

### Step 5: Select Plan

- Scroll down to **"Plan"**
- Select **"Free"** (perfect to start!)
- The free plan includes:
  - ✅ 750 hours/month
  - ✅ Auto-sleep after 15 min inactivity
  - ✅ 512 MB RAM
  - ✅ Free SSL certificate

### Step 6: Advanced Settings (Optional)

Click **"Advanced"** to set environment variables:

- Click **"Add Environment Variable"**
- Add:
  - **Key**: `FLASK_ENV`
  - **Value**: `production`

### Step 7: Deploy! 🚀

1. Click **"Create Web Service"** at the bottom
2. Render will now:
   - ✅ Clone your repository
   - ✅ Install dependencies
   - ✅ Start your application
   - ✅ Assign a URL

3. Watch the deployment logs in real-time!

### Step 8: Access Your App

Once deployment completes (2-3 minutes):

1. You'll see **"Live"** status with a green dot
2. Your app URL will be: `https://fpl-optimizer.onrender.com` (or your chosen name)
3. Click the URL to open your app!

---

## 🎉 You're Live!

Your FPL Optimizer is now accessible to anyone on the internet at:

```
https://your-app-name.onrender.com
```

Share this URL with your friends and mini-league competitors!

---

## 🔄 Automatic Updates

**Best Feature**: Render automatically redeploys when you push to GitHub!

```bash
# Make changes to your code
git add .
git commit -m "Added new feature"
git push origin main

# Render automatically detects the push and redeploys!
```

---

## ⚙️ Managing Your App

### View Logs
1. Go to your service dashboard
2. Click **"Logs"** tab
3. See real-time application logs

### Restart Service
1. In dashboard, click **"Manual Deploy"** dropdown
2. Select **"Clear build cache & deploy"**

### Update Environment Variables
1. Go to **"Environment"** tab
2. Add/edit variables
3. Service automatically restarts

---

## 💡 Free Tier Notes

### Sleep Behavior
- App sleeps after **15 minutes** of inactivity
- First request after sleep takes **~30 seconds** to wake up
- Subsequent requests are instant

### Keep It Awake (Optional)
Use a service like **UptimeRobot** (free) to ping your app every 5 minutes:

1. Go to https://uptimerobot.com
2. Create free account
3. Add new monitor:
   - Type: HTTP(s)
   - URL: `https://your-app.onrender.com/health`
   - Interval: 5 minutes

---

## 🌐 Custom Domain (Optional)

Want `fpl.yourdomain.com` instead of `.onrender.com`?

### On Free Tier:
Not available (need paid plan)

### On Paid Tier ($7/month):
1. Go to **"Settings"** → **"Custom Domains"**
2. Click **"Add Custom Domain"**
3. Enter your domain: `fpl.yourdomain.com`
4. Update DNS records at your domain provider:
   - Type: `CNAME`
   - Name: `fpl`
   - Value: `your-app.onrender.com`
5. Wait for DNS propagation (5-30 minutes)
6. Free SSL certificate automatically issued!

---

## 🚀 Upgrade to Paid Plan

If your app becomes popular:

**Starter Plan ($7/month):**
- ✅ No sleep time
- ✅ Custom domains
- ✅ More RAM
- ✅ Faster build times

To upgrade:
1. Go to your service dashboard
2. Click **"Settings"** → **"Plan"**
3. Select **"Starter"**
4. Add payment method

---

## 🐛 Troubleshooting

### Build Failed
- Check logs in Render dashboard
- Verify `requirements.txt` is complete
- Make sure `Procfile` exists in repository

### App Shows Error
- View **"Logs"** tab
- Look for Python errors
- Check environment variables are set

### Can't Access App
- Wait 30 seconds (might be waking from sleep)
- Check if deployment status is "Live"
- Try clearing browser cache

### Changes Not Showing
- Verify you pushed to correct branch
- Check **"Events"** tab for deployment status
- Try manual deploy: **"Manual Deploy"** → **"Deploy latest commit"**

---

## 📊 Monitor Your App

### Built-in Metrics
Render provides:
- Request counts
- Response times
- Error rates
- Memory usage

Access in dashboard under **"Metrics"** tab

### Upgrade Analytics
Paid plans include:
- More detailed metrics
- Longer history
- Custom alerts

---

## 🎯 Next Steps

1. ✅ Share your URL with friends
2. ✅ Monitor logs for any issues
3. ✅ Set up UptimeRobot to prevent sleep
4. ✅ Consider custom domain
5. ✅ Upgrade if you need more performance

---

## 🎓 Additional Resources

- **Render Docs**: https://render.com/docs
- **Flask Deployment**: https://render.com/docs/deploy-flask
- **Render Community**: https://community.render.com

---

## ✨ Success!

**Congratulations!** 🎉

Your FPL Optimizer is now live on the internet and accessible to anyone, anywhere!

```
🌐 Your App: https://your-app-name.onrender.com
📱 Works on: Desktop, tablet, and mobile
🔒 Secure: Free SSL certificate
🚀 Fast: Global CDN
```

Time to dominate your mini-leagues with data-driven decisions! 🏆⚽

