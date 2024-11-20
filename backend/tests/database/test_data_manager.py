"""Database test data management utilities."""

import argparse
import sys
import random
from typing import List, Dict
from datetime import datetime, timedelta
from backend.database.db_config import DatabaseConfig
from backend.common.dao.train_dao import TrainDAO

class TestDataManager:
    """Manages test data operations for the database."""

    def __init__(self):
        self.db_config = DatabaseConfig()
        self.train_dao = TrainDAO()

    def populate_test_data(self) -> None:
        """Populate the database with test data"""
        try:
            # Sample train positions
            train_positions = self._generate_train_positions()
            
            # Use TrainDAO to insert train positions
            for train_data in train_positions:
                self.train_dao.update_train_position({
                    'train_id': train_data['train_id'],
                    'latitude': train_data['latitude'],
                    'longitude': train_data['longitude'],
                    'direction': train_data['direction'],
                    'speed': train_data['speed']
                })

            # Sample predicted crossings
            predicted_crossings = self._generate_predicted_crossings()
            
            # Use TrainDAO to insert predicted crossings
            for crossing in predicted_crossings:
                self.train_dao.insert_predicted_crossing({
                    'crossing_id': crossing['crossing_id'],
                    'time_slot': crossing['time_slot'],
                    'crossing_probability': crossing['crossing_probability'],
                    'predictions_count': crossing['predictions_count']
                })

        except Exception as e:
            print(f"Error populating test data: {str(e)}")
            raise

    def clear_all_data(self) -> None:
        """Remove all data from the database tables."""
        try:
            with self.db_config.get_connection() as conn:
                with conn.cursor() as cur:
                    # MySQL doesn't support TRUNCATE CASCADE
                    # First disable foreign key checks
                    cur.execute("SET FOREIGN_KEY_CHECKS = 0")
                    cur.execute("TRUNCATE TABLE train_positions")
                    cur.execute("TRUNCATE TABLE predicted_crossings")
                    cur.execute("SET FOREIGN_KEY_CHECKS = 1")
                conn.commit()
            print("All data cleared successfully")

        except Exception as e:
            print(f"Error clearing data: {str(e)}")
            raise

    def _generate_train_positions(self) -> List[Dict]:
        """Generate sample train position data"""
        return [
            {
                'train_id': 'TRAIN001',
                'latitude': 42.3601,
                'longitude': -71.0589,
                'direction': 'N',
                'speed': 45.5
            },
            {
                'train_id': 'TRAIN002',
                'latitude': 42.3502,
                'longitude': -71.0677,
                'direction': 'S',
                'speed': 38.2
            }
        ]

    def _generate_predicted_crossings(self) -> List[Dict]:
        """Generate sample crossing predictions in 10-minute increments."""
        current_time = datetime.now()
        start_time = current_time.replace(minute=current_time.minute // 10 * 10, 
                                        second=0, microsecond=0)
        predictions = []
        
        for i in range(144):
            time_slot = start_time + timedelta(minutes=i * 10)
            hour = time_slot.hour
            
            if (7 <= hour <= 9) or (16 <= hour <= 18):
                base_prob = random.uniform(0.4, 0.8)
            else:
                base_prob = random.uniform(0.1, 0.3)
            
            if hour % 2 == 0 and time_slot.minute < 20:
                base_prob += random.uniform(0.2, 0.4)
            
            probability = round(min(max(base_prob, 0.0), 1.0), 3)
            
            predictions.append({
                'crossing_id': 'CROSSING_MAIN_ST',
                'time_slot': time_slot,
                'crossing_probability': probability,
                'predictions_count': random.randint(1, 10)
            })
        
        return predictions

    def generate_sql_inserts(self) -> None:
        """Generate SQL INSERT statements for test data"""
        try:
            # Print train position inserts
            print("-- Train Position Inserts")
            for train_data in self._generate_train_positions():
                print(f"""INSERT INTO train_positions 
                    (train_id, latitude, longitude, direction, speed)
                    VALUES (
                        '{train_data['train_id']}',
                        {train_data['latitude']},
                        {train_data['longitude']},
                        '{train_data['direction']}',
                        {train_data['speed']}
                    );""")
            
            # Print predicted crossing inserts
            print("\n-- Predicted Crossing Inserts")
            print("INSERT INTO predicted_crossings \
                  (crossing_id, time_slot, crossing_probability, predictions_count) VALUES")
            
            crossings = self._generate_predicted_crossings()
            values = []
            for crossing in crossings:
                values.append(f"""(
                    '{crossing['crossing_id']}',
                    '{crossing['time_slot'].strftime('%Y-%m-%d %H:%M:%S')}',
                    {crossing['crossing_probability']},
                    {crossing['predictions_count']}
                )""")
            
            # Join all values with commas and add semicolon at the end
            print(',\n'.join(values) + ';')

        except Exception as e:
            print(f"Error generating SQL: {str(e)}")
            raise

    def test_connection(self) -> bool:
        """Test if database connection is working."""
        try:
            with self.db_config.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")
                    result = cur.fetchone()
                    cur.close()
                    return True
        except Exception as e:
            print(f"Connection test failed: {str(e)}")
            return False

def main():
    """Main function to handle database test data operations."""
    parser = argparse.ArgumentParser(description='Database test data management utility')
    parser.add_argument('--populate', action='store_true', 
                       help='Populate the database with test data')
    parser.add_argument('--clear', action='store_true',
                       help='Clear all data from the database')
    parser.add_argument('--generate-sql', action='store_true',
                       help='Generate SQL INSERT statements')
    parser.add_argument('--test-connection', action='store_true',
                       help='Test database connection')
    
    args = parser.parse_args()
    
    if not (args.populate or args.clear or args.generate_sql or args.test_connection):
        parser.print_help()
        sys.exit(1)
    
    manager = TestDataManager()
    
    if args.test_connection:
        success = manager.test_connection()
        print("Database connection test:", "SUCCESS" if success else "FAILED")
        if not success:
            sys.exit(1)
    
    if args.clear:
        manager.clear_all_data()
    
    if args.populate:
        manager.populate_test_data()
        
    if args.generate_sql:
        manager.generate_sql_inserts()

if __name__ == "__main__":
    main() 