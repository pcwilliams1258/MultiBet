"""Data schemas for the MultiBet application."""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class OddsData(BaseModel):
    """Schema for odds data."""
    home_win: float = Field(..., gt=0, description="Odds for home team win")
    draw: Optional[float] = Field(None, gt=0, description="Odds for draw")
    away_win: float = Field(..., gt=0, description="Odds for away team win")
    timestamp: datetime = Field(..., description="Timestamp when odds were recorded")


class MatchData(BaseModel):
    """Schema for match data."""
    match_id: str = Field(..., description="Unique identifier for the match")
    home_team: str = Field(..., description="Home team name")
    away_team: str = Field(..., description="Away team name")
    sport: str = Field(..., description="Sport type")
    match_date: datetime = Field(..., description="Date and time of the match")
    opening_odds: OddsData = Field(..., description="Opening odds")
    closing_odds: Optional[OddsData] = Field(None, description="Closing odds")
    current_odds: Optional[OddsData] = Field(None, description="Current odds")


class PredictionData(BaseModel):
    """Schema for model predictions."""
    match_id: str = Field(..., description="Unique identifier for the match")
    home_win_probability: float = Field(..., ge=0, le=1, description="Probability of home win")
    draw_probability: Optional[float] = Field(None, ge=0, le=1, description="Probability of draw")
    away_win_probability: float = Field(..., ge=0, le=1, description="Probability of away win")
    model_version: str = Field(..., description="Version of the model used")
    prediction_timestamp: datetime = Field(..., description="When prediction was made")


class ValueBet(BaseModel):
    """Schema for value betting opportunities."""
    match_id: str = Field(..., description="Unique identifier for the match")
    bet_type: str = Field(..., description="Type of bet (home_win, draw, away_win)")
    odds: float = Field(..., gt=0, description="Bookmaker odds")
    predicted_probability: float = Field(..., ge=0, le=1, description="Model predicted probability")
    value_score: float = Field(..., description="Calculated value score")
    clv_score: Optional[float] = Field(None, description="Closing Line Value score")
    recommended_stake: Optional[float] = Field(None, ge=0, description="Recommended stake amount")


class MatchResult(BaseModel):
    """Schema for match results."""
    match_id: str = Field(..., description="Unique identifier for the match")
    home_score: int = Field(..., ge=0, description="Home team score")
    away_score: int = Field(..., ge=0, description="Away team score")
    result: str = Field(..., description="Match result (home_win, draw, away_win)")
    status: str = Field(..., description="Match status (completed, cancelled, etc.)")
    completed_at: datetime = Field(..., description="When the match was completed")