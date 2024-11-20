"""Data Access Object for managing train-related database operations."""

from typing import List, Dict
from backend.database.db_config import DatabaseConfig
from datetime import datetime, timedelta

class TrainDAO:
    """Data Access Object for managing train-related database operations."""
    def __init__(self, is_lambda=False):
        self.db_config = DatabaseConfig(is_lambda=is_lambda)

    def get_current_train_positions(self) -> List[Dict]:
        """Retrieve current train positions from the database"""
        query = """
        SELECT 
            id,
            train_id,
            latitude,
            longitude,
            direction,
            speed,
            last_updated
        FROM train_positions
        WHERE last_updated >= NOW() - INTERVAL 5 MINUTE
        """
        
        try:
            with self.db_config.get_connection() as conn:
                with conn.cursor(dictionary=True) as cur:  # MySQL dictionary cursor
                    cur.execute(query)
                    return cur.fetchall()  # Returns list of dictionaries directly
        except Exception as e:
            print(f"Error fetching train positions: {str(e)}")
            raise

    def update_train_position(self, train_data: Dict) -> bool:
        """Update train position in the database"""
        query = """
        INSERT INTO train_positions 
            (train_id, latitude, longitude, direction, speed)
        VALUES 
            (%(train_id)s, %(latitude)s, %(longitude)s, %(direction)s, %(speed)s)
        """
        
        try:
            with self.db_config.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, train_data)
                    conn.commit()
                    return True
        except Exception as e:
            print(f"Error updating train position: {str(e)}")
            raise

    def insert_predicted_crossing(self, crossing_data: Dict) -> bool:
        """Insert a new predicted crossing"""
        query = """
        INSERT INTO predicted_crossings 
            (crossing_id, time_slot, crossing_probability, predictions_count)
        VALUES 
            (%(crossing_id)s, %(time_slot)s, %(crossing_probability)s, %(predictions_count)s)
        """
        
        try:
            with self.db_config.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, crossing_data)
                    conn.commit()
                    return True
        except Exception as e:
            print(f"Error inserting predicted crossing: {str(e)}")
            raise

    def get_predicted_crossings(self) -> List[Dict]:
        """Retrieve predicted crossing times for the next 24 hours"""
        query = """
        SELECT 
            id,
            crossing_id,
            predicted_time,
            confidence_score,
            prediction_created_at
        FROM predicted_crossings
        WHERE predicted_time >= NOW()
        AND predicted_time <= NOW() + INTERVAL 24 HOUR
        ORDER BY predicted_time ASC
        """
        
        try:
            with self.db_config.get_connection() as conn:
                with conn.cursor(dictionary=True) as cur:  # MySQL dictionary cursor
                    cur.execute(query)
                    return cur.fetchall()  # Returns list of dictionaries directly
        except Exception as e:
            print(f"Error fetching predicted crossings: {str(e)}")
            raise

    def update_crossing_prediction(self, prediction_data: Dict) -> bool:
        """Update or insert a crossing prediction for a 10-minute time slot"""
        query = """
        INSERT INTO predicted_crossings 
            (crossing_id, time_slot, crossing_probability, predictions_count)
        VALUES 
            (%(crossing_id)s, %(time_slot)s, %(crossing_probability)s, %(predictions_count)s)
        ON DUPLICATE KEY UPDATE
            crossing_probability = %(crossing_probability)s,
            predictions_count = %(predictions_count)s,
            last_updated = CURRENT_TIMESTAMP
        """
        
        try:
            with self.db_config.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, prediction_data)
                    conn.commit()
                    return True
        except Exception as e:
            print(f"Error updating crossing prediction: {str(e)}")
            raise

    def get_upcoming_crossing_probabilities(self, crossing_id: str, hours_ahead: int = 2) -> List[Dict]:
        """Get crossing probabilities for upcoming time slots"""
        query = """
        SELECT 
            crossing_id,
            time_slot,
            crossing_probability,
            predictions_count,
            last_updated
        FROM predicted_crossings
        WHERE crossing_id = %(crossing_id)s
        AND time_slot >= %(start_time)s
        AND time_slot < %(end_time)s
        ORDER BY time_slot ASC
        """
        
        try:
            with self.db_config.get_connection() as conn:
                with conn.cursor(dictionary=True) as cur:
                    current_time = datetime.now()
                    # Round current_time down to nearest 10-minute mark
                    current_slot = current_time.replace(minute=current_time.minute // 10 * 10, second=0, microsecond=0)
                    end_time = current_slot + timedelta(hours=hours_ahead)
                    
                    cur.execute(query, {
                        'crossing_id': crossing_id,
                        'start_time': current_slot,
                        'end_time': end_time
                    })
                    return cur.fetchall()
        except Exception as e:
            print(f"Error fetching crossing probabilities: {str(e)}")
            raise 