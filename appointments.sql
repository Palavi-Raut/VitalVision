CREATE TABLE appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    doctor VARCHAR(100),
    date DATE,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO appointments (name, email, phone, doctor, date, message)
VALUES ('plvi raut', 'palavi7@example.com', '1234567890', 'Dr. Krishnan Kumar', '2025-04-10', 'Routine Checkup');

SELECT * FROM appointments;