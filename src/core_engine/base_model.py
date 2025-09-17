"""Base model for the MultiBet application."""


class BaseModel:
    """Base class for all MultiBet models."""
    
    def __init__(self):
        """Initialize the base model."""
        pass
    
    def predict(self, data):
        """Make predictions on the given data.
        
        Args:
            data: Input data for prediction
            
        Returns:
            Prediction results
        """
        raise NotImplementedError("Subclasses must implement predict method")
    
    def train(self, training_data):
        """Train the model on the given training data.
        
        Args:
            training_data: Data to train the model on
        """
        raise NotImplementedError("Subclasses must implement train method")