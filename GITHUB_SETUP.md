# 📦 GitHub Setup Guide

Before deploying to a hosting platform, you need to push your code to GitHub.

## 🎯 Quick Start

If you haven't already pushed to GitHub, follow these steps:

---

## Step 1: Check Deployment Readiness

Run the deployment check script:

```bash
./deploy_check.sh
```

This will verify all required files are present.

---

## Step 2: Initialize Git (if needed)

```bash
# Check if git is already initialized
git status

# If not, initialize it
git init
```

---

## Step 3: Create Repository on GitHub

1. Go to https://github.com/new
2. Fill in:
   - **Repository name**: `fpl-optimizer`
   - **Description**: "Fantasy Premier League Team Optimizer - Web Application"
   - **Visibility**: Public (or Private)
3. **Don't** initialize with README, .gitignore, or license (we already have these)
4. Click **"Create repository"**

---

## Step 4: Commit Your Code

```bash
# Add all files
git add .

# Commit
git commit -m "Initial commit - FPL Optimizer web app"
```

---

## Step 5: Push to GitHub

GitHub will show you commands after creating the repository. Use these:

```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/fpl-optimizer.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

### If You Use SSH:
```bash
git remote add origin git@github.com:YOUR_USERNAME/fpl-optimizer.git
git push -u origin main
```

---

## Step 6: Verify Upload

1. Go to your repository on GitHub
2. You should see all your files including:
   - `app.py`
   - `templates/` folder
   - `requirements.txt`
   - `Procfile`
   - `render.yaml`
   - etc.

---

## 🔐 Security Checklist

Before pushing, make sure:

- [ ] `.gitignore` is present
- [ ] No `.env` files are included
- [ ] No API keys or secrets in code
- [ ] `venv/` folder is not included

Run this to check:
```bash
git status
```

If you see `venv/` or `.env` files, they shouldn't be there! Check your `.gitignore`.

---

## 🚀 Ready to Deploy!

Once your code is on GitHub, choose a deployment platform:

### Option 1: Render (Easiest)
📖 Follow: [DEPLOY_RENDER.md](DEPLOY_RENDER.md)

### Option 2: Railway
📖 Follow: [DEPLOYMENT.md](DEPLOYMENT.md#railway)

### Option 3: Heroku
📖 Follow: [DEPLOYMENT.md](DEPLOYMENT.md#heroku)

---

## 🔄 Updating Your Deployed App

After deploying, when you make changes:

```bash
# 1. Make your changes
# 2. Test locally
./run.sh

# 3. Commit and push
git add .
git commit -m "Description of changes"
git push origin main

# 4. Your app will auto-redeploy (on Render/Railway)!
```

---

## 🐛 Troubleshooting

### "Permission denied (publickey)"
**Solution**: Set up SSH keys or use HTTPS instead
```bash
# Switch to HTTPS
git remote set-url origin https://github.com/YOUR_USERNAME/fpl-optimizer.git
```

### "Repository not found"
**Solution**: Check the URL and your username
```bash
# Check current remote
git remote -v

# Update if wrong
git remote set-url origin https://github.com/CORRECT_USERNAME/fpl-optimizer.git
```

### "Authentication failed"
**Solution**: Use a personal access token instead of password
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token with `repo` scope
3. Use token as password when pushing

### Files Missing on GitHub
**Solution**: Check if they're in `.gitignore`
```bash
# See what's ignored
git status --ignored
```

---

## 📚 Git Basics Reminder

```bash
# See status
git status

# Add specific file
git add filename.py

# Add all changes
git add .

# Commit with message
git commit -m "Your message"

# Push to GitHub
git push

# Pull latest changes
git pull

# See commit history
git log --oneline
```

---

## 🎯 Next Steps

1. ✅ Push to GitHub (you're here!)
2. 🚀 Deploy to hosting platform
3. 🌐 Access your live app
4. 📱 Share with friends

---

## ✨ All Done!

Once your code is on GitHub, head to [DEPLOY_RENDER.md](DEPLOY_RENDER.md) for the easiest deployment process.

Good luck! 🏆

