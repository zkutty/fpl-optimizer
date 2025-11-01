"""
Team Optimizer - Uses linear programming to select the optimal FPL team
"""
import pulp
import pandas as pd
from typing import Dict, List, Optional, Tuple
from fpl_api import FPLApi
from player_analyzer import PlayerAnalyzer


class TeamOptimizer:
    """Optimizes team selection using linear programming"""
    
    # FPL constraints
    TOTAL_BUDGET = 1000  # £100.0m in tenths
    SQUAD_SIZE = 15
    TEAM_POSITIONS = {
        1: (2, 2),   # GK: min 2, max 2
        2: (5, 5),   # DEF: min 5, max 5
        3: (5, 5),   # MID: min 5, max 5
        4: (3, 3)    # FWD: min 3, max 3
    }
    MAX_PLAYERS_PER_TEAM = 3
    
    # Starting 11 constraints
    STARTING_XI_SIZE = 11
    FORMATION_CONSTRAINTS = {
        1: (1, 1),   # GK: exactly 1
        2: (3, 5),   # DEF: 3-5
        3: (2, 5),   # MID: 2-5
        4: (1, 3)    # FWD: 1-3
    }
    
    def __init__(self, api: FPLApi, analyzer: PlayerAnalyzer):
        self.api = api
        self.analyzer = analyzer
        
    def optimize_squad(self, budget: Optional[int] = None, horizon: int = 5) -> Dict:
        """
        Optimize squad selection for the next N gameweeks.
        
        Args:
            budget: Budget in tenths (default: 1000 = £100.0m)
            horizon: Number of gameweeks to optimize for
            
        Returns:
            Dictionary containing optimal squad and metadata
        """
        if budget is None:
            budget = self.TOTAL_BUDGET
        
        # Get all available players
        players_df = self.analyzer.players_df
        available_players = players_df[
            (players_df['status'] == 'a') &
            (players_df['chance_of_playing_next_round'].isna() | 
             (players_df['chance_of_playing_next_round'] >= 75))
        ].copy()
        
        # Calculate expected points for all players
        available_players['expected_points'] = available_players['id'].apply(
            lambda x: self.analyzer.calculate_expected_points(x, horizon)
        )
        
        # Create the optimization problem
        prob = pulp.LpProblem("FPL_Squad_Selection", pulp.LpMaximize)
        
        # Decision variables: binary variable for each player
        player_vars = {}
        for idx, player in available_players.iterrows():
            player_vars[player['id']] = pulp.LpVariable(
                f"player_{player['id']}", 
                cat='Binary'
            )
        
        # Objective: maximize expected points
        prob += pulp.lpSum([
            player_vars[player['id']] * player['expected_points']
            for _, player in available_players.iterrows()
        ])
        
        # Constraint 1: Total squad size
        prob += pulp.lpSum([
            player_vars[player['id']]
            for _, player in available_players.iterrows()
        ]) == self.SQUAD_SIZE
        
        # Constraint 2: Budget
        prob += pulp.lpSum([
            player_vars[player['id']] * player['now_cost']
            for _, player in available_players.iterrows()
        ]) <= budget
        
        # Constraint 3: Position requirements
        for position, (min_count, max_count) in self.TEAM_POSITIONS.items():
            position_players = available_players[available_players['element_type'] == position]
            prob += pulp.lpSum([
                player_vars[player['id']]
                for _, player in position_players.iterrows()
            ]) >= min_count
            prob += pulp.lpSum([
                player_vars[player['id']]
                for _, player in position_players.iterrows()
            ]) <= max_count
        
        # Constraint 4: Max players per team
        for team_id in available_players['team'].unique():
            team_players = available_players[available_players['team'] == team_id]
            prob += pulp.lpSum([
                player_vars[player['id']]
                for _, player in team_players.iterrows()
            ]) <= self.MAX_PLAYERS_PER_TEAM
        
        # Solve the problem
        prob.solve(pulp.PULP_CBC_CMD(msg=0))
        
        # Extract selected players
        selected_players = []
        total_cost = 0
        total_expected_points = 0
        
        for _, player in available_players.iterrows():
            if player_vars[player['id']].varValue == 1:
                selected_players.append({
                    'id': player['id'],
                    'name': player['web_name'],
                    'team': player['team_name'],
                    'position': player['element_type'],
                    'cost': player['now_cost'] / 10,
                    'expected_points': player['expected_points']
                })
                total_cost += player['now_cost']
                total_expected_points += player['expected_points']
        
        return {
            'players': sorted(selected_players, key=lambda x: (x['position'], -x['expected_points'])),
            'total_cost': total_cost / 10,
            'remaining_budget': (budget - total_cost) / 10,
            'total_expected_points': total_expected_points,
            'status': pulp.LpStatus[prob.status]
        }
    
    def optimize_starting_xi(self, squad_player_ids: List[int]) -> Dict:
        """
        Select the best starting 11 from a squad of 15 players.
        
        Args:
            squad_player_ids: List of player IDs in the squad
            
        Returns:
            Dictionary containing starting XI and bench
        """
        # Get player data for the squad
        squad_df = self.analyzer.players_df[
            self.analyzer.players_df['id'].isin(squad_player_ids)
        ].copy()
        
        # Calculate expected points for next gameweek
        squad_df['expected_points'] = squad_df['id'].apply(
            lambda x: self.analyzer.calculate_expected_points(x, 1)
        )
        
        # Create the optimization problem
        prob = pulp.LpProblem("FPL_Starting_XI", pulp.LpMaximize)
        
        # Decision variables
        player_vars = {}
        for idx, player in squad_df.iterrows():
            player_vars[player['id']] = pulp.LpVariable(
                f"start_{player['id']}", 
                cat='Binary'
            )
        
        # Objective: maximize expected points
        prob += pulp.lpSum([
            player_vars[player['id']] * player['expected_points']
            for _, player in squad_df.iterrows()
        ])
        
        # Constraint 1: Exactly 11 players
        prob += pulp.lpSum([
            player_vars[player['id']]
            for _, player in squad_df.iterrows()
        ]) == self.STARTING_XI_SIZE
        
        # Constraint 2: Formation requirements (1 GK, 3-5 DEF, 2-5 MID, 1-3 FWD)
        for position, (min_count, max_count) in self.FORMATION_CONSTRAINTS.items():
            position_players = squad_df[squad_df['element_type'] == position]
            prob += pulp.lpSum([
                player_vars[player['id']]
                for _, player in position_players.iterrows()
            ]) >= min_count
            prob += pulp.lpSum([
                player_vars[player['id']]
                for _, player in position_players.iterrows()
            ]) <= max_count
        
        # Solve the problem
        prob.solve(pulp.PULP_CBC_CMD(msg=0))
        
        # Extract results
        starting_xi = []
        bench = []
        
        for _, player in squad_df.iterrows():
            player_info = {
                'id': player['id'],
                'name': player['web_name'],
                'team': player['team_name'],
                'position': player['element_type'],
                'expected_points': player['expected_points']
            }
            
            if player_vars[player['id']].varValue == 1:
                starting_xi.append(player_info)
            else:
                bench.append(player_info)
        
        # Sort starting XI by position, then by expected points
        starting_xi.sort(key=lambda x: (x['position'], -x['expected_points']))
        
        # Sort bench: GK first, then by expected points
        bench.sort(key=lambda x: (0 if x['position'] == 1 else 1, -x['expected_points']))
        
        return {
            'starting_xi': starting_xi,
            'bench': bench,
            'total_expected_points': sum(p['expected_points'] for p in starting_xi),
            'formation': self._get_formation(starting_xi)
        }
    
    def _get_formation(self, starting_xi: List[Dict]) -> str:
        """Determine the formation from starting XI"""
        position_counts = {1: 0, 2: 0, 3: 0, 4: 0}
        for player in starting_xi:
            position_counts[player['position']] += 1
        
        # Format as DEF-MID-FWD (exclude GK)
        return f"{position_counts[2]}-{position_counts[3]}-{position_counts[4]}"

