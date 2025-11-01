# Fantasy Premier League Team Optimizer - Project Overview

## 🎯 What This App Does

This is a comprehensive Fantasy Premier League (FPL) team optimizer that helps you make data-driven decisions to improve your FPL performance. It analyzes player data, fixtures, form, and uses mathematical optimization to suggest:

- **Optimal team selection** from all available players
- **Transfer recommendations** to improve your team
- **Starting lineup selection** from your 15-player squad
- **Captain and vice-captain choices** with differential options
- **Chip usage strategy** (Wildcard, Free Hit, Bench Boost, Triple Captain)
- **Value players** to maximize points per million spent

## 📁 Project Structure

```
fpl-optimizer/
├── README.md              # Main documentation
├── QUICK_START.md         # Quick start guide
├── FEATURES.md            # Detailed feature documentation
├── API_USAGE.md           # Programmatic API usage guide
├── PROJECT_OVERVIEW.md    # This file
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore file
│
├── main.py               # Main CLI application
├── example_usage.py      # Usage examples
│
├── fpl_api.py           # FPL API client
├── player_analyzer.py    # Player analysis and expected points
├── team_optimizer.py     # Squad and lineup optimization
├── transfer_suggester.py # Transfer recommendations
├── captain_selector.py   # Captain recommendations
└── chip_advisor.py       # Chip usage recommendations
```

## 🧩 Core Components

### 1. FPL API Client (`fpl_api.py`)
- Connects to official FPL API
- Fetches player data, fixtures, teams, gameweek info
- Retrieves user team data
- Caches data to minimize API calls

### 2. Player Analyzer (`player_analyzer.py`)
- Calculates expected points for each player
- Considers form, fixtures, minutes played
- Identifies best value players
- Compares players head-to-head
- Weights multiple factors:
  - 50% recent form
  - 30% season average
  - 20% FPL's expected points
  - Adjusted for fixture difficulty

### 3. Team Optimizer (`team_optimizer.py`)
- Uses Linear Programming (PuLP) for optimization
- Optimizes squad selection (15 players)
- Optimizes starting XI (11 players)
- Respects all FPL constraints:
  - £100m budget
  - Formation requirements (2-5-5-3)
  - Max 3 players per team
  - Valid starting formations

### 4. Transfer Suggester (`transfer_suggester.py`)
- Recommends optimal transfers
- Single or multiple transfers
- Accounts for transfer costs (4 points each)
- Evaluates wildcard usage
- Ensures budget and team constraints

### 5. Captain Selector (`captain_selector.py`)
- Suggests captain and vice-captain
- Calculates ceiling (high upside) and floor (consistency)
- Provides differential options for mini-leagues
- Evaluates Triple Captain chip usage
- Considers fixtures and form

### 6. Chip Advisor (`chip_advisor.py`)
- Comprehensive chip strategy
- Wildcard: When to restructure team
- Free Hit: For difficult gameweeks/DGWs
- Bench Boost: When bench is strong
- Triple Captain: Best opportunities
- Prioritizes chips based on situation

## 🔬 Optimization Approach

### Linear Programming
The app uses Linear Programming (LP) to solve optimization problems:

**Variables:** Binary (0 or 1) for each player (selected or not)

**Objective:** Maximize total expected points

**Constraints:**
- Budget ≤ £100m
- Exactly 15 players (squad) or 11 players (lineup)
- Position requirements met
- Max 3 players per team

**Solver:** PuLP with CBC (Coin-or branch and cut) solver

### Expected Points Model
Multi-factor predictive model:

```
EP = (Form × 0.5 + PPG × 0.3 + FPL_EP × 0.2) 
     × FixtureDifficultyMultiplier 
     × AvailabilityFactor
     × NumGameweeks
```

Where:
- **Form**: Last 5 games average
- **PPG**: Points per game this season  
- **FPL_EP**: FPL's own expected points
- **Fixture Multiplier**: 1.4 - (difficulty × 0.12)
- **Availability**: Minutes played / possible minutes

## 📊 Data Flow

```
1. FPL API
   ↓
2. Data Fetching (fpl_api.py)
   ↓
3. Data Processing (player_analyzer.py)
   ↓
4. Analysis & Calculation
   ├── Expected Points
   ├── Fixture Difficulty
   └── Value Metrics
   ↓
5. Optimization
   ├── Squad Selection (team_optimizer.py)
   ├── Transfers (transfer_suggester.py)
   ├── Captain (captain_selector.py)
   └── Chips (chip_advisor.py)
   ↓
6. Output
   ├── CLI (main.py)
   └── Programmatic API
```

## 🎮 Usage Modes

### 1. Command Line Interface (CLI)
```bash
# Analyze your team
python main.py --team-id YOUR_ID --all

# Get transfers
python main.py --team-id YOUR_ID --suggest-transfers

# Get optimal squad
python main.py --optimal-squad
```

### 2. Interactive Python
```python
from fpl_api import FPLApi
from player_analyzer import PlayerAnalyzer

api = FPLApi()
analyzer = PlayerAnalyzer(api)
analyzer.load_data()

# Your custom analysis
```

### 3. Web Integration
Can be integrated into Flask/Django apps to provide web interface

## 🔑 Key Algorithms

### 1. Squad Optimization
```
Maximize: Σ(player_i × expected_points_i)
Subject to:
  - Σ(player_i) = 15
  - Σ(player_i × cost_i) ≤ 1000
  - Σ(player_i where position=GK) = 2
  - Σ(player_i where position=DEF) = 5
  - Σ(player_i where position=MID) = 5
  - Σ(player_i where position=FWD) = 3
  - Σ(player_i where team=t) ≤ 3, for all teams t
```

### 2. Starting XI Optimization
```
Maximize: Σ(starter_i × expected_points_i)
Subject to:
  - Σ(starter_i) = 11
  - Σ(starter_i where position=GK) = 1
  - 3 ≤ Σ(starter_i where position=DEF) ≤ 5
  - 2 ≤ Σ(starter_i where position=MID) ≤ 5
  - 1 ≤ Σ(starter_i where position=FWD) ≤ 3
  - starter_i ∈ current_squad
```

### 3. Transfer Optimization
For single transfer:
```
Find: (out_player, in_player)
Maximize: EP(in_player) - EP(out_player) - transfer_cost
Subject to:
  - Same position
  - Budget constraint
  - Team constraint (max 3)
```

For multiple transfers: Greedy approach iteratively finding best transfer

## 🎯 Use Cases

### Weekly Management
1. Check lineup before deadline
2. Choose captain based on fixtures
3. Make informed transfer decisions

### Strategic Planning
1. Wildcard planning (complete team overhaul)
2. Chip strategy (when to use which chip)
3. Long-term fixtures analysis

### Value Hunting
1. Find budget enablers
2. Identify breakout players
3. Maximize points per million

### Mini-League Strategy
1. Template team comparison
2. Differential picks for catching up
3. Ownership-based captain choices

## 📈 Performance Characteristics

### Accuracy
- Expected points typically ±30% of actual
- Better for consistent players
- More variance for differentials
- Improves as season progresses

### Speed
- Data loading: 5-15 seconds (API call)
- Optimization: 1-5 seconds per analysis
- Total analysis: 10-30 seconds

### Data Freshness
- Live data from FPL API
- Updated in real-time
- No stale data (no persistent cache)

## 🔧 Technical Stack

### Languages & Libraries
- **Python 3.7+**: Core language
- **pandas**: Data manipulation
- **numpy**: Numerical operations
- **PuLP**: Linear programming
- **requests**: API calls
- **scipy**: Statistical operations

### APIs
- **FPL API**: Official Fantasy Premier League API
  - Bootstrap data: Players, teams, gameweeks
  - Fixtures: Match schedules and difficulty
  - User data: Team picks and history

## 🚀 Getting Started

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Find your team ID:**
   - Visit fantasy.premierleague.com
   - URL shows: `/entry/YOUR_TEAM_ID/`

3. **Run analysis:**
   ```bash
   python main.py --team-id YOUR_TEAM_ID --all
   ```

4. **See examples:**
   ```bash
   python example_usage.py
   ```

## 📚 Documentation Files

- **README.md**: Overview and installation
- **QUICK_START.md**: Getting started quickly
- **FEATURES.md**: Detailed feature documentation
- **API_USAGE.md**: Programmatic usage guide
- **PROJECT_OVERVIEW.md**: This file (architecture)

## 🎓 Educational Value

This project demonstrates:
- **Optimization**: Linear programming for constrained optimization
- **Data Science**: Predictive modeling with multiple factors
- **API Integration**: Working with external APIs
- **Software Architecture**: Modular, maintainable code design
- **Domain Modeling**: Representing FPL rules as constraints

## 🔮 Future Enhancements (Ideas)

- Machine learning models for predictions
- Historical performance tracking
- Auto-filling team changes
- Web dashboard interface
- Price change predictions
- Injury news integration
- Twitter sentiment analysis
- Mini-league tracking and comparison
- Mobile app
- Automated team updates

## 📝 License & Usage

This is a personal tool for FPL analysis. Use responsibly:
- Don't spam the FPL API
- Data is for personal use
- No guarantees on accuracy
- Use as decision support, not absolute truth

## 🤝 Contributing

If extending this project:
1. Maintain modular structure
2. Add tests for new features
3. Update documentation
4. Follow existing code style
5. Add examples for new features

## 🏆 Philosophy

**Data-Driven Decisions:** Use statistics and optimization to inform choices

**Transparency:** Show reasoning behind recommendations

**Flexibility:** Allow customization of time horizons and constraints

**Simplicity:** Make complex analysis accessible

**Realism:** Acknowledge limitations and uncertainties

---

Built for FPL managers who want to combine data science with football passion! 🎯⚽📊

