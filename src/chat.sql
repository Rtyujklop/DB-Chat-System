-- -- Drop existing tables
-- DROP TABLE IF EXISTS message_user CASCADE;
-- DROP TABLE IF EXISTS messages CASCADE;
-- DROP TABLE IF EXISTS user_relationships CASCADE;

-- -- Create the updated 'message_user' table
-- CREATE TABLE message_user (
--     user_id             SERIAL PRIMARY KEY,
--     username            TEXT NOT NULL UNIQUE,  
--     created_at          TIMESTAMP NOT NULL,
--     last_username_change TIMESTAMP,  -- Track the last username change date
--     is_suspended        BOOLEAN DEFAULT FALSE,  -- Status of suspension
--     suspension_end      TIMESTAMP,  -- When the suspension ends, if applicable
--     email               TEXT NOT NULL UNIQUE -- Email should be unique
-- );

-- -- Insert data into 'message_user' table
-- INSERT INTO message_user(user_id, username, created_at, last_username_change, email) VALUES
--   (1, 'Abbott', '2040-02-03 04:23', NULL, 'abb@gmail.com'),
--   (2, 'Costello', '1922-03-11 00:00:00', NULL, 'cos@gmail.com'),
--   (3, 'Larry','2060-01-01','2060-01-01','lar@gmail'),
--   (4, 'Moe','2060-01-01','2060-01-01','moe@gmail'),
--   (5, 'Curly','1922-12-31','1922-12-31','cur@gmail'),
--   (6, 'DrMarvin','1991-05-16','1991-05-16','mar@gmail'),
--   (7, 'Bob','1991-05-17','1991-05-17','bob@gmail.com');


-- -- Create the updated 'messages' table
-- CREATE TABLE messages (
--     message_id     SERIAL PRIMARY KEY,
--     sender_id      INTEGER REFERENCES message_user(user_id) ON DELETE CASCADE,
--     recipient_id   INTEGER REFERENCES message_user(user_id) ON DELETE CASCADE,
--     sent_at        TIMESTAMP NOT NULL,
--     is_read        BOOLEAN DEFAULT FALSE, -- 'unread' has been renamed to 'is_read'
--     content        TEXT NOT NULL DEFAULT '' -- Message content
-- );

-- -- Insert data into the 'messages' table
-- INSERT INTO messages(sender_id, recipient_id, sent_at, is_read, content) VALUES
--   (1, 2, '1922-03-11 00:00:00', FALSE, 'Hey Costello'),
--   (2, 1, '2060-01-01 00:00:00', FALSE, 'Hey Abbott'),
--   (3, 4, '2030-06-12 00:00:00',FALSE, 'Hey Larry'),
--   (4, 5, '2060-01-01 00:00:00',FALSE, 'Hi Moe'),
--   (5, 4, '2060-01-01 00:00:00',FALSE, 'Hi Abbott'),
--   (6, 7, '1991-05-16 00:00:00',FALSE, 'Hi'),
--   (7, 6, '1991-05-17 00:00:00',TRUE, 'Im doing the work, Im baby-stepping')
--   ;

-- -- Create a 'user_relationships' table to track unread messages between users
-- CREATE TABLE user_relationships (
--     user_id          INTEGER REFERENCES message_user(user_id) ON DELETE CASCADE,
--     contact_id       INTEGER REFERENCES message_user(user_id) ON DELETE CASCADE,
--     unread_count     INTEGER DEFAULT 0,
--     PRIMARY KEY (user_id, contact_id)
-- );

-- -- Populate 'user_relationships' table
-- This is an example entry; real counts should be updated dynamically
-- INSERT INTO user_relationships (user_id, contact_id, unread_count) VALUES
  -- (6, 7, 1); -- DrMarvin has 1 unread message from Bob

