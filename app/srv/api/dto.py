from pydantic import BaseModel
import numpy as np

class PredictionInput(BaseModel):
    lead_time: int
    no_of_special_requests: int
    avg_price_per_room: float
    arrival_month: int
    arrival_date: int
    market_segment_type: int
    no_of_week_nights: int
    no_of_weekend_nights: int
    type_of_meal_plan: int
    room_type_reserved: int

    def to_numpy(self) -> np.ndarray:
        """
        Convert the input features into a NumPy array of shape (1, -1)
        suitable for model prediction.
        """
        features = [
            self.lead_time,
            self.no_of_special_requests,
            self.avg_price_per_room,
            self.arrival_month,
            self.arrival_date,
            self.market_segment_type,
            self.no_of_week_nights,
            self.no_of_weekend_nights,
            self.type_of_meal_plan,
            self.room_type_reserved,
        ]
        return np.array(features, dtype=float).reshape(1, -1)
