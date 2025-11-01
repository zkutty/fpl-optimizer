"""
FPL API Client - Fetches data from the official Fantasy Premier League API
"""
import requests
import time
from typing import Dict, List, Optional
from datetime import datetime


class FPLApi:
    """Client for interacting with the FPL API"""
    
    BASE_URL = "https://fantasy.premierleague.com/api"
    
    def __init__(self):
        self.session = requests.Session()
        self._bootstrap_data = None
        self._fixtures = None
        
    def get_bootstrap_data(self, force_refresh: bool = False) -> Dict:
        """
        Get bootstrap-static data containing all players, teams, and gameweek info.
        This is cached to avoid excessive API calls.
        """
        if self._bootstrap_data is None or force_refresh:
            url = f"{self.BASE_URL}/bootstrap-static/"
            response = self.session.get(url)
            response.raise_for_status()
            self._bootstrap_data = response.json()
        return self._bootstrap_data
    
    def get_players(self) -> List[Dict]:
        """Get all player data"""
        data = self.get_bootstrap_data()
        return data['elements']
    
    def get_teams(self) -> List[Dict]:
        """Get all team data"""
        data = self.get_bootstrap_data()
        return data['teams']
    
    def get_element_types(self) -> List[Dict]:
        """Get player position types (GK, DEF, MID, FWD)"""
        data = self.get_bootstrap_data()
        return data['element_types']
    
    def get_current_gameweek(self) -> int:
        """Get the current gameweek number"""
        data = self.get_bootstrap_data()
        for event in data['events']:
            if event['is_current']:
                return event['id']
        # If no current gameweek, return next one
        for event in data['events']:
            if event['is_next']:
                return event['id']
        return 1
    
    def get_gameweeks(self) -> List[Dict]:
        """Get all gameweek information"""
        data = self.get_bootstrap_data()
        return data['events']
    
    def get_fixtures(self, force_refresh: bool = False) -> List[Dict]:
        """Get all fixture data"""
        if self._fixtures is None or force_refresh:
            url = f"{self.BASE_URL}/fixtures/"
            response = self.session.get(url)
            response.raise_for_status()
            self._fixtures = response.json()
        return self._fixtures
    
    def get_player_details(self, player_id: int) -> Dict:
        """Get detailed information for a specific player"""
        url = f"{self.BASE_URL}/element-summary/{player_id}/"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_team(self, team_id: int) -> Dict:
        """Get a user's FPL team"""
        url = f"{self.BASE_URL}/entry/{team_id}/"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_team_picks(self, team_id: int, gameweek: Optional[int] = None) -> Dict:
        """Get a user's team picks for a specific gameweek"""
        if gameweek is None:
            gameweek = self.get_current_gameweek()
        url = f"{self.BASE_URL}/entry/{team_id}/event/{gameweek}/picks/"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_team_transfers(self, team_id: int) -> Dict:
        """Get a user's transfer history"""
        url = f"{self.BASE_URL}/entry/{team_id}/transfers/"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_team_history(self, team_id: int) -> Dict:
        """Get a user's team history"""
        url = f"{self.BASE_URL}/entry/{team_id}/history/"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

