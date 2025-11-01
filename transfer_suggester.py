"""
Transfer Suggester - Recommends optimal transfers for your FPL team
"""
import pulp
import pandas as pd
from typing import Dict, List, Optional, Tuple
from fpl_api import FPLApi
from player_analyzer import PlayerAnalyzer
from team_optimizer import TeamOptimizer


class TransferSuggester:
    """Suggests optimal transfers considering constraints and costs"""
    
    def __init__(self, api: FPLApi, analyzer: PlayerAnalyzer, optimizer: TeamOptimizer):
        self.api = api
        self.analyzer = analyzer
        self.optimizer = optimizer
        
    def suggest_transfers(
        self, 
        team_id: int, 
        num_transfers: int = 1,
        horizon: int = 5,
        free_transfers: int = 1,
        bank: float = 0.0
    ) -> Dict:
        """
        Suggest optimal transfers for a team.
        
        Args:
            team_id: FPL team ID
            num_transfers: Number of transfers to make
            horizon: Number of gameweeks to optimize for
            free_transfers: Number of free transfers available
            bank: Money in the bank (ITB)
            
        Returns:
            Dictionary with transfer suggestions
        """
        # Get current team
        try:
            current_gw = self.api.get_current_gameweek()
            picks_data = self.api.get_team_picks(team_id, current_gw)
            current_squad = [pick['element'] for pick in picks_data['picks']]
        except:
            return {
                'error': 'Could not fetch team data. Please check team ID.',
                'transfers': []
            }
        
        # Get current squad data
        current_squad_df = self.analyzer.players_df[
            self.analyzer.players_df['id'].isin(current_squad)
        ].copy()
        
        # Calculate current squad value and expected points
        current_squad_df['expected_points'] = current_squad_df['id'].apply(
            lambda x: self.analyzer.calculate_expected_points(x, horizon)
        )
        
        current_value = current_squad_df['now_cost'].sum()
        available_budget = current_value + (bank * 10)
        
        # Calculate transfer cost
        transfer_cost = max(0, num_transfers - free_transfers) * 4  # 4 points per extra transfer
        
        # Get all available players
        all_players_df = self.analyzer.players_df[
            (self.analyzer.players_df['status'] == 'a') &
            (~self.analyzer.players_df['id'].isin(current_squad))
        ].copy()
        
        all_players_df['expected_points'] = all_players_df['id'].apply(
            lambda x: self.analyzer.calculate_expected_points(x, horizon)
        )
        
        # Find best transfers
        if num_transfers == 1:
            transfers = self._find_single_transfer(
                current_squad_df, all_players_df, available_budget, transfer_cost
            )
        else:
            transfers = self._find_multiple_transfers(
                current_squad_df, all_players_df, available_budget, 
                num_transfers, transfer_cost
            )
        
        return transfers
    
    def _find_single_transfer(
        self, 
        current_squad: pd.DataFrame, 
        available_players: pd.DataFrame,
        budget: int,
        transfer_cost: int
    ) -> Dict:
        """Find the best single transfer"""
        best_transfer = None
        best_improvement = -transfer_cost  # Account for transfer cost
        
        for _, current_player in current_squad.iterrows():
            position = current_player['element_type']
            current_team = current_player['team']
            
            # Find potential replacements in same position
            replacements = available_players[
                available_players['element_type'] == position
            ]
            
            for _, new_player in replacements.iterrows():
                # Check if we can afford this transfer
                cost_diff = new_player['now_cost'] - current_player['now_cost']
                if cost_diff > budget - current_squad['now_cost'].sum():
                    continue
                
                # Check team constraint (max 3 per team)
                if new_player['team'] == current_team:
                    # Same team, no issue
                    pass
                else:
                    # Check if adding this player would exceed 3 from their team
                    team_count = (current_squad['team'] == new_player['team']).sum()
                    if team_count >= 3:
                        continue
                
                # Calculate improvement
                points_improvement = (
                    new_player['expected_points'] - 
                    current_player['expected_points'] - 
                    transfer_cost
                )
                
                if points_improvement > best_improvement:
                    best_improvement = points_improvement
                    best_transfer = {
                        'out': {
                            'id': current_player['id'],
                            'name': current_player['web_name'],
                            'team': current_player['team_name'],
                            'position': current_player['element_type'],
                            'cost': current_player['now_cost'] / 10,
                            'expected_points': current_player['expected_points']
                        },
                        'in': {
                            'id': new_player['id'],
                            'name': new_player['web_name'],
                            'team': new_player['team_name'],
                            'position': new_player['element_type'],
                            'cost': new_player['now_cost'] / 10,
                            'expected_points': new_player['expected_points']
                        },
                        'cost_change': cost_diff / 10,
                        'points_improvement': points_improvement
                    }
        
        if best_transfer is None:
            return {
                'recommendation': 'No beneficial transfers found',
                'transfers': [],
                'expected_improvement': 0
            }
        
        return {
            'recommendation': f"Transfer out {best_transfer['out']['name']} for {best_transfer['in']['name']}",
            'transfers': [best_transfer],
            'expected_improvement': best_improvement
        }
    
    def _find_multiple_transfers(
        self, 
        current_squad: pd.DataFrame,
        available_players: pd.DataFrame,
        budget: int,
        num_transfers: int,
        transfer_cost: int
    ) -> Dict:
        """Find the best combination of multiple transfers"""
        # For multiple transfers, we use a greedy approach
        # In practice, you might want to use more sophisticated optimization
        
        transfers = []
        working_squad = current_squad.copy()
        remaining_budget = budget
        total_improvement = -transfer_cost
        
        for i in range(num_transfers):
            best_transfer = None
            best_improvement = 0
            
            for _, current_player in working_squad.iterrows():
                position = current_player['element_type']
                
                # Find potential replacements
                replacements = available_players[
                    (available_players['element_type'] == position) &
                    (~available_players['id'].isin([t['in']['id'] for t in transfers]))
                ]
                
                for _, new_player in replacements.iterrows():
                    # Check affordability
                    cost_diff = new_player['now_cost'] - current_player['now_cost']
                    new_total = working_squad['now_cost'].sum() + cost_diff
                    if new_total > remaining_budget:
                        continue
                    
                    # Check team constraint
                    temp_squad = working_squad[working_squad['id'] != current_player['id']]
                    team_count = (temp_squad['team'] == new_player['team']).sum()
                    if team_count >= 3:
                        continue
                    
                    # Calculate improvement (no additional transfer cost for subsequent transfers)
                    points_improvement = new_player['expected_points'] - current_player['expected_points']
                    
                    if points_improvement > best_improvement:
                        best_improvement = points_improvement
                        best_transfer = {
                            'out': {
                                'id': current_player['id'],
                                'name': current_player['web_name'],
                                'team': current_player['team_name'],
                                'position': current_player['element_type'],
                                'cost': current_player['now_cost'] / 10,
                                'expected_points': current_player['expected_points']
                            },
                            'in': {
                                'id': new_player['id'],
                                'name': new_player['web_name'],
                                'team': new_player['team_name'],
                                'position': new_player['element_type'],
                                'cost': new_player['now_cost'] / 10,
                                'expected_points': new_player['expected_points']
                            },
                            'cost_change': cost_diff / 10,
                            'points_improvement': points_improvement
                        }
            
            if best_transfer is None:
                break
            
            # Apply the transfer
            transfers.append(best_transfer)
            total_improvement += best_improvement
            
            # Update working squad
            working_squad = working_squad[working_squad['id'] != best_transfer['out']['id']]
            new_row = available_players[available_players['id'] == best_transfer['in']['id']].iloc[0]
            working_squad = pd.concat([working_squad, new_row.to_frame().T])
        
        return {
            'recommendation': f"Make {len(transfers)} transfer(s)",
            'transfers': transfers,
            'expected_improvement': total_improvement
        }
    
    def evaluate_wildcard(self, team_id: int, horizon: int = 5) -> Dict:
        """
        Evaluate whether using a wildcard is beneficial.
        Compares the best possible team vs current team.
        
        Args:
            team_id: FPL team ID
            horizon: Number of gameweeks to optimize for
            
        Returns:
            Dictionary with wildcard recommendation
        """
        try:
            # Get current team
            current_gw = self.api.get_current_gameweek()
            picks_data = self.api.get_team_picks(team_id, current_gw)
            current_squad = [pick['element'] for pick in picks_data['picks']]
            
            # Calculate current team value
            current_squad_df = self.analyzer.players_df[
                self.analyzer.players_df['id'].isin(current_squad)
            ].copy()
            
            current_squad_df['expected_points'] = current_squad_df['id'].apply(
                lambda x: self.analyzer.calculate_expected_points(x, horizon)
            )
            
            current_value = current_squad_df['now_cost'].sum()
            current_expected = current_squad_df['expected_points'].sum()
            
            # Get optimal team with same budget
            optimal_team = self.optimizer.optimize_squad(budget=current_value, horizon=horizon)
            
            improvement = optimal_team['total_expected_points'] - current_expected
            
            # Wildcard is worth it if improvement > ~20-30 points over the horizon
            threshold = 20 if horizon >= 5 else 15
            
            return {
                'recommended': improvement > threshold,
                'current_expected_points': current_expected,
                'optimal_expected_points': optimal_team['total_expected_points'],
                'improvement': improvement,
                'optimal_team': optimal_team['players'],
                'reasoning': self._get_wildcard_reasoning(improvement, threshold)
            }
            
        except Exception as e:
            return {
                'error': f'Could not evaluate wildcard: {str(e)}',
                'recommended': False
            }
    
    def _get_wildcard_reasoning(self, improvement: float, threshold: float) -> str:
        """Generate reasoning for wildcard recommendation"""
        if improvement > threshold * 1.5:
            return f"Strongly recommend using wildcard. Expected improvement of {improvement:.1f} points is significant."
        elif improvement > threshold:
            return f"Recommend using wildcard. Expected improvement of {improvement:.1f} points justifies the chip usage."
        elif improvement > threshold * 0.7:
            return f"Marginal case. Expected improvement of {improvement:.1f} points. Consider team situation and remaining chips."
        else:
            return f"Do not recommend wildcard. Expected improvement of {improvement:.1f} points is too small."

