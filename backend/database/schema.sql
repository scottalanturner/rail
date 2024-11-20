-- Train positions table
CREATE TABLE train_positions (
    train_id VARCHAR(50) PRIMARY KEY,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    direction VARCHAR(20) NOT NULL,
    speed DECIMAL(6, 2) NOT NULL,
    last_updated TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Create index on last_updated for efficient querying of recent positions
CREATE INDEX idx_train_positions_last_updated 
ON train_positions(last_updated);

-- Predicted crossings table
CREATE TABLE predicted_crossings (
    crossing_id SERIAL PRIMARY KEY,
    predicted_time TIMESTAMP WITH TIME ZONE NOT NULL,
    confidence_score DECIMAL(4, 3) NOT NULL,
    prediction_created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Create index on predicted_time for efficient querying of future predictions
CREATE INDEX idx_predicted_crossings_predicted_time 
ON predicted_crossings(predicted_time); 