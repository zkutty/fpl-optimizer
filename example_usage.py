#!/usr/bin/env python3
"""
Example usage of the FPL Optimizer
"""
from fpl_api import FPLApi
from player_analyzer import PlayerAnalyzer
from team_optimizer import TeamOptimizer
from transfer_suggester import TransferSuggester
from captain_selector import CaptainSelector
from chip_advisor import ChipAdvisor


def example_optimal_squad():
    """Example: Generate an optimal squad"""
    print("=" * 70)
    print("EXAMPLE 1: Generate Optimal Squad")
    print("=" * 70 + "\n")
    
    # Initialize
    api = FPLApi()
    analyzer = PlayerAnalyzer(api)
    analyzer.load_data()
    optimizer = TeamOptimizer(api, analyzer)
    
    # Get optimal squad for next 5 gameweeks
    result = optimizer.optimize_squad(horizon=5)
    
    print(f"Total Cost: £{result['total_cost']:.1f}m")
    print(f"Expected Points: {result['total_expected_points']:.1f}\n")
    
    for player in result['players'][:5]:  # Show first 5
        print(f"  {player['name']:20} £{player['cost']:.1f}m  EP: {player['expected_points']:.1f}")
    
    print(f"\n... and {len(result['players']) - 5} more players\n")


def example_value_players():
    """Example: Find best value players"""
    print("=" * 70)
    print("EXAMPLE 2: Find Best Value Players")
    print("=" * 70 + "\n")
    
    api = FPLApi()
    analyzer = PlayerAnalyzer(api)
    analyzer.load_data()
    
    # Get best value midfielders
    value_mids = analyzer.get_value_players(position=3, limit=5)
    
    print("Top 5 Value Midfielders:\n")
    for _, player in value_mids.iterrows():
        print(f"  {player['web_name']:20} £{player['now_cost']/10:.1f}m  "
              f"Value: {player['value']:.2f}")
    print()


def example_captain_selection():
    """Example: Select captain from a sample squad"""
    print("=" * 70)
    print("EXAMPLE 3: Captain Selection")
    print("=" * 70 + "\n")
    
    api = FPLApi()
    analyzer = PlayerAnalyzer(api)
    analyzer.load_data()
    captain_selector = CaptainSelector(api, analyzer)
    
    # Get top 15 players by form as example squad
    top_players = analyzer.players_df.nlargest(15, 'total_points')
    squad_ids = top_players['id'].tolist()
    
    result = captain_selector.suggest_captain(squad_ids)
    
    captain = result['captain']
    print(f"Captain: {captain['name']} ({captain['team']})")
    print(f"Expected Points: {captain['expected_points']:.1f}")
    print(f"Reasoning: {captain['reasoning']}\n")


def example_transfers():
    """Example: Get transfer suggestions (requires valid team ID)"""
    print("=" * 70)
    print("EXAMPLE 4: Transfer Suggestions")
    print("=" * 70 + "\n")
    
    print("To use transfer suggestions, run:")
    print("  python main.py --team-id YOUR_TEAM_ID --suggest-transfers\n")
    print("Find your team ID in the FPL URL when logged in:")
    print("  https://fantasy.premierleague.com/entry/YOUR_TEAM_ID/\n")


def main():
    """Run all examples"""
    print("\n" + "=" * 70)
    print("FPL OPTIMIZER - EXAMPLES")
    print("=" * 70 + "\n")
    
    print("Loading data from FPL API...\n")
    
    try:
        example_optimal_squad()
        example_value_players()
        example_captain_selection()
        example_transfers()
        
        print("=" * 70)
        print("Examples complete!")
        print("=" * 70 + "\n")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nNote: These examples require an active internet connection")
        print("to fetch data from the FPL API.\n")


if __name__ == '__main__':
    main()

