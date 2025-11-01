# Programmatic API Usage

If you want to integrate the FPL Optimizer into your own Python scripts or applications, here's how to use it programmatically.

## Basic Setup

```python
from fpl_api import FPLApi
from player_analyzer import PlayerAnalyzer
from team_optimizer import TeamOptimizer
from transfer_suggester import TransferSuggester
from captain_selector import CaptainSelector
from chip_advisor import ChipAdvisor

# Initialize
api = FPLApi()
analyzer = PlayerAnalyzer(api)
analyzer.load_data()

# Create other components
optimizer = TeamOptimizer(api, analyzer)
transfer_suggester = TransferSuggester(api, analyzer, optimizer)
captain_selector = CaptainSelector(api, analyzer)
chip_advisor = ChipAdvisor(api, analyzer, transfer_suggester, captain_selector)
```

## Examples

### 1. Get Player Data

```python
# Get all players
players = api.get_players()
print(f"Total players: {len(players)}")

# Get player by ID
player_id = 354  # Example: Haaland
player_details = api.get_player_details(player_id)
print(player_details)

# Get current gameweek
current_gw = api.get_current_gameweek()
print(f"Current gameweek: {current_gw}")
```

### 2. Analyze Individual Players

```python
# Get player score
player_id = 354
score = analyzer.get_player_score(player_id, horizon=5)

print(f"Player: {score['name']}")
print(f"Team: {score['team']}")
print(f"Cost: £{score['cost']}m")
print(f"Expected Points (5 GWs): {score['expected_points']:.1f}")
print(f"Value: {score['value']:.2f}")

# Compare two players
comparison = analyzer.compare_players(354, 355)
better_player = comparison['better_player']
print(f"Better player: {comparison[f'player{1 if better_player == 354 else 2}']['name']}")
```

### 3. Find Best Value Players

```python
# Get best value midfielders
value_mids = analyzer.get_value_players(position=3, limit=10)

for _, player in value_mids.iterrows():
    print(f"{player['web_name']}: £{player['now_cost']/10:.1f}m - Value: {player['value']:.2f}")
```

### 4. Optimize Squad

```python
# Generate optimal squad
result = optimizer.optimize_squad(budget=1000, horizon=5)

print(f"Total cost: £{result['total_cost']:.1f}m")
print(f"Expected points: {result['total_expected_points']:.1f}")

for player in result['players']:
    print(f"  {player['name']} ({player['team']}) - £{player['cost']:.1f}m")
```

### 5. Optimize Starting XI

```python
# Given a squad of 15 player IDs
squad_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]  # Your squad

lineup = optimizer.optimize_starting_xi(squad_ids)

print(f"Formation: {lineup['formation']}")
print(f"Expected points: {lineup['total_expected_points']:.1f}")

print("\nStarting XI:")
for player in lineup['starting_xi']:
    print(f"  {player['name']} - EP: {player['expected_points']:.1f}")

print("\nBench:")
for player in lineup['bench']:
    print(f"  {player['name']} - EP: {player['expected_points']:.1f}")
```

### 6. Get Transfer Suggestions

```python
team_id = 123456  # Your team ID

# Single transfer
transfers = transfer_suggester.suggest_transfers(
    team_id=team_id,
    num_transfers=1,
    horizon=5,
    free_transfers=1,
    bank=0.5  # Money in the bank
)

print(f"Recommendation: {transfers['recommendation']}")
print(f"Expected improvement: {transfers['expected_improvement']:.1f} points")

for transfer in transfers['transfers']:
    print(f"\nOut: {transfer['out']['name']} (£{transfer['out']['cost']:.1f}m)")
    print(f"In:  {transfer['in']['name']} (£{transfer['in']['cost']:.1f}m)")
    print(f"Improvement: +{transfer['points_improvement']:.1f} points")
```

### 7. Evaluate Wildcard

```python
team_id = 123456

wildcard = transfer_suggester.evaluate_wildcard(team_id, horizon=10)

print(f"Recommended: {wildcard['recommended']}")
print(f"Current expected: {wildcard['current_expected_points']:.1f}")
print(f"Optimal expected: {wildcard['optimal_expected_points']:.1f}")
print(f"Improvement: {wildcard['improvement']:.1f}")
print(f"Reasoning: {wildcard['reasoning']}")
```

### 8. Captain Selection

```python
squad_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

captain_rec = captain_selector.suggest_captain(squad_ids, num_gameweeks=1)

captain = captain_rec['captain']
print(f"Captain: {captain['name']} ({captain['team']})")
print(f"Expected points: {captain['expected_points']:.1f}")
print(f"Ceiling: {captain['ceiling']:.1f}")
print(f"Reasoning: {captain['reasoning']}")

# Differential option
if captain_rec['differential_option']:
    diff = captain_rec['differential_option']
    print(f"\nDifferential: {diff['name']}")
    print(f"Ownership: {diff['ownership']:.1f}%")
```

### 9. Triple Captain Evaluation

```python
squad_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

tc_eval = captain_selector.evaluate_triple_captain(squad_ids)

print(f"Recommended: {tc_eval['recommended']}")
print(f"Reason: {tc_eval['reason']}")
print(f"Reasoning: {tc_eval['reasoning']}")

if tc_eval['recommended'] and 'player' in tc_eval:
    player = tc_eval['player']
    print(f"Best player: {player['name']} (EP: {player['expected_points']:.1f})")
```

### 10. Comprehensive Chip Recommendations

```python
team_id = 123456

chips = chip_advisor.get_chip_recommendations(team_id)

print(f"Current gameweek: {chips['current_gameweek']}")
print(f"Chips used: {chips['chips_used']}")
print(f"Chips available: {chips['chips_available']}")

strategy = chips['strategy']
print(f"\nStrategy: {strategy['recommendation']}")
if 'reasoning' in strategy:
    print(f"Reasoning: {strategy['reasoning']}")

# Individual chip recommendations
if 'wildcard' in chips:
    wc = chips['wildcard']
    print(f"\nWildcard: {'YES' if wc['recommended'] else 'NO'}")
    print(f"  {wc['reasoning']}")

if 'triple_captain' in chips:
    tc = chips['triple_captain']
    print(f"\nTriple Captain: {'YES' if tc['recommended'] else 'NO'}")
    print(f"  {tc['reasoning']}")
```

## Working with DataFrames

The `PlayerAnalyzer` uses pandas DataFrames internally:

```python
# Access the full player DataFrame
df = analyzer.players_df

# Filter by position
goalkeepers = df[df['element_type'] == 1]
defenders = df[df['element_type'] == 2]
midfielders = df[df['element_type'] == 3]
forwards = df[df['element_type'] == 4]

# Filter by team
team_id = 1  # Arsenal
arsenal_players = df[df['team'] == team_id]

# Sort by points
top_scorers = df.nlargest(10, 'total_points')

# Custom analysis
high_form = df[df['form'].astype(float) > 5]
expensive = df[df['now_cost'] > 100]  # > £10.0m
```

## Error Handling

```python
try:
    result = optimizer.optimize_squad()
    if 'error' in result:
        print(f"Error: {result['error']}")
    else:
        # Process result
        pass
except Exception as e:
    print(f"Exception: {e}")
```

## Custom Horizons and Constraints

```python
# Short-term optimization (next 3 gameweeks)
result_short = optimizer.optimize_squad(horizon=3)

# Long-term optimization (next 10 gameweeks)
result_long = optimizer.optimize_squad(horizon=10)

# Custom budget (e.g., for team value)
result_custom = optimizer.optimize_squad(budget=1050, horizon=5)  # £105.0m

# Multiple transfers
transfers_multi = transfer_suggester.suggest_transfers(
    team_id=123456,
    num_transfers=3,
    horizon=5,
    free_transfers=1,  # 1 free, 2 cost 4 points each
    bank=2.0  # £2.0m in the bank
)
```

## Batch Processing

```python
# Analyze multiple teams
team_ids = [123456, 234567, 345678]

for team_id in team_ids:
    try:
        transfers = transfer_suggester.suggest_transfers(team_id)
        print(f"\nTeam {team_id}:")
        print(f"  {transfers['recommendation']}")
    except:
        print(f"Could not analyze team {team_id}")

# Compare multiple players
player_ids = [354, 355, 356]  # Haaland, Salah, Kane (example)
scores = [analyzer.get_player_score(pid, horizon=5) for pid in player_ids]

# Sort by expected points
scores.sort(key=lambda x: x['expected_points'], reverse=True)

print("Player rankings:")
for i, score in enumerate(scores, 1):
    print(f"{i}. {score['name']}: {score['expected_points']:.1f} points")
```

## Integration with Web Apps

```python
# Flask example
from flask import Flask, jsonify
app = Flask(__name__)

# Initialize once at startup
api = FPLApi()
analyzer = PlayerAnalyzer(api)
analyzer.load_data()
optimizer = TeamOptimizer(api, analyzer)

@app.route('/api/optimal-squad')
def get_optimal_squad():
    result = optimizer.optimize_squad(horizon=5)
    return jsonify(result)

@app.route('/api/captain/<int:team_id>')
def get_captain(team_id):
    picks = api.get_team_picks(team_id)
    squad_ids = [pick['element'] for pick in picks['picks']]
    captain_selector = CaptainSelector(api, analyzer)
    result = captain_selector.suggest_captain(squad_ids)
    return jsonify(result)

if __name__ == '__main__':
    app.run()
```

## Caching and Performance

```python
# Force refresh data
analyzer.api.get_bootstrap_data(force_refresh=True)
analyzer.api.get_fixtures(force_refresh=True)
analyzer.load_data()

# First load is slow, subsequent calls use cached data
result1 = optimizer.optimize_squad()  # ~10 seconds
result2 = optimizer.optimize_squad()  # < 1 second (uses cache)
```

## Advanced: Custom Expected Points

```python
# Override expected points calculation
def custom_expected_points(player_id):
    # Your custom logic here
    player = analyzer.players_df[analyzer.players_df['id'] == player_id].iloc[0]
    
    # Example: weight form more heavily
    form = float(player['form']) if player['form'] else 0
    ppg = float(player['points_per_game']) if player['points_per_game'] else 0
    
    return (form * 0.8) + (ppg * 0.2)

# Apply to all players
analyzer.players_df['custom_ep'] = analyzer.players_df['id'].apply(custom_expected_points)
```

