#!/usr/bin/env python3
"""
Fantasy Premier League Team Optimizer - Main CLI
"""
import argparse
import sys
from typing import Optional
from fpl_api import FPLApi
from player_analyzer import PlayerAnalyzer
from team_optimizer import TeamOptimizer
from transfer_suggester import TransferSuggester
from captain_selector import CaptainSelector
from chip_advisor import ChipAdvisor


def print_section(title: str):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def print_optimal_squad(result: dict):
    """Print optimal squad selection"""
    print_section("OPTIMAL SQUAD")
    
    if 'error' in result:
        print(f"Error: {result['error']}")
        return
    
    print(f"Total Cost: £{result['total_cost']:.1f}m")
    print(f"Remaining Budget: £{result['remaining_budget']:.1f}m")
    print(f"Total Expected Points: {result['total_expected_points']:.1f}")
    print(f"\nStatus: {result['status']}\n")
    
    # Group by position
    positions = {1: "Goalkeepers", 2: "Defenders", 3: "Midfielders", 4: "Forwards"}
    
    for pos_id in [1, 2, 3, 4]:
        players = [p for p in result['players'] if p['position'] == pos_id]
        if players:
            print(f"\n{positions[pos_id]}:")
            print("-" * 70)
            for p in players:
                print(f"  {p['name']:20} ({p['team']:15}) £{p['cost']:.1f}m  "
                      f"EP: {p['expected_points']:.1f}")


def print_starting_xi(result: dict):
    """Print starting XI and bench"""
    print_section("STARTING XI")
    
    print(f"Formation: {result['formation']}")
    print(f"Total Expected Points: {result['total_expected_points']:.1f}\n")
    
    positions = {1: "GK", 2: "DEF", 3: "MID", 4: "FWD"}
    
    print("Starting XI:")
    print("-" * 70)
    for p in result['starting_xi']:
        print(f"  {positions[p['position']]:5} {p['name']:20} ({p['team']:15}) "
              f"EP: {p['expected_points']:.1f}")
    
    print("\nBench:")
    print("-" * 70)
    for i, p in enumerate(result['bench'], 1):
        print(f"  {i}. {positions[p['position']]:5} {p['name']:20} ({p['team']:15}) "
              f"EP: {p['expected_points']:.1f}")


def print_transfers(result: dict):
    """Print transfer suggestions"""
    print_section("TRANSFER SUGGESTIONS")
    
    if 'error' in result:
        print(f"Error: {result['error']}")
        return
    
    print(f"Recommendation: {result['recommendation']}")
    print(f"Expected Improvement: {result['expected_improvement']:.1f} points\n")
    
    if not result['transfers']:
        print("No beneficial transfers found at this time.")
        return
    
    for i, transfer in enumerate(result['transfers'], 1):
        print(f"\nTransfer {i}:")
        print("-" * 70)
        print(f"  OUT: {transfer['out']['name']:20} ({transfer['out']['team']:15}) "
              f"£{transfer['out']['cost']:.1f}m  EP: {transfer['out']['expected_points']:.1f}")
        print(f"  IN:  {transfer['in']['name']:20} ({transfer['in']['team']:15}) "
              f"£{transfer['in']['cost']:.1f}m  EP: {transfer['in']['expected_points']:.1f}")
        print(f"  Cost Change: {transfer['cost_change']:+.1f}m")
        print(f"  Points Improvement: {transfer['points_improvement']:+.1f}")


def print_captain(result: dict):
    """Print captain recommendations"""
    print_section("CAPTAIN RECOMMENDATIONS")
    
    captain = result['captain']
    vice = result['vice_captain']
    
    print("Captain:")
    print("-" * 70)
    print(f"  {captain['name']} ({captain['team']})")
    print(f"  Expected Points: {captain['expected_points']:.1f}")
    print(f"  Fixture Difficulty: {captain['fixture_difficulty']:.1f}/5")
    print(f"  High Ceiling: {captain['ceiling']:.1f}")
    print(f"  Ownership: {captain['ownership']:.1f}%")
    print(f"  Reasoning: {captain['reasoning']}")
    
    print("\nVice-Captain:")
    print("-" * 70)
    print(f"  {vice['name']} ({vice['team']})")
    print(f"  Expected Points: {vice['expected_points']:.1f}")
    
    if result.get('differential_option'):
        diff = result['differential_option']
        print("\nDifferential Option (Risky):")
        print("-" * 70)
        print(f"  {diff['name']} ({diff['team']})")
        print(f"  Expected Points: {diff['expected_points']:.1f}")
        print(f"  Ceiling: {diff['ceiling']:.1f}")
        print(f"  Ownership: {diff['ownership']:.1f}%")
        print(f"  {diff['reasoning']}")
    
    print("\nTop 5 Captain Options:")
    print("-" * 70)
    for i, option in enumerate(result['top_5_options'], 1):
        print(f"  {i}. {option['name']:20} ({option['team']:15}) "
              f"EP: {option['expected_points']:.1f}  Own: {option['ownership']:.1f}%")


def print_chips(result: dict):
    """Print chip recommendations"""
    print_section("CHIP RECOMMENDATIONS")
    
    if 'error' in result:
        print(f"Error: {result['error']}")
        return
    
    print(f"Current Gameweek: {result['current_gameweek']}")
    print(f"Chips Used: {', '.join(result['chips_used']) if result['chips_used'] else 'None'}\n")
    
    strategy = result.get('strategy', {})
    if strategy:
        print("OVERALL STRATEGY:")
        print("-" * 70)
        print(f"Recommendation: {strategy['recommendation']}")
        if strategy.get('priority'):
            print(f"Priority: {strategy['priority'].upper()}")
            print(f"Reasoning: {strategy.get('reasoning', '')}")
        if strategy.get('advice'):
            print(f"Advice: {strategy['advice']}")
        print()
    
    # Wildcard
    if 'wildcard' in result:
        wc = result['wildcard']
        print("\nWILDCARD:")
        print("-" * 70)
        if 'error' not in wc:
            print(f"Recommended: {'YES' if wc['recommended'] else 'NO'}")
            print(f"Current Expected: {wc['current_expected_points']:.1f} points")
            print(f"Optimal Expected: {wc['optimal_expected_points']:.1f} points")
            print(f"Improvement: +{wc['improvement']:.1f} points")
            print(f"Reasoning: {wc['reasoning']}")
    
    # Triple Captain
    if 'triple_captain' in result:
        tc = result['triple_captain']
        print("\nTRIPLE CAPTAIN:")
        print("-" * 70)
        print(f"Recommended: {'YES' if tc['recommended'] else 'NO'}")
        print(f"Reason: {tc['reason']}")
        print(f"Reasoning: {tc['reasoning']}")
        if 'player' in tc:
            player = tc['player']
            if isinstance(player, dict) and 'name' in player:
                print(f"Best Player: {player['name']} (EP: {player.get('expected_points', 0):.1f})")
    
    # Bench Boost
    if 'bench_boost' in result:
        bb = result['bench_boost']
        print("\nBENCH BOOST:")
        print("-" * 70)
        print(f"Recommended: {'YES' if bb['recommended'] else 'NO'}")
        print(f"Reason: {bb['reason']}")
        print(f"Bench Expected Points: {bb['bench_expected_points']:.1f}")
        print(f"Double Gameweek: {'Yes' if bb['double_gameweek'] else 'No'}")
    
    # Free Hit
    if 'free_hit' in result:
        fh = result['free_hit']
        print("\nFREE HIT:")
        print("-" * 70)
        print(f"Recommended: {'YES' if fh['recommended'] else 'NO'}")
        print(f"Reason: {fh['reason']}")
        if 'current_expected_points' in fh:
            print(f"Current Expected: {fh['current_expected_points']:.1f} points")
            print(f"Difficult Fixtures: {fh.get('difficult_fixtures_count', 0)}")
            print(f"DGW Teams: {fh.get('dgw_teams', 0)}")


def print_value_players(analyzer: PlayerAnalyzer):
    """Print best value players"""
    print_section("BEST VALUE PLAYERS")
    
    positions = {1: "Goalkeepers", 2: "Defenders", 3: "Midfielders", 4: "Forwards"}
    position_map = {1: "GK", 2: "DEF", 3: "MID", 4: "FWD"}
    
    for pos_id in [1, 2, 3, 4]:
        print(f"\n{positions[pos_id]}:")
        print("-" * 70)
        
        value_players = analyzer.get_value_players(position=pos_id, limit=5)
        
        for _, player in value_players.iterrows():
            print(f"  {player['web_name']:20} ({player['team_name']:15}) "
                  f"£{player['now_cost']/10:.1f}m  "
                  f"EP: {player['expected_points']:.1f}  "
                  f"Value: {player['value']:.2f}")


def main():
    parser = argparse.ArgumentParser(
        description='Fantasy Premier League Team Optimizer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Get optimal squad
  python main.py --optimal-squad
  
  # Analyze your team (requires team ID from FPL website)
  python main.py --team-id 123456 --all
  
  # Get transfer suggestions
  python main.py --team-id 123456 --suggest-transfers
  
  # Get captain recommendations
  python main.py --team-id 123456 --suggest-captain
  
  # Get chip recommendations
  python main.py --team-id 123456 --suggest-chips
  
  # Get best value players
  python main.py --value-players
        """
    )
    
    parser.add_argument('--team-id', type=int, help='Your FPL team ID')
    parser.add_argument('--optimal-squad', action='store_true', help='Generate optimal squad')
    parser.add_argument('--suggest-transfers', action='store_true', help='Suggest transfers')
    parser.add_argument('--suggest-lineup', action='store_true', help='Suggest starting XI')
    parser.add_argument('--suggest-captain', action='store_true', help='Suggest captain')
    parser.add_argument('--suggest-chips', action='store_true', help='Suggest chip usage')
    parser.add_argument('--value-players', action='store_true', help='Show best value players')
    parser.add_argument('--all', action='store_true', help='Show all recommendations')
    parser.add_argument('--num-transfers', type=int, default=1, help='Number of transfers to suggest')
    parser.add_argument('--horizon', type=int, default=5, help='Number of gameweeks to optimize for')
    
    args = parser.parse_args()
    
    # If no arguments, show help
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    print_section("FPL TEAM OPTIMIZER")
    print("Loading data from FPL API...")
    
    try:
        # Initialize components
        api = FPLApi()
        analyzer = PlayerAnalyzer(api)
        analyzer.load_data()
        
        optimizer = TeamOptimizer(api, analyzer)
        transfer_suggester = TransferSuggester(api, analyzer, optimizer)
        captain_selector = CaptainSelector(api, analyzer)
        chip_advisor = ChipAdvisor(api, analyzer, transfer_suggester, captain_selector)
        
        print("Data loaded successfully!\n")
        
        # Execute requested analyses
        if args.optimal_squad:
            result = optimizer.optimize_squad(horizon=args.horizon)
            print_optimal_squad(result)
        
        if args.value_players:
            print_value_players(analyzer)
        
        if args.team_id:
            # Get current squad
            current_gw = api.get_current_gameweek()
            picks_data = api.get_team_picks(args.team_id, current_gw)
            current_squad = [pick['element'] for pick in picks_data['picks']]
            
            if args.all or args.suggest_lineup:
                result = optimizer.optimize_starting_xi(current_squad)
                print_starting_xi(result)
            
            if args.all or args.suggest_transfers:
                result = transfer_suggester.suggest_transfers(
                    args.team_id,
                    num_transfers=args.num_transfers,
                    horizon=args.horizon
                )
                print_transfers(result)
            
            if args.all or args.suggest_captain:
                result = captain_selector.suggest_captain(current_squad)
                print_captain(result)
            
            if args.all or args.suggest_chips:
                result = chip_advisor.get_chip_recommendations(args.team_id)
                print_chips(result)
        
        print("\n" + "=" * 70)
        print("Analysis complete!")
        print("=" * 70 + "\n")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

