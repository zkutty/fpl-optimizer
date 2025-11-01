"""
Chip Advisor - Recommends when to use FPL chips (Wildcard, Free Hit, Bench Boost, Triple Captain)
"""
import pandas as pd
from typing import Dict, List, Optional
from fpl_api import FPLApi
from player_analyzer import PlayerAnalyzer
from transfer_suggester import TransferSuggester
from captain_selector import CaptainSelector


class ChipAdvisor:
    """Advises on optimal chip usage strategy"""
    
    def __init__(
        self, 
        api: FPLApi, 
        analyzer: PlayerAnalyzer,
        transfer_suggester: TransferSuggester,
        captain_selector: CaptainSelector
    ):
        self.api = api
        self.analyzer = analyzer
        self.transfer_suggester = transfer_suggester
        self.captain_selector = captain_selector
        
    def get_chip_recommendations(self, team_id: int) -> Dict:
        """
        Get comprehensive chip usage recommendations.
        
        Args:
            team_id: FPL team ID
            
        Returns:
            Dictionary with all chip recommendations
        """
        try:
            # Get team data
            team_data = self.api.get_team(team_id)
            team_history = self.api.get_team_history(team_id)
            
            # Check which chips have been used
            chips_used = {chip['name'] for chip in team_history.get('chips', [])}
            
            current_gw = self.api.get_current_gameweek()
            picks_data = self.api.get_team_picks(team_id, current_gw)
            current_squad = [pick['element'] for pick in picks_data['picks']]
            
            recommendations = {
                'current_gameweek': current_gw,
                'chips_used': list(chips_used),
                'chips_available': []
            }
            
            # Wildcard
            if 'wildcard' not in chips_used and '3xc' not in chips_used:  # wildcard chip name varies
                wildcard_rec = self.transfer_suggester.evaluate_wildcard(team_id, horizon=10)
                if 'error' not in wildcard_rec:
                    recommendations['wildcard'] = wildcard_rec
                    if wildcard_rec['recommended']:
                        recommendations['chips_available'].append('wildcard')
            
            # Triple Captain
            if '3xc' not in chips_used:
                tc_rec = self.captain_selector.evaluate_triple_captain(current_squad)
                recommendations['triple_captain'] = tc_rec
                if tc_rec['recommended']:
                    recommendations['chips_available'].append('3xc')
            
            # Bench Boost
            if 'bboost' not in chips_used:
                bb_rec = self._evaluate_bench_boost(current_squad)
                recommendations['bench_boost'] = bb_rec
                if bb_rec['recommended']:
                    recommendations['chips_available'].append('bboost')
            
            # Free Hit
            if 'freehit' not in chips_used:
                fh_rec = self._evaluate_free_hit(team_id, current_gw)
                recommendations['free_hit'] = fh_rec
                if fh_rec['recommended']:
                    recommendations['chips_available'].append('freehit')
            
            # Overall strategy recommendation
            recommendations['strategy'] = self._get_overall_strategy(
                recommendations, current_gw
            )
            
            return recommendations
            
        except Exception as e:
            return {
                'error': f'Could not generate chip recommendations: {str(e)}'
            }
    
    def _evaluate_bench_boost(self, squad_player_ids: List[int]) -> Dict:
        """
        Evaluate whether to use Bench Boost chip.
        Best used on double gameweeks or when bench has high expected points.
        """
        current_gw = self.api.get_current_gameweek()
        
        # Check for double gameweeks
        fixtures = self.api.get_fixtures()
        fixtures_df = pd.DataFrame(fixtures)
        gw_fixtures = fixtures_df[fixtures_df['event'] == current_gw]
        
        teams_with_dgw = []
        for team_id in self.analyzer.teams_df['id']:
            team_fixtures = gw_fixtures[
                (gw_fixtures['team_h'] == team_id) | (gw_fixtures['team_a'] == team_id)
            ]
            if len(team_fixtures) >= 2:
                teams_with_dgw.append(team_id)
        
        # Get squad data
        squad_df = self.analyzer.players_df[
            self.analyzer.players_df['id'].isin(squad_player_ids)
        ].copy()
        
        # Calculate expected points
        squad_df['expected_points'] = squad_df['id'].apply(
            lambda x: self.analyzer.calculate_expected_points(x, 1)
        )
        
        # Sort by expected points to simulate lineup
        squad_df = squad_df.sort_values('expected_points', ascending=False)
        
        # Assume top 11 are starters, bottom 4 are bench
        bench = squad_df.tail(4)
        bench_expected = bench['expected_points'].sum()
        
        # Check if bench players have DGW
        bench_dgw_count = (bench['team'].isin(teams_with_dgw)).sum()
        
        # Recommend if:
        # 1. It's a double gameweek with multiple bench players having DGW
        # 2. Bench expected points is > 15 (average 3.75 per player)
        
        if bench_dgw_count >= 2 and bench_expected > 12:
            recommended = True
            reason = f"Double gameweek with {bench_dgw_count} bench players having DGW"
        elif bench_expected > 15:
            recommended = True
            reason = f"Strong bench with {bench_expected:.1f} expected points"
        elif len(teams_with_dgw) > 0 and bench_expected > 10:
            recommended = True
            reason = f"Double gameweek opportunity with decent bench"
        else:
            recommended = False
            reason = f"Bench too weak ({bench_expected:.1f} expected points) or no DGW"
        
        return {
            'recommended': recommended,
            'reason': reason,
            'bench_expected_points': bench_expected,
            'double_gameweek': len(teams_with_dgw) > 0,
            'bench_players': [
                {
                    'name': row['web_name'],
                    'team': row['team_name'],
                    'expected_points': row['expected_points'],
                    'has_dgw': row['team'] in teams_with_dgw
                }
                for _, row in bench.iterrows()
            ]
        }
    
    def _evaluate_free_hit(self, team_id: int, current_gw: int) -> Dict:
        """
        Evaluate whether to use Free Hit chip.
        Best used when many players blank or have difficult fixtures.
        """
        try:
            # Get current squad
            picks_data = self.api.get_team_picks(team_id, current_gw)
            current_squad = [pick['element'] for pick in picks_data['picks']]
            
            # Get squad data
            squad_df = self.analyzer.players_df[
                self.analyzer.players_df['id'].isin(current_squad)
            ].copy()
            
            # Calculate expected points for current squad
            squad_df['expected_points'] = squad_df['id'].apply(
                lambda x: self.analyzer.calculate_expected_points(x, 1)
            )
            
            current_expected = squad_df['expected_points'].sum()
            
            # Check fixture difficulty
            squad_df['fixture_difficulty'] = squad_df['team'].apply(
                lambda x: self.analyzer._get_fixture_difficulty(x, 1)
            )
            
            # Count players with difficult fixtures (4+)
            difficult_fixtures = (squad_df['fixture_difficulty'] >= 4).sum()
            
            # Count blanking players (expected < 2 points)
            blanking_players = (squad_df['expected_points'] < 2).sum()
            
            # Check for double gameweeks
            fixtures = self.api.get_fixtures()
            fixtures_df = pd.DataFrame(fixtures)
            gw_fixtures = fixtures_df[fixtures_df['event'] == current_gw]
            
            teams_with_dgw = []
            for team_id_check in self.analyzer.teams_df['id']:
                team_fixtures = gw_fixtures[
                    (gw_fixtures['team_h'] == team_id_check) | 
                    (gw_fixtures['team_a'] == team_id_check)
                ]
                if len(team_fixtures) >= 2:
                    teams_with_dgw.append(team_id_check)
            
            # Count current squad players in DGW
            dgw_in_squad = (squad_df['team'].isin(teams_with_dgw)).sum()
            
            # Recommend Free Hit if:
            # 1. Many difficult fixtures and few DGW players
            # 2. Many blanking players
            # 3. There's a big DGW but you don't have many players
            
            if len(teams_with_dgw) >= 5 and dgw_in_squad < 5:
                recommended = True
                reason = f"Big double gameweek but only {dgw_in_squad} of your players have DGW"
            elif difficult_fixtures >= 8:
                recommended = True
                reason = f"{difficult_fixtures} players have very difficult fixtures"
            elif blanking_players >= 7:
                recommended = True
                reason = f"{blanking_players} players expected to blank"
            elif current_expected < 35:
                recommended = True
                reason = f"Low expected points ({current_expected:.1f}) this gameweek"
            else:
                recommended = False
                reason = "Current squad is reasonably strong for this gameweek"
            
            return {
                'recommended': recommended,
                'reason': reason,
                'current_expected_points': current_expected,
                'difficult_fixtures_count': difficult_fixtures,
                'blanking_players_count': blanking_players,
                'dgw_teams': len(teams_with_dgw),
                'dgw_in_squad': dgw_in_squad
            }
            
        except Exception as e:
            return {
                'recommended': False,
                'reason': f'Could not evaluate: {str(e)}'
            }
    
    def _get_overall_strategy(self, recommendations: Dict, current_gw: int) -> Dict:
        """Generate overall chip strategy recommendations"""
        chips_available = recommendations.get('chips_available', [])
        
        if not chips_available:
            return {
                'recommendation': 'No chips recommended for this gameweek',
                'priority': None
            }
        
        # Priority order: Free Hit (for DGW) > Triple Captain (for DGW) > Bench Boost (for DGW) > Wildcard
        priorities = []
        
        if 'freehit' in chips_available:
            fh_rec = recommendations.get('free_hit', {})
            if fh_rec.get('dgw_teams', 0) >= 5:
                priorities.append(('freehit', 'high', fh_rec.get('reason', '')))
        
        if '3xc' in chips_available:
            tc_rec = recommendations.get('triple_captain', {})
            if tc_rec.get('reason') == 'Double Gameweek':
                priorities.append(('3xc', 'high', tc_rec.get('reasoning', '')))
            elif tc_rec.get('recommended'):
                priorities.append(('3xc', 'medium', tc_rec.get('reasoning', '')))
        
        if 'bboost' in chips_available:
            bb_rec = recommendations.get('bench_boost', {})
            if bb_rec.get('double_gameweek') and bb_rec.get('bench_expected_points', 0) > 12:
                priorities.append(('bboost', 'high', bb_rec.get('reason', '')))
            elif bb_rec.get('recommended'):
                priorities.append(('bboost', 'medium', bb_rec.get('reason', '')))
        
        if 'wildcard' in chips_available:
            wc_rec = recommendations.get('wildcard', {})
            if wc_rec.get('recommended'):
                if current_gw <= 10:
                    priorities.append(('wildcard', 'high', 'Early season team overhaul'))
                else:
                    priorities.append(('wildcard', 'medium', wc_rec.get('reasoning', '')))
        
        if not priorities:
            return {
                'recommendation': 'Chips available but not optimal to use this gameweek',
                'priority': None,
                'advice': 'Save chips for more favorable gameweeks (e.g., double gameweeks)'
            }
        
        # Sort by priority
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        priorities.sort(key=lambda x: priority_order[x[1]])
        
        top_chip = priorities[0]
        
        return {
            'recommendation': f"Use {top_chip[0]} chip",
            'priority': top_chip[1],
            'reasoning': top_chip[2],
            'all_options': [
                {'chip': p[0], 'priority': p[1], 'reason': p[2]}
                for p in priorities
            ]
        }

