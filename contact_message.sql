CREATE TABLE contact_messages (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Unique message ID
    name VARCHAR(100) NOT NULL, -- Sender's name
    email VARCHAR(100) NOT NULL, -- Sender's email
    message TEXT NOT NULL, -- Message content
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Time of message submission
);

INSERT INTO contact_messages (name, email, message)
VALUES ('Plvi', 'palavi7@email.com', 'I have a question about my appointment.');

SELECT * FROM contact_messages;




