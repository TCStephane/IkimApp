cCREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY, 
    username VARCHAR(50) NOT NULL UNIQUE, 
    password VARCHAR(255) NOT NULL, 
    role ENUM('admin', 'treasurer', 'member') NOT NULL DEFAULT 'member', 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);