# Fantasy Premier League Team Optimizer 🏆⚽

An intelligent FPL team optimizer that helps you make data-driven decisions for your Fantasy Premier League team.

## 🌐 Web Application (NEW!)

This project now includes a **beautiful web interface** for easy access to all features!

### Quick Start - Web App

```bash
./run.sh
```

Then open your browser to `http://localhost:5000`

📖 See [WEB_APP_README.md](WEB_APP_README.md) for detailed web app documentation.

---

## Features

- **Team Selection**: Optimizes your initial team selection within budget constraints
- **Transfer Suggestions**: Recommends the best transfers considering your current team
- **Lineup Optimization**: Suggests the best starting 11 from your squad
- **Captain Selection**: Identifies the best captain and vice-captain choices
- **Chip Strategy**: Advises when to use Wildcard, Free Hit, Bench Boost, and Triple Captain
- **Fixture Analysis**: Considers upcoming fixture difficulty in all recommendations

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Web Interface (Recommended)

```bash
./run.sh
```

Open `http://localhost:5000` in your browser for a beautiful UI with all features.

### Command Line Interface

```bash
# Get optimal team for a new gameweek
python main.py --team-id YOUR_TEAM_ID

# Get all analysis at once
python main.py --team-id YOUR_TEAM_ID --all

# Get transfer suggestions
python main.py --team-id YOUR_TEAM_ID --suggest-transfers

# Get lineup recommendations
python main.py --team-id YOUR_TEAM_ID --suggest-lineup

# Get captain recommendations
python main.py --team-id YOUR_TEAM_ID --suggest-captain

# Get chip recommendations
python main.py --team-id YOUR_TEAM_ID --suggest-chips

# Build optimal squad from scratch
python main.py --optimal-squad

# Find best value players
python main.py --value-players
```

## How It Works

The optimizer uses:
- **Linear Programming**: For team selection and lineup optimization
- **Expected Points**: Based on recent form, fixtures, and historical data
- **Value Analysis**: Points per million to identify the best value players
- **Fixture Difficulty**: Upcoming opponent strength ratings

## Data Source

All data is sourced from the official FPL API.

