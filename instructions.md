# Project overview

This project aims to develop a real-time train monitoring system for the town center's railroad crossing, providing public updates through a dedicated website. The system will utilize machine learning technologies to predict train movements, addressing the challenge of variable and unpublished train schedules.

The core infrastructure consists of strategically placed cameras monitoring the railroad line. When train movement is detected, the system will securely transmit this data to Amazon Web Services (AWS) through either Lambda functions or S3 storage, depending on the data type and processing requirements.

The cloud-based component of the system will handle both real-time processing and predictive analytics. As train movement data accumulates in the AWS database, the machine learning algorithm will analyze historical patterns to generate probability predictions for train crossings at different times throughout the day. This predictive capability is essential since the official train schedule is not publicly available and varies regularly.

The system requires robust data collection, processing, and storage mechanisms. The database will store historical train movement data, detected patterns, and prediction models, while maintaining data integrity and accessibility.

The public interface will be delivered through a user-friendly website, providing real-time updates on current train positions and predicted crossing times. The wesbite will handle very low volume, only a few requests per hour. The website needs to display a map of the town with the railroad crossing highlighted. It should also display the current train positions and predicted crossing times. The train positions should be displayed as a train icon moving along a train track line.

Regular model retraining, and performance monitoring will be essential to maintain prediction accuracy and overall system reliability.

You will be using the following frontend technologies:

Next.js
React
TailwindCSS
WebSocket client

You will be using the following backend technologies:

Python (for camera/ML processing)
AWS Lambda
API Gateway (REST and WebSocket)
RDS (PostgreSQL)

Amazon SageMaker would integrate into the train monitoring system:
SageMaker would handle two main functions:

Training the model to detect trains from camera images
Making predictions about future train arrivals based on historical data

The flow would work like this:

Cameras capture images -> S3 bucket
Lambda triggers SageMaker endpoint for real-time inference (train detection)
Results stored in RDS database
Separate SageMaker endpoint used for time-series predictions of future crossings

# Core functionalities
1. Real-Time Train Detection
   - Camera System Setup
     * Configure and position cameras at strategic points
     * Implement image capture and preprocessing in Python
     * Set up secure image transmission to S3

   - Image Processing Pipeline
     * Create S3 bucket for image storage
     * Develop Lambda function for image preprocessing
     * Configure SageMaker endpoint for train detection
     * Store detection results in RDS

2. Train Movement Prediction
   - Historical Data Management
     * Design PostgreSQL schema for train movement data
     * Implement data storage procedures in Lambda

   - ML Prediction System
     * Develop time-series prediction model in SageMaker
     * Set up model training pipeline
     * Configure model retraining schedule
     * Create prediction accuracy monitoring system

3. Website Development
   - Frontend Interface
     * Create Next.js application structure
     * Implement town map display with railway crossing
     * Design train position visualization
     * Build prediction time display components
     * Implement WebSocket connection for real-time updates

   - Backend API
     * Set up API Gateway endpoints (REST and WebSocket)
     * Create Lambda functions for data retrieval
     * Implement WebSocket broadcast system
     * Configure secure API access

4. Database System
   - Data Structure
     * Train detection records
     * Historical movement patterns
     * Prediction results
     * System performance metrics

   - Data Access
     * Create database access layer
     * Implement data retrieval APIs

5. Integration & Monitoring
   - System Integration
     * Link ML predictions to website display
     * Integrate real-time updates with frontend

   - Performance Monitoring
     * Set up ML model performance tracking
     * Implement error logging and alerting

# Doc




# Current file structure