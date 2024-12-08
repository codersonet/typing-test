-- Create the database
CREATE DATABASE IF NOT EXISTS typing_speed;

-- Use the database
USE typing_speed;

-- Create the user_scores table
CREATE TABLE IF NOT EXISTS user_scores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    difficulty ENUM('easy', 'medium', 'hard') NOT NULL,
    wpm FLOAT NOT NULL,
    accuracy FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the user_logs table
CREATE TABLE IF NOT EXISTS user_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    test_date DATE NOT NULL,
    test_time TIME NOT NULL,
    difficulty ENUM('easy', 'medium', 'hard') NOT NULL,
    wpm FLOAT NOT NULL,
    accuracy FLOAT NOT NULL,
    marks INT NOT NULL,
    elapsed_time FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sample data for testing (optional, remove if not needed)
--INSERT INTO user_scores (name, difficulty, wpm, accuracy) 
--VALUES 
--('Alice', 'easy', 50.0, 95.0),
--('Bob', 'medium', 42.5, 89.0),
--('Charlie', 'hard', 35.0, 80.0);

--INSERT INTO user_logs (user_name, test_date, test_time, difficulty, wpm, accuracy, marks, elapsed_time) 
--VALUES 
--('Alice', CURDATE(), CURTIME(), 'easy', 50.0, 95.0, 48, 60.0),
--('Bob', CURDATE(), CURTIME(), 'medium', 42.5, 89.0, 37, 75.0),
--('Charlie', CURDATE(), CURTIME(), 'hard', 35.0, 80.0, 28, 90.0);
