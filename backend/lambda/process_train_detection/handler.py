import json
from datetime import datetime
import logging

from backend.common.dao.train_dao import TrainDAO

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    AWS Lambda handler for processing new train detection data
    
    Expected event body format:
    {
        "location_id": int,
        "confidence_score": float,  # Optional, defaults to 1.0
        "direction": string,        # Optional, defaults to "UNKNOWN"
        "detection_time": string    # Optional, defaults to current time
    }
    """
    try:
        logger.info("Processing new train detection")
        
        # Parse input
        body = json.loads(event['body']) if isinstance(event.get('body'), str) else event.get('body', {})
        logger.info(f"Received detection data: {body}")
        
        # Validate input
        validate_detection_data(body)
        
        # Prepare detection data
        detection_data = {
            'location_id': body['location_id'],
            'detection_time': body.get('detection_time', datetime.now().isoformat()),
            'confidence_score': body.get('confidence_score', 1.0),
            'direction': body.get('direction', 'UNKNOWN')
        }

        # Initialize DAO with Lambda configuration
        train_dao = TrainDAO(is_lambda=True)
        
        try:
            # Insert detection
            detection_id = train_dao.insert_detection(detection_data)
            logger.info(f"Inserted detection with ID: {detection_id}")
            
            # Get recent detection history for this location
            recent_detections = train_dao.get_recent_detections(detection_data['location_id'])
            logger.info(f"Found {len(recent_detections)} recent detections")
            
            # Calculate initial probability
            # TODO: Replace with actual ML model prediction
            initial_probability = 0.5
            
            # Update crossing predictions
            train_dao.update_crossing_prediction(detection_id, initial_probability)
            logger.info(f"Updated crossing prediction with probability: {initial_probability}")
            
            # Prepare success response
            response = {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'  # Configure as needed for CORS
                },
                'body': json.dumps({
                    'detection_id': detection_id,
                    'probability': initial_probability,
                    'message': 'Detection processed successfully',
                    'timestamp': datetime.now().isoformat()
                })
            }
            
            return response
            
        except Exception as e:
            logger.error(f"Database operation failed: {str(e)}")
            raise

    except ValueError as ve:
        logger.error(f"Validation error: {str(ve)}")
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(ve),
                'message': 'Invalid input data'
            })
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(e),
                'message': 'Internal server error'
            })
        } 