# Quick Start Guide

## Installation

1. **Install dependencies:**
```bash
cd /tmp/fpl-optimizer
pip install -r requirements.txt
```

## Finding Your Team ID

Your FPL Team ID can be found in the URL when you're logged into your team:
- Go to https://fantasy.premierleague.com
- Click on your team
- Look at the URL: `https://fantasy.premierleague.com/entry/YOUR_TEAM_ID/`
- The number in the URL is your Team ID

## Basic Usage

### 1. Analyze Your Current Team (Recommended First Step)

```bash
python main.py --team-id YOUR_TEAM_ID --all
```

This will show you:
- Optimal starting lineup from your current squad
- Transfer suggestions
- Captain recommendations
- Chip usage advice

### 2. Get Transfer Suggestions

```bash
# Single transfer
python main.py --team-id YOUR_TEAM_ID --suggest-transfers

# Multiple transfers (e.g., for wildcard)
python main.py --team-id YOUR_TEAM_ID --suggest-transfers --num-transfers 3
```

### 3. Get Captain Recommendations

```bash
python main.py --team-id YOUR_TEAM_ID --suggest-captain
```

### 4. Get Chip Recommendations

```bash
python main.py --team-id YOUR_TEAM_ID --suggest-chips
```

This tells you when to use:
- Wildcard
- Free Hit
- Bench Boost
- Triple Captain

### 5. Build an Optimal Squad from Scratch

```bash
python main.py --optimal-squad
```

### 6. Find Best Value Players

```bash
python main.py --value-players
```

## Advanced Options

### Optimize for Different Time Horizons

```bash
# Optimize for next 3 gameweeks (short-term)
python main.py --team-id YOUR_TEAM_ID --suggest-transfers --horizon 3

# Optimize for next 10 gameweeks (long-term)
python main.py --team-id YOUR_TEAM_ID --suggest-transfers --horizon 10
```

## Example Workflow

### Before Each Gameweek:

1. **Check your lineup:**
   ```bash
   python main.py --team-id YOUR_TEAM_ID --suggest-lineup
   ```

2. **Choose your captain:**
   ```bash
   python main.py --team-id YOUR_TEAM_ID --suggest-captain
   ```

3. **Consider transfers:**
   ```bash
   python main.py --team-id YOUR_TEAM_ID --suggest-transfers
   ```

4. **Check chip strategy:**
   ```bash
   python main.py --team-id YOUR_TEAM_ID --suggest-chips
   ```

### During Wildcards:

```bash
# Get the optimal squad within your budget
python main.py --optimal-squad --horizon 10

# Or get multiple transfer suggestions
python main.py --team-id YOUR_TEAM_ID --suggest-transfers --num-transfers 10
```

## Understanding the Output

### Expected Points (EP)
The number of points a player is expected to score over the optimization horizon.

### Value
Points per million (EP / Cost). Higher is better.

### Fixture Difficulty
Scale of 1-5:
- 1-2: Easy fixtures (good time to captain/transfer in)
- 3: Neutral
- 4-5: Hard fixtures (avoid captaining/consider transferring out)

### Ceiling
The high upside potential. Useful for captain picks - you want high ceiling players.

### Floor
The consistent baseline. Useful for reliable players who won't blank.

## Tips

1. **Run before each gameweek** to get the latest data
2. **Consider the horizon** - use shorter horizons (3-5 weeks) for regular transfers
3. **Don't always follow exactly** - the tool provides data-driven suggestions, but trust your instincts too
4. **Check differential captains** for mini-leagues where you need to make up ground
5. **Save chips for big occasions** - especially Double Gameweeks

## Troubleshooting

### "Could not fetch team data"
- Check your team ID is correct
- Make sure your team is not set to private
- Ensure you have internet connection

### "Module not found" errors
- Run: `pip install -r requirements.txt`

### Slow performance
- First run downloads data from FPL API and can take 10-30 seconds
- Subsequent operations are faster

## Examples

Run the examples file to see it in action:
```bash
python example_usage.py
```

