# How to Run the FPL Optimizer

## ✅ Setup Complete!

Your FPL Optimizer is installed and working at: `/tmp/fpl-optimizer/`

## 🚀 Quick Start

### 1. Activate the Virtual Environment

Every time you want to use the app, first activate the virtual environment:

```bash
cd /tmp/fpl-optimizer
source venv/bin/activate
```

You'll see `(venv)` appear in your terminal prompt.

### 2. Find Your FPL Team ID

- Go to https://fantasy.premierleague.com
- Log in to your account
- Click on "Pick Team" or your team name
- Look at the URL in your browser: `https://fantasy.premierleague.com/entry/123456/`
- The number (123456 in this example) is your Team ID

### 3. Run the Commands

#### Get All Recommendations for Your Team
```bash
python main.py --team-id YOUR_TEAM_ID --all
```
This shows: lineup, transfers, captain, and chips

#### Get Best Value Players
```bash
python main.py --value-players
```

#### Generate Optimal Squad (from scratch)
```bash
python main.py --optimal-squad
```

#### Get Transfer Suggestions
```bash
python main.py --team-id YOUR_TEAM_ID --suggest-transfers
```

#### Get Captain Recommendations
```bash
python main.py --team-id YOUR_TEAM_ID --suggest-captain
```

#### Get Chip Strategy
```bash
python main.py --team-id YOUR_TEAM_ID --suggest-chips
```

#### Get Starting Lineup
```bash
python main.py --team-id YOUR_TEAM_ID --suggest-lineup
```

## 📊 What You'll See

The app will:
1. Fetch live data from the FPL API (takes 5-10 seconds)
2. Analyze all players, fixtures, and form
3. Use mathematical optimization to find the best choices
4. Display clear recommendations with reasoning

## 🎯 Example Output

You'll get detailed info like:
- **Expected Points (EP)**: How many points a player is predicted to score
- **Value**: Points per million spent (higher = better value)
- **Fixture Difficulty**: 1-5 scale (1 = easy, 5 = hard)
- **Reasoning**: Why each recommendation is made

## 💡 Tips

1. **Run before each gameweek deadline** to get fresh data
2. **Use `--all` first** to see everything about your team
3. **Consider the horizon**: Use `--horizon 3` for short-term, `--horizon 10` for long-term
   ```bash
   python main.py --team-id YOUR_ID --suggest-transfers --horizon 3
   ```
4. **Multiple transfers**: For wildcards, specify how many transfers
   ```bash
   python main.py --team-id YOUR_ID --suggest-transfers --num-transfers 5
   ```

## 🔧 Advanced Options

### Optimize for Different Timeframes
```bash
# Short-term (next 3 weeks)
python main.py --optimal-squad --horizon 3

# Long-term (next 10 weeks)
python main.py --optimal-squad --horizon 10
```

### Multiple Transfers
```bash
# Get 3 transfer suggestions (useful during wildcards)
python main.py --team-id YOUR_ID --suggest-transfers --num-transfers 3
```

## ❓ Troubleshooting

### "Could not fetch team data"
- Double-check your team ID is correct
- Make sure your team isn't private (go to FPL settings)

### Virtual environment not activated
If you see errors about missing modules, activate the virtual environment:
```bash
cd /tmp/fpl-optimizer
source venv/bin/activate
```

### Need to reinstall packages
```bash
cd /tmp/fpl-optimizer
source venv/bin/activate
pip install --index-url https://pypi.org/simple/ -r requirements.txt
```

## 📁 Location

Your app is at: `/tmp/fpl-optimizer/`

⚠️ **Note**: The `/tmp` directory is cleared on system restart. If you want to keep this permanently, copy it to another location:

```bash
cp -r /tmp/fpl-optimizer ~/fpl-optimizer
cd ~/fpl-optimizer
```

## 🎓 Learn More

- `README.md` - Project overview
- `QUICK_START.md` - Detailed getting started guide
- `FEATURES.md` - All features explained
- `API_USAGE.md` - Use it in your own Python scripts
- `PROJECT_OVERVIEW.md` - Technical architecture

## 🏆 Enjoy!

You now have a powerful tool to optimize your FPL team with data science and mathematical optimization. Good luck with your mini-leagues! ⚽📊

