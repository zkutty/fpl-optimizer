"""
Captain Selector - Recommends captain and vice-captain choices
"""
import pandas as pd
from typing import Dict, List, Tuple
from fpl_api import FPLApi
from player_analyzer import PlayerAnalyzer


class CaptainSelector:
    """Selects optimal captain and vice-captain"""
    
    def __init__(self, api: FPLApi, analyzer: PlayerAnalyzer):
        self.api = api
        self.analyzer = analyzer
        
    def suggest_captain(self, squad_player_ids: List[int], num_gameweeks: int = 1) -> Dict:
        """
        Suggest captain and vice-captain from the squad.
        
        Args:
            squad_player_ids: List of player IDs in the squad
            num_gameweeks: Number of gameweeks to consider (for triple captain decision)
            
        Returns:
            Dictionary with captain recommendations
        """
        # Get squad data
        squad_df = self.analyzer.players_df[
            self.analyzer.players_df['id'].isin(squad_player_ids)
        ].copy()
        
        # Calculate expected points for each player
        squad_df['expected_points'] = squad_df['id'].apply(
            lambda x: self.analyzer.calculate_expected_points(x, num_gameweeks)
        )
        
        # Calculate ceiling (high upside potential) based on position and form
        squad_df['ceiling'] = squad_df.apply(self._calculate_ceiling, axis=1)
        
        # Calculate floor (consistent points) based on minutes and form
        squad_df['floor'] = squad_df.apply(self._calculate_floor, axis=1)
        
        # Get fixture difficulty for next gameweek
        squad_df['fixture_difficulty'] = squad_df['team'].apply(
            lambda x: self.analyzer._get_fixture_difficulty(x, num_gameweeks)
        )
        
        # Sort by expected points
        top_captains = squad_df.nlargest(5, 'expected_points')
        
        # Get top 2 as captain and vice-captain
        captain = top_captains.iloc[0]
        vice_captain = top_captains.iloc[1] if len(top_captains) > 1 else captain
        
        # Alternative differential pick (lower ownership, high ceiling)
        differential = self._find_differential_captain(squad_df, captain['id'])
        
        return {
            'captain': {
                'id': captain['id'],
                'name': captain['web_name'],
                'team': captain['team_name'],
                'position': captain['element_type'],
                'expected_points': captain['expected_points'],
                'fixture_difficulty': captain['fixture_difficulty'],
                'ceiling': captain['ceiling'],
                'ownership': float(captain['selected_by_percent']),
                'reasoning': self._get_captain_reasoning(captain)
            },
            'vice_captain': {
                'id': vice_captain['id'],
                'name': vice_captain['web_name'],
                'team': vice_captain['team_name'],
                'position': vice_captain['element_type'],
                'expected_points': vice_captain['expected_points'],
                'fixture_difficulty': vice_captain['fixture_difficulty']
            },
            'differential_option': differential,
            'top_5_options': [
                {
                    'name': row['web_name'],
                    'team': row['team_name'],
                    'expected_points': row['expected_points'],
                    'ownership': float(row['selected_by_percent'])
                }
                for _, row in top_captains.iterrows()
            ]
        }
    
    def _calculate_ceiling(self, player: pd.Series) -> float:
        """
        Calculate the high upside potential for a player.
        Attackers and players in form have higher ceilings.
        """
        base = float(player['expected_points'])
        
        # Position multiplier (attackers have higher ceiling)
        position_mult = {1: 1.2, 2: 1.3, 3: 1.5, 4: 1.6}
        mult = position_mult.get(player['element_type'], 1.0)
        
        # Form bonus
        form = float(player['form']) if player['form'] else 0
        form_bonus = form * 0.2
        
        # Recent high scores (check creativity/threat/ICT)
        threat = float(player.get('threat', 0))
        threat_bonus = (threat / 100) * 2  # Normalize threat score
        
        return base * mult + form_bonus + threat_bonus
    
    def _calculate_floor(self, player: pd.Series) -> float:
        """
        Calculate the consistent baseline points.
        Players with high minutes and defensive stats have higher floors.
        """
        base = float(player['expected_points']) * 0.6  # Conservative estimate
        
        # Minutes played consistency
        if player['minutes'] > 0 and player['starts'] > 0:
            minutes_ratio = player['minutes'] / (player['starts'] * 90)
            minutes_bonus = minutes_ratio * 2
        else:
            minutes_bonus = 0
        
        # Add bonus for clean sheet potential (defenders/GK)
        if player['element_type'] in [1, 2]:
            clean_sheet_prob = float(player.get('clean_sheets', 0)) / max(player['starts'], 1)
            cs_bonus = clean_sheet_prob * 4
        else:
            cs_bonus = 0
        
        return base + minutes_bonus + cs_bonus
    
    def _find_differential_captain(self, squad_df: pd.DataFrame, captain_id: int) -> Dict:
        """Find a differential captain pick (low ownership, high potential)"""
        # Filter out the main captain and low expected points
        differentials = squad_df[
            (squad_df['id'] != captain_id) &
            (squad_df['expected_points'] > 4)  # Minimum threshold
        ].copy()
        
        if len(differentials) == 0:
            return None
        
        # Calculate differential score: ceiling / ownership
        differentials['ownership'] = differentials['selected_by_percent'].astype(float)
        differentials['diff_score'] = (
            differentials['ceiling'] * 100 / (differentials['ownership'] + 1)
        )
        
        # Get best differential
        best_diff = differentials.nlargest(1, 'diff_score').iloc[0]
        
        return {
            'id': best_diff['id'],
            'name': best_diff['web_name'],
            'team': best_diff['team_name'],
            'expected_points': best_diff['expected_points'],
            'ceiling': best_diff['ceiling'],
            'ownership': best_diff['ownership'],
            'reasoning': f"Differential pick with {best_diff['ownership']:.1f}% ownership and high ceiling"
        }
    
    def _get_captain_reasoning(self, captain: pd.Series) -> str:
        """Generate reasoning for captain choice"""
        reasons = []
        
        # Expected points
        reasons.append(f"Highest expected points ({captain['expected_points']:.1f})")
        
        # Form
        form = float(captain['form']) if captain['form'] else 0
        if form > 6:
            reasons.append(f"excellent form ({form:.1f})")
        elif form > 4:
            reasons.append(f"good form ({form:.1f})")
        
        # Fixture
        difficulty = captain['fixture_difficulty']
        if difficulty < 2.5:
            reasons.append("favorable fixture")
        elif difficulty > 3.5:
            reasons.append("difficult fixture - be cautious")
        
        # Position
        if captain['element_type'] == 4:
            reasons.append("premium forward with high ceiling")
        elif captain['element_type'] == 3:
            reasons.append("attacking midfielder")
        
        return ", ".join(reasons).capitalize()
    
    def evaluate_triple_captain(self, squad_player_ids: List[int]) -> Dict:
        """
        Evaluate whether to use Triple Captain chip.
        Should be used on double gameweeks or very favorable single fixtures.
        
        Args:
            squad_player_ids: List of player IDs in the squad
            
        Returns:
            Dictionary with Triple Captain recommendation
        """
        # Get current gameweek
        current_gw = self.api.get_current_gameweek()
        
        # Check for double gameweeks
        fixtures = self.api.get_fixtures()
        fixtures_df = pd.DataFrame(fixtures)
        
        # Count fixtures per team in current gameweek
        gw_fixtures = fixtures_df[fixtures_df['event'] == current_gw]
        
        teams_with_dgw = []
        for team_id in self.analyzer.teams_df['id']:
            team_fixtures = gw_fixtures[
                (gw_fixtures['team_h'] == team_id) | (gw_fixtures['team_a'] == team_id)
            ]
            if len(team_fixtures) >= 2:
                teams_with_dgw.append(team_id)
        
        # Check if any squad players have double gameweek
        squad_df = self.analyzer.players_df[
            self.analyzer.players_df['id'].isin(squad_player_ids)
        ]
        
        dgw_players = squad_df[squad_df['team'].isin(teams_with_dgw)]
        
        if len(dgw_players) > 0:
            # Calculate expected points for DGW
            dgw_players = dgw_players.copy()
            dgw_players['expected_points'] = dgw_players['id'].apply(
                lambda x: self.analyzer.calculate_expected_points(x, 1) * 1.8  # ~2 games
            )
            
            best_dgw = dgw_players.nlargest(1, 'expected_points').iloc[0]
            
            return {
                'recommended': True,
                'reason': 'Double Gameweek',
                'player': {
                    'id': best_dgw['id'],
                    'name': best_dgw['web_name'],
                    'team': best_dgw['team_name'],
                    'expected_points': best_dgw['expected_points']
                },
                'reasoning': f"{best_dgw['web_name']} has a double gameweek with excellent expected returns"
            }
        
        # Check for exceptional single gameweek (very easy fixture + in-form premium)
        captain_rec = self.suggest_captain(squad_player_ids, 1)
        captain = captain_rec['captain']
        
        # Triple Captain threshold: very easy fixture + high ceiling + premium player
        if (captain['fixture_difficulty'] < 2.0 and 
            captain['ceiling'] > 15 and 
            captain['expected_points'] > 8):
            return {
                'recommended': True,
                'reason': 'Exceptional fixture and form',
                'player': captain,
                'reasoning': f"While not a DGW, {captain['name']} has exceptional fixture and form"
            }
        
        return {
            'recommended': False,
            'reason': 'Wait for better opportunity',
            'reasoning': 'Save Triple Captain for a double gameweek or exceptional fixture'
        }
