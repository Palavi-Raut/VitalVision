CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),  -- Added phone number field
    password VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (name, email,phone, password) 
VALUES ('palvii', 'palavi7@example.com', '8484912130', 'plvi9');

SELECT * FROM users;

