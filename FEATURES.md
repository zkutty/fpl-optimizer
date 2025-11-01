# Features Documentation

## Core Features

### 1. Team Selection Optimizer

**What it does:**
- Builds the optimal 15-player squad within budget (£100m)
- Meets all FPL constraints (formation, max 3 per team, etc.)
- Maximizes expected points over your chosen time horizon

**Algorithm:**
- Uses Linear Programming (PuLP library)
- Considers expected points based on form, fixtures, and historical data
- Optimizes for multiple gameweeks ahead

**Use cases:**
- Building a team from scratch
- Planning wildcard teams
- Comparing your team to the theoretical optimal

### 2. Transfer Suggester

**What it does:**
- Recommends which players to transfer in/out
- Accounts for transfer costs (4 points per additional transfer)
- Ensures transfers improve expected points
- Respects budget and team constraints

**Features:**
- Single transfer optimization (for regular gameweeks)
- Multiple transfer optimization (for wildcards)
- Wildcard evaluation (compares optimal team vs current)

**Factors considered:**
- Expected points over horizon
- Cost changes
- Team balance (formations, diversity)
- Fixture difficulty

### 3. Lineup Optimizer

**What it does:**
- Selects best starting 11 from your squad of 15
- Ensures valid formation (1 GK, 3-5 DEF, 2-5 MID, 1-3 FWD)
- Maximizes expected points
- Orders bench optimally

**Algorithm:**
- Linear Programming to select best 11
- Considers expected points for next gameweek
- Bench ordered: GK first, then by expected points

### 4. Captain Selector

**What it does:**
- Recommends captain and vice-captain
- Provides differential options (low ownership, high ceiling)
- Shows top 5 captain choices with reasoning

**Metrics considered:**
- **Expected Points**: Base prediction
- **Ceiling**: High upside potential (important for captaincy)
- **Floor**: Consistency baseline
- **Fixture Difficulty**: Opponent strength
- **Ownership**: For differential picks

**Special features:**
- Position-based ceiling calculations (forwards have higher ceiling)
- Form-based adjustments
- Differential picks for mini-league catch-up

### 5. Chip Advisor

**What it does:**
- Recommends when to use each chip
- Prioritizes chips based on gameweek situation
- Provides detailed reasoning for each recommendation

#### Wildcard
**Best used when:**
- Team needs major overhaul (8+ transfers beneficial)
- Expected improvement > 20-30 points over horizon
- Early season (GW 1-10) for team restructure

#### Free Hit
**Best used when:**
- Big double gameweek with few of your players having DGW
- Many players have difficult fixtures (8+ difficult)
- Many blanking players (7+ expected < 2 points)
- Current squad expected points < 35

#### Bench Boost
**Best used when:**
- Double gameweek with 2+ bench players having DGW
- Strong bench (expected > 15 points)
- All 15 players likely to start

#### Triple Captain
**Best used when:**
- Player has double gameweek (2 games)
- Exceptional fixture + in-form premium (difficulty < 2, ceiling > 15)
- Save for best opportunity

### 6. Player Analyzer

**What it does:**
- Calculates expected points for any player
- Identifies best value players (points per million)
- Compares players head-to-head
- Analyzes fixtures difficulty

**Expected Points Formula:**
- 50% recent form (last 5 games)
- 30% season points per game
- 20% FPL's own expected points
- Adjusted for fixture difficulty
- Adjusted for minutes played tendency

**Fixture Difficulty:**
- Uses FPL's official fixture difficulty ratings
- Averages over multiple gameweeks
- Converts to points multiplier (easy fixtures = more points)

### 7. Value Players Finder

**What it does:**
- Identifies best value players by position
- Ranks by points per million
- Filters out injured/unavailable players

**Perfect for:**
- Finding budget enablers
- Identifying breakout players
- Maximizing value in each position

## Technical Details

### Data Sources
- **FPL API**: Official Fantasy Premier League API
- Real-time player data
- Live fixture updates
- Current gameweek information

### Optimization Approach
- **Linear Programming** via PuLP
- Binary variables for player selection
- Constraint satisfaction (budget, formation, team limits)
- Objective: maximize expected points

### Expected Points Calculation
Multi-factor model:
1. **Form** (50%): Recent 5-game performance
2. **Season Average** (30%): Overall points per game
3. **FPL Prediction** (20%): Official expected points
4. **Fixture Adjustment**: Multiplier based on opponent difficulty
5. **Availability**: Minutes played ratio

### Fixture Difficulty Rating
- Scale: 1 (easiest) to 5 (hardest)
- Based on opponent strength
- Home/away considered
- Converted to multiplier: 1.4 - (difficulty × 0.12)

### Constraints Handled
- **Budget**: £100m for full squad
- **Squad Size**: Exactly 15 players
- **Formation**: 2 GK, 5 DEF, 5 MID, 3 FWD
- **Team Limit**: Max 3 players per team
- **Starting XI**: 11 players in valid formation
- **Position Limits**: 1 GK, 3-5 DEF, 2-5 MID, 1-3 FWD

## Limitations & Assumptions

### What the tool does NOT consider:
1. **Bonus Points**: Not fully predictable
2. **Price Changes**: Future rises/falls
3. **Injuries**: Only current status (not predictions)
4. **Rotation Risk**: Only uses past minutes
5. **Player Psychology**: Form, confidence beyond stats
6. **Weather/External Factors**: Not in data

### Assumptions:
- Past performance indicates future results
- Fixture difficulty ratings are accurate
- Players maintain fitness
- Teams maintain strategy
- No inside information

### Recommendations:
- Use as decision support, not absolute truth
- Combine with your own knowledge
- Watch for breaking news (injuries, suspensions)
- Consider context (team news, tactics)
- Trust your instincts alongside the data

## Performance

### Speed:
- Initial data load: 5-15 seconds
- Squad optimization: 1-3 seconds
- Transfer suggestions: 2-5 seconds
- Captain selection: < 1 second
- Chip analysis: 1-2 seconds

### Accuracy:
- Expected points typically within ±30% actual
- Better for consistent players
- More variance for differential picks
- Improves with more gameweeks of data

### Data Freshness:
- Data fetched live from FPL API
- Updated in real-time
- No caching between runs (always fresh)

