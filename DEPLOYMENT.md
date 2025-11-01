# 🚀 Deployment Guide - FPL Optimizer Web App

This guide covers deploying your FPL Optimizer to various hosting platforms.

## 📋 Table of Contents

1. [Render (Recommended - Easiest)](#render)
2. [Heroku](#heroku)
3. [Railway](#railway)
4. [PythonAnywhere](#pythonanywhere)
5. [AWS / DigitalOcean](#vps-deployment)

---

## 🌟 Render (RECOMMENDED)

**Best for:** Beginners, free tier available, automatic deployments from GitHub

### Step 1: Prepare Your Repository

Make sure all changes are committed and pushed to GitHub:

```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### Step 2: Create Render Account

1. Go to https://render.com
2. Sign up with your GitHub account (easier)

### Step 3: Create New Web Service

1. Click "New +" → "Web Service"
2. Connect your GitHub repository (`fpl-optimizer`)
3. Configure the service:
   - **Name**: `fpl-optimizer` (or your choice)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Select "Free"

### Step 4: Deploy

- Click "Create Web Service"
- Render will automatically deploy your app
- Your app will be live at: `https://fpl-optimizer.onrender.com` (or your chosen name)

### Notes:
- Free tier sleeps after 15 minutes of inactivity (first load takes ~30 seconds)
- Restarts automatically on push to GitHub
- Free SSL certificate included

---

## 🟣 Heroku

**Best for:** Traditional cloud platform, easy CLI tools

### Step 1: Install Heroku CLI

```bash
# macOS
brew install heroku/brew/heroku

# Or download from https://devcenter.heroku.com/articles/heroku-cli
```

### Step 2: Login and Create App

```bash
heroku login
heroku create fpl-optimizer-yourusername
```

### Step 3: Deploy

```bash
git push heroku main
```

### Step 4: Open Your App

```bash
heroku open
```

Your app will be at: `https://fpl-optimizer-yourusername.herokuapp.com`

### Notes:
- Free tier has 550 hours/month (with credit card verification)
- Also sleeps after 30 minutes of inactivity
- Easy to scale if needed

---

## 🚂 Railway

**Best for:** Modern alternative to Heroku, generous free tier

### Step 1: Create Account

1. Go to https://railway.app
2. Sign up with GitHub

### Step 2: Deploy

1. Click "New Project" → "Deploy from GitHub repo"
2. Select your `fpl-optimizer` repository
3. Railway auto-detects it's a Python app
4. Click "Deploy"

### Step 3: Add Domain

1. Go to your project settings
2. Click "Generate Domain"
3. Your app will be at: `https://your-app.up.railway.app`

### Notes:
- $5 free credit per month
- No sleep time (stays active)
- Automatic deployments on GitHub push

---

## 🐍 PythonAnywhere

**Best for:** Python-specific hosting, beginner-friendly

### Step 1: Create Account

1. Go to https://www.pythonanywhere.com
2. Sign up for a free account

### Step 2: Upload Code

Option A - Via GitHub:
```bash
# In PythonAnywhere console
git clone https://github.com/yourusername/fpl-optimizer.git
cd fpl-optimizer
pip install --user -r requirements.txt
```

Option B - Upload files directly via web interface

### Step 3: Configure Web App

1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Flask"
4. Set Python version: 3.10
5. Set:
   - Source code: `/home/yourusername/fpl-optimizer`
   - Working directory: `/home/yourusername/fpl-optimizer`
   - WSGI file: Point to `app.py`

### Step 4: Reload and Visit

- Click "Reload" button
- Visit: `https://yourusername.pythonanywhere.com`

### Notes:
- Free tier: one web app
- Slower than other options
- No custom domain on free tier

---

## 🖥️ VPS Deployment (AWS, DigitalOcean, Linode)

**Best for:** Full control, production deployments

### Option 1: Using Nginx + Gunicorn (Ubuntu)

```bash
# 1. Connect to your server
ssh user@your-server-ip

# 2. Install dependencies
sudo apt update
sudo apt install python3-pip python3-venv nginx

# 3. Clone and setup
git clone https://github.com/yourusername/fpl-optimizer.git
cd fpl-optimizer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# 4. Create systemd service
sudo nano /etc/systemd/system/fpl-optimizer.service
```

Add this configuration:

```ini
[Unit]
Description=FPL Optimizer Web App
After=network.target

[Service]
User=yourusername
WorkingDirectory=/home/yourusername/fpl-optimizer
Environment="PATH=/home/yourusername/fpl-optimizer/venv/bin"
ExecStart=/home/yourusername/fpl-optimizer/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
```

```bash
# 5. Configure Nginx
sudo nano /etc/nginx/sites-available/fpl-optimizer
```

Add:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# 6. Enable and start
sudo ln -s /etc/nginx/sites-available/fpl-optimizer /etc/nginx/sites-enabled
sudo systemctl start fpl-optimizer
sudo systemctl enable fpl-optimizer
sudo systemctl restart nginx
```

### Option 2: Using Docker

See `DEPLOYMENT_DOCKER.md` for containerized deployment.

---

## 🔒 Environment Variables

For production, set these environment variables on your hosting platform:

```bash
SECRET_KEY=your-random-secret-key-here
FLASK_ENV=production
```

Generate a secret key:
```python
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 🌐 Custom Domain

### For Render:
1. Go to Settings → Custom Domains
2. Add your domain
3. Update DNS records as shown

### For Heroku:
```bash
heroku domains:add www.yourdomain.com
```

### For Railway:
1. Go to Settings → Domains
2. Add custom domain
3. Update DNS

---

## 📊 Monitoring & Logs

### Render:
- View logs in dashboard under "Logs" tab

### Heroku:
```bash
heroku logs --tail
```

### Railway:
- View logs in project dashboard

---

## ⚡ Performance Tips

1. **Enable Caching**: Add Redis for caching FPL API responses
2. **Use CDN**: For static files (if you add any)
3. **Upgrade Plan**: If you get popular, upgrade to paid tier
4. **Add Database**: For user accounts/saved teams (future feature)

---

## 🔧 Troubleshooting

### App Won't Start
- Check logs for errors
- Verify `requirements.txt` is complete
- Ensure `Procfile` exists (for Heroku/Render)

### Slow First Load
- Free tiers sleep - consider paid tier or keep-alive service
- Use UptimeRobot to ping your app every 5 minutes

### API Errors
- Check FPL API is accessible from your server
- Verify no IP blocking

---

## 📞 Need Help?

- **Render Support**: https://render.com/docs
- **Heroku Support**: https://devcenter.heroku.com
- **Railway Support**: https://docs.railway.app

---

## 🎯 Recommended Path

**For Beginners:**
1. Start with **Render** (easiest, free, auto-deploy)
2. Push to GitHub
3. Connect to Render
4. Deploy in 5 minutes!

**For Production:**
1. Use **Railway** or **Render** paid tier
2. Add custom domain
3. Enable monitoring
4. Set up backups

---

## ✅ Post-Deployment Checklist

- [ ] App loads successfully
- [ ] Can enter team ID and get analysis
- [ ] All tabs work (lineup, transfers, captain, chips)
- [ ] Value players page loads
- [ ] Optimal squad builder works
- [ ] Set up custom domain (optional)
- [ ] Enable HTTPS (automatic on most platforms)
- [ ] Monitor logs for errors
- [ ] Share with friends! 🎉

