-- Create the giftcard_system database if it doesn't exist
DROP DATABASE IF EXISTS giftcard_system_db;
CREATE DATABASE giftcard_system_db;

-- Connect to the giftcard_system_db database
\c giftcard_system_db;

-- Drop the giftcards table if it already exists
DROP TABLE IF EXISTS giftcards;

-- Create the giftcards table if it doesn't exist
CREATE TABLE giftcards (
    id SERIAL PRIMARY KEY,
    giftcard_number BIGINT NOT NULL UNIQUE,
    amount NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    created_time TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    last_used_time TIMESTAMPTZ
);

-- Sample data to insert into the giftcards table
INSERT INTO giftcards (giftcard_number, amount, created_time, last_used_time) VALUES
(12345678, 50.00, '2024-02-16 10:15:23', '2024-02-16 12:30:45'),
(23456789, 100.00, '2024-02-15 14:20:35', NULL),
(34567890, 25.00, '2024-02-14 08:45:10', '2024-02-15 09:10:20');
