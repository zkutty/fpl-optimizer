"""
Player Analysis Module - Analyzes player performance and calculates expected points
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from fpl_api import FPLApi


class PlayerAnalyzer:
    """Analyzes player data to predict future performance"""
    
    def __init__(self, api: FPLApi):
        self.api = api
        self.players_df = None
        self.teams_df = None
        self.fixtures_df = None
        
    def load_data(self):
        """Load and prepare player and team data"""
        # Load players
        players = self.api.get_players()
        self.players_df = pd.DataFrame(players)
        
        # Load teams
        teams = self.api.get_teams()
        self.teams_df = pd.DataFrame(teams)
        
        # Load fixtures
        fixtures = self.api.get_fixtures()
        self.fixtures_df = pd.DataFrame(fixtures)
        
        # Add team names to players
        team_map = dict(zip(self.teams_df['id'], self.teams_df['name']))
        self.players_df['team_name'] = self.players_df['team'].map(team_map)
        
    def calculate_expected_points(self, player_id: int, num_gameweeks: int = 5) -> float:
        """
        Calculate expected points for a player over the next N gameweeks.
        Uses a weighted combination of:
        - Recent form (last 5 games)
        - Season points per game
        - Fixture difficulty
        - Minutes played tendency
        """
        player = self.players_df[self.players_df['id'] == player_id].iloc[0]
        
        # Base expected points from form and season average
        form = float(player['form']) if player['form'] else 0
        ep_next = float(player['ep_next']) if player['ep_next'] else 0
        points_per_game = float(player['points_per_game']) if player['points_per_game'] else 0
        
        # Weight recent form more heavily
        base_ep = (form * 0.5) + (points_per_game * 0.3) + (ep_next * 0.2)
        
        # Adjust for fixture difficulty
        fixture_difficulty = self._get_fixture_difficulty(player['team'], num_gameweeks)
        difficulty_multiplier = self._difficulty_to_multiplier(fixture_difficulty)
        
        # Adjust for minutes played (availability)
        minutes_played = float(player['minutes'])
        starts = player['starts'] if player['starts'] > 0 else 1
        total_possible = 90 * starts
        availability = min(minutes_played / total_possible, 1.0) if total_possible > 0 else 0.5
        
        # Calculate final expected points
        expected_points = base_ep * difficulty_multiplier * availability * num_gameweeks
        
        return max(expected_points, 0)
    
    def _get_fixture_difficulty(self, team_id: int, num_gameweeks: int) -> float:
        """Get average fixture difficulty for a team over next N gameweeks"""
        current_gw = self.api.get_current_gameweek()
        
        # Filter fixtures for this team in upcoming gameweeks
        team_fixtures = self.fixtures_df[
            (self.fixtures_df['event'] >= current_gw) &
            (self.fixtures_df['event'] < current_gw + num_gameweeks) &
            ((self.fixtures_df['team_h'] == team_id) | (self.fixtures_df['team_a'] == team_id))
        ]
        
        if len(team_fixtures) == 0:
            return 3.0  # Neutral difficulty
        
        difficulties = []
        for _, fixture in team_fixtures.iterrows():
            if fixture['team_h'] == team_id:
                # Home game - use away team difficulty
                difficulties.append(fixture['team_h_difficulty'])
            else:
                # Away game - use home team difficulty
                difficulties.append(fixture['team_a_difficulty'])
        
        return np.mean(difficulties) if difficulties else 3.0
    
    def _difficulty_to_multiplier(self, difficulty: float) -> float:
        """Convert fixture difficulty rating to expected points multiplier"""
        # Difficulty ranges from 1 (easy) to 5 (hard)
        # Multiplier ranges from 1.2 (easy) to 0.8 (hard)
        return 1.4 - (difficulty * 0.12)
    
    def get_value_players(self, position: Optional[int] = None, limit: int = 10) -> pd.DataFrame:
        """
        Get the best value players (points per million).
        
        Args:
            position: Filter by position (1=GK, 2=DEF, 3=MID, 4=FWD)
            limit: Number of players to return
        """
        df = self.players_df.copy()
        
        # Filter by position if specified
        if position:
            df = df[df['element_type'] == position]
        
        # Calculate expected points for next gameweek
        df['expected_points'] = df['id'].apply(lambda x: self.calculate_expected_points(x, 1))
        
        # Calculate value (points per million)
        df['value'] = df['expected_points'] / (df['now_cost'] / 10)
        
        # Filter out unavailable players
        df = df[df['status'] == 'a']  # 'a' = available
        df = df[df['chance_of_playing_next_round'].isna() | (df['chance_of_playing_next_round'] >= 75)]
        
        # Sort by value and return top N
        result = df.nlargest(limit, 'value')[
            ['web_name', 'team_name', 'element_type', 'now_cost', 'expected_points', 'value', 'form']
        ]
        
        return result
    
    def get_player_score(self, player_id: int, horizon: int = 5) -> Dict:
        """
        Get a comprehensive score for a player including all relevant metrics.
        
        Args:
            player_id: Player ID
            horizon: Number of gameweeks to consider
            
        Returns:
            Dictionary with player scores and metrics
        """
        player = self.players_df[self.players_df['id'] == player_id].iloc[0]
        
        expected_points = self.calculate_expected_points(player_id, horizon)
        cost = player['now_cost'] / 10  # Convert to actual price
        
        return {
            'player_id': player_id,
            'name': player['web_name'],
            'team': player['team_name'],
            'position': player['element_type'],
            'cost': cost,
            'expected_points': expected_points,
            'value': expected_points / cost if cost > 0 else 0,
            'form': float(player['form']) if player['form'] else 0,
            'total_points': player['total_points'],
            'selected_by_percent': float(player['selected_by_percent'])
        }
    
    def compare_players(self, player1_id: int, player2_id: int) -> Dict:
        """Compare two players and determine which is better"""
        score1 = self.get_player_score(player1_id)
        score2 = self.get_player_score(player2_id)
        
        # Calculate overall score weighted by multiple factors
        def overall_score(s):
            return (s['expected_points'] * 0.5 + 
                    s['value'] * 0.3 + 
                    s['form'] * 0.2)
        
        return {
            'player1': score1,
            'player2': score2,
            'better_player': player1_id if overall_score(score1) > overall_score(score2) else player2_id,
            'score_difference': abs(overall_score(score1) - overall_score(score2))
        }

