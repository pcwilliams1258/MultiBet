"""Value scorer for evaluating betting opportunities."""


class ValueScorer:
    """Calculates value scores for betting opportunities."""
    
    def __init__(self):
        """Initialize the value scorer."""
        pass
    
    def calculate_value_score(self, predicted_probability, odds):
        """Calculate the value score for a betting opportunity.
        
        Args:
            predicted_probability: Model's predicted probability
            odds: Bookmaker odds
            
        Returns:
            Value score (positive indicates value)
        """
        if odds <= 0 or predicted_probability <= 0 or predicted_probability >= 1:
            return 0.0
        
        # Value = (probability * odds) - 1
        return (predicted_probability * odds) - 1.0
    
    def calculate_clv(self, opening_odds, closing_odds, predicted_probability):
        """Calculate Closing Line Value (CLV).
        
        Args:
            opening_odds: Opening odds
            closing_odds: Closing odds
            predicted_probability: Model's predicted probability
            
        Returns:
            CLV value
        """
        if closing_odds <= 0 or predicted_probability <= 0:
            return 0.0
        
        # CLV = (opening_odds - closing_odds) / closing_odds
        return (opening_odds - closing_odds) / closing_odds