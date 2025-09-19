"""
API clients for external data sources.
"""

import requests
from typing import Dict, Any


class RaceCardClient:
    """Client for fetching race card data from external APIs."""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
    
    def fetch_race_card(self, race_id: str) -> Dict[str, Any]:
        """
        Fetch race card data for a specific race.
        
        Args:
            race_id: The ID of the race to fetch data for
            
        Returns:
            Dictionary containing race card data
        """
        response = requests.get(f"{self.base_url}/races/{race_id}")
        if response.status_code != 200:
            raise ValueError("Failed to fetch race card")
        
        return response.json()
    
    def fetch_odds(self, race_id: str) -> Dict[str, Any]:
        """
        Fetch odds data for a specific race.
        
        Args:
            race_id: The ID of the race to fetch odds for
            
        Returns:
            Dictionary containing odds data
        """
        response = requests.get(f"{self.base_url}/races/{race_id}/odds")
        if response.status_code != 200:
            raise ValueError("Failed to fetch odds data")
        
        return response.json()