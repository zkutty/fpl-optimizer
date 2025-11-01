# 🚀 Quick Start Guide

Get your FPL Optimizer web app running in 3 easy steps!

## Step 1: Run the Application

```bash
./run.sh
```

That's it! The script will:
- ✅ Create a virtual environment
- ✅ Install all dependencies
- ✅ Start the web server

## Step 2: Open Your Browser

Navigate to: **http://localhost:5000**

## Step 3: Start Analyzing!

### Option A: Analyze Your Team
1. Enter your **FPL Team ID** on the home page
2. Click "Analyze My Team"
3. View comprehensive analysis across multiple tabs

### Option B: Explore Without Team ID
- **Build Optimal Squad**: Create the perfect team from scratch
- **Value Players**: Find the best points-per-million players

---

## Finding Your FPL Team ID

1. Go to https://fantasy.premierleague.com/
2. Log in to your account
3. Click on "Points" or "Transfers"
4. Look at your browser's address bar
5. Your URL will look like: `https://fantasy.premierleague.com/entry/123456/...`
6. **Your Team ID is: `123456`**

---

## Features You Can Use

### 📊 Dashboard
Get instant insights on:
- Starting XI optimization
- Transfer suggestions
- Captain recommendations
- Chip strategy advice

### 👥 Optimal Squad Builder
- Set your budget (£50m - £100m)
- Choose gameweek horizon (1-10 weeks)
- Get the mathematically optimal team

### ⭐ Value Players
- Filter by position (GK, DEF, MID, FWD)
- See points-per-million rankings
- Find hidden gems

---

## Troubleshooting

### "Port 5000 already in use"
```bash
# Use a different port
PORT=8000 python app.py
```

### "Module not found"
```bash
# Make sure you're in the project directory
cd /Users/zkutlow/fpl-optimizer-1

# Run the setup script again
./run.sh
```

### App is slow
The first analysis takes 10-30 seconds as it:
- Fetches data from FPL API
- Calculates expected points for all players
- Runs optimization algorithms

Subsequent analyses are faster!

---

## Need Help?

- 📖 Full documentation: [WEB_APP_README.md](WEB_APP_README.md)
- 🐛 Issues? Check the troubleshooting section above
- 💡 CLI version: See [README.md](README.md) for command-line usage

---

## Pro Tips

1. **Bookmark with Team ID**: `http://localhost:5000/dashboard?team_id=YOUR_ID`
2. **Compare Options**: Use multiple tabs to compare different strategies
3. **Regular Updates**: Refresh analysis before each gameweek deadline
4. **Check All Tabs**: Don't miss transfers, captain, or chip recommendations

---

## What's Next?

Once the app is running:
1. ✨ Enter your Team ID for personalized analysis
2. 📈 Review transfer suggestions for the upcoming gameweek
3. 👑 Check captain recommendations
4. 🎯 See if any chips should be activated
5. 💪 Dominate your mini-league!

**Good luck!** 🏆

