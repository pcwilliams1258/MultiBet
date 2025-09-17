"""API poller for fetching data from external sources."""

import requests
from typing import Dict, Any, Optional


class APIPoller:
    """Polls external APIs for betting data."""
    
    def __init__(self, base_url: str = None, api_key: str = None):
        """Initialize the API poller.
        
        Args:
            base_url: Base URL for the API
            api_key: API key for authentication
        """
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})
    
    def fetch_odds(self, match_id: str) -> Optional[Dict[str, Any]]:
        """Fetch odds data for a specific match.
        
        Args:
            match_id: Unique identifier for the match
            
        Returns:
            Odds data or None if fetch fails
        """
        if not self.base_url:
            return None
        
        try:
            url = f"{self.base_url}/odds/{match_id}"
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return None
    
    def fetch_match_data(self, sport: str, date: str = None) -> Optional[Dict[str, Any]]:
        """Fetch match data for a specific sport and date.
        
        Args:
            sport: Sport type (e.g., 'football', 'basketball')
            date: Date in YYYY-MM-DD format
            
        Returns:
            Match data or None if fetch fails
        """
        if not self.base_url:
            return None
        
        try:
            url = f"{self.base_url}/matches/{sport}"
            params = {"date": date} if date else {}
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return None