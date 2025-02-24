import csv
from datetime import *
from src.swen344_db_utils import *


def rebuildTables():
    conn = connect()
    cur = conn.cursor()
    drop_sql = """
        DROP TABLE IF EXISTS Memberships CASCADE;
        DROP TABLE IF EXISTS Channels CASCADE;
        DROP TABLE IF EXISTS Communities CASCADE;
        DROP TABLE IF EXISTS Suspensions CASCADE;
        DROP TABLE IF EXISTS Messages CASCADE;
        DROP TABLE IF EXISTS Users CASCADE;
    """
    create_users_sql = """
        CREATE TABLE Users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            contact_info TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
            last_username_change TIMESTAMP
        );
    """
    create_messages_sql = """
        CREATE TABLE Messages (
            id SERIAL PRIMARY KEY,
            sender_id INT REFERENCES Users(id) NOT NULL,
            receiver_id INT REFERENCES Users(id) NOT NULL,
            message TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
            is_unread BOOLEAN DEFAULT TRUE NOT NULL,
            community_id INT REFERENCES Communities(id),
            channel_id INT REFERENCES Channels(id),
            search_vector tsvector
        );
    """
    create_suspensions_sql = """
        CREATE TABLE Suspensions (
            user_id INT REFERENCES Users(id) NOT NULL,
            suspended_until TIMESTAMP,
            PRIMARY KEY(user_id)
        );
    """
    create_communities_sql = """
        CREATE TABLE Communities (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL
        );
    """
    create_channels_sql = """
        CREATE TABLE Channels (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL,
            community_id INT REFERENCES Communities(id) NOT NULL
        );
    """
    create_memberships_sql = """
        CREATE TABLE Memberships (
            user_id INT REFERENCES Users(id) NOT NULL,
            community_id INT REFERENCES Communities(id) NOT NULL,
            channel_id INT REFERENCES Channels(id) NOT NULL,
            suspended BOOLEAN DEFAULT FALSE NOT NULL,
            PRIMARY KEY (user_id, community_id)
        );
    """
    insert_users_sql = """
        INSERT INTO Users (username, contact_info, created_at) VALUES
        ('Abbott', 'abbott@gmail.com', '1922-01-01'),
        ('Costello', 'costello@gmail.com', '1922-01-01'),
        ('Moe', 'moe@gmail.com', '1922-01-01'),
        ('Larry', 'larry@gmail.com', '1922-01-01'),
        ('Curly', 'curly@gmail.com', '1922-01-01'),
        ('DrMarvin', 'drmarvin@gmail.com', '1991-05-16');
    """
    insert_messages_sql = """
        INSERT INTO Messages (sender_id, receiver_id, message, timestamp, is_unread, community_id, channel_id) VALUES
        (1, 2, 'Hey Costello', '1925-01-01', TRUE, 1, 2),
        (2, 1, 'Hey Abbott', '1925-01-02', FALSE, 1, 2),
        (3, 4, 'Hey Larry', '1995-06-01', TRUE, 1, 2),
        (4, 3, 'Hey Moe', '1995-06-05', FALSE, 1, 2),
        (5, 1, 'Hey Abbott', '1970-02-15', TRUE, 1, 2);
    """
    insert_suspensions_sql = """
        INSERT INTO Suspensions (user_id, suspended_until) VALUES
        (4, '2060-01-01'),
        (5, '1999-12-31');
    """
    insert_communities_sql = """
        INSERT INTO Communities (name) VALUES
        ('Arrakis'),
        ('Comedy');
    """
    insert_channels_sql = """
        INSERT INTO Channels (name, community_id) VALUES
        ('Worms', 1),
        ('Random', 1),
        ('ArgumentClinic', 2),
        ('Dialogs', 2),
        ('Comedy', 2);
    """
    cur.execute(drop_sql)
    cur.execute(create_users_sql)
    cur.execute(create_communities_sql)
    cur.execute(create_channels_sql)
    cur.execute(create_memberships_sql)
    cur.execute(create_messages_sql)
    cur.execute(create_suspensions_sql)
    cur.execute(insert_users_sql)
    cur.execute(insert_communities_sql)
    cur.execute(insert_channels_sql)
    # cur.execute(insert_memberships_sql)
    cur.execute(insert_messages_sql)
    cur.execute(insert_suspensions_sql)
    conn.commit()
    conn.close()




def get_messages_between_users_1(user_id, other_user_id):
    sql = """
    SELECT * FROM Messages
    WHERE (sender_id = %s AND receiver_id = %s)
    OR (sender_id = %s AND receiver_id = %s)
    ORDER BY timestamp;
    """
    return exec_get_all(sql, [user_id, other_user_id, other_user_id, user_id])


def get_messages_between_users_2(user1_id, user2_id):
    sql = """
    SELECT id, sender_id, receiver_id, message, timestamp, is_unread, community_id, channel_id
    FROM Messages
    WHERE (sender_id = %s AND receiver_id = %s) OR (sender_id = %s AND receiver_id = %s);
    """
    messages = exec_get_all(sql, [user1_id, user2_id, user2_id, user1_id])        
    return [{
        'id': msg[0],
        'sender_id': msg[1],
        'receiver_id': msg[2],
        'message': msg[3],
        'timestamp': msg[4],
        'is_unread': msg[5],
        'community_id': msg[6],
        'channel_id': msg[7],
    } for msg in messages]


def get_unread_message_count(user_id):
    sql = "SELECT COUNT(*) FROM Messages WHERE receiver_id = %s AND is_unread = TRUE;"
    return exec_get_one(sql, [user_id])


def get_suspension_status(user_id, current_date):
    sql = "SELECT suspended_until FROM Suspensions WHERE user_id = %s AND suspended_until > %s;"
    return exec_get_one(sql, [user_id, current_date])


def send_message_1(sender_id, receiver_id, message, community_id, channel_id):
    #sends messages
    current_timestamp = datetime.now()
    suspended_until = get_suspension_status(sender_id, current_timestamp)    
    if suspended_until:
        raise Exception(f"User is suspended until {suspended_until[0]}.")
    sql = """
    INSERT INTO Messages (sender_id, receiver_id, message, timestamp, is_unread, community_id, channel_id)
    VALUES (%s, %s, %s, CURRENT_TIMESTAMP, TRUE, %s, %s);
    """
    exec_commit(sql, [sender_id, receiver_id, message, community_id, channel_id])

def send_message_3(sender_id, receiver_id, message):
    current_timestamp = datetime.now()
    suspended_until = get_suspension_status(sender_id, current_timestamp)    
    if suspended_until:
        raise Exception(f"User is suspended until {suspended_until[0]}.")
    sql = """
    INSERT INTO Messages (sender_id, receiver_id, message, timestamp, is_unread)
    VALUES (%s, %s, %s, CURRENT_TIMESTAMP, TRUE);
    """
    exec_commit(sql, [sender_id, receiver_id, message])
   
def send_message_2(sender_id, receiver_id, message, community_id, channel_name):
    #also sends messages but for the community and channels
    current_timestamp = datetime.now()
    suspended_until = get_suspension_status(sender_id, current_timestamp)    
    if suspended_until:
        raise Exception(f"User is suspended until {suspended_until[0]}.")
    channel_id = exec_get_one("SELECT id FROM Channels WHERE name = %s", [channel_name])
    if channel_id is None:
        raise ValueError(f"Channel '{channel_name}' does not exist")
    receiver_id = exec_get_one("SELECT id FROM Users WHERE username = %s", [receiver_id])
    if receiver_id is None:
        raise ValueError(f"Receiver '{receiver_id}' does not exist")
    sql = """
    INSERT INTO Messages (sender_id, receiver_id, message, community_id, channel_id, timestamp, is_unread)
    VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP, TRUE)
    """
    exec_commit(sql, [sender_id, receiver_id, message, community_id, channel_id])


def mark_message_as_read(message_id):
    sql = "UPDATE Messages SET is_unread = FALSE WHERE id = %s;"
    exec_commit(sql, [message_id])
       
def change_username(user_id, new_username):
    #changes username
    sql_check = "SELECT last_username_change FROM Users WHERE id = %s;"
    last_change = exec_get_one(sql_check, [user_id])
    if last_change is None or (datetime.now() - last_change[0]).days >= 180:
        sql_update = "UPDATE Users SET username = %s, last_username_change = CURRENT_TIMESTAMP WHERE id = %s;"
        exec_commit(sql_update, [new_username, user_id])
    else:
        raise Exception("You cannot change your username again yet.")


def suspend_user(user_id, until_timestamp):
    #suspends user from the until date
    until_date = datetime.strptime(until_timestamp, '%Y-%m-%d')
    sql = """
        INSERT INTO Suspensions (user_id, suspended_until)
        VALUES (%s, %s);
    """
    exec_commit(sql, [user_id, until_date])


def clear_suspension(user_id):
    #clear suspension from user
    sql = "DELETE FROM Suspensions WHERE user_id = %s;"
    exec_commit(sql, [user_id])


def get_user_id(username):
    #gets the user id
    sql = "SELECT id FROM Users WHERE username = %s;"
    return exec_get_one(sql, [username])[0]
               
def create_user(username, contact_info):
    #creates the user
    sql = """
    INSERT INTO Users (username, contact_info, created_at)
    VALUES (%s, %s, CURRENT_TIMESTAMP) RETURNING id;
    """
    return exec_commit(sql, [username, contact_info])


def get_all_messages():
    #get all messages
    sql = "SELECT * FROM Messages;"
    return exec_get_all(sql)


def update_last_username_change(username, timestamp):
    #update the last username for changes
    sql = """
    UPDATE Users
    SET last_username_change = %s
    WHERE username = %s;
    """
    exec_commit(sql, [timestamp, username])
   
def import_chat_data(csv_file_path):
    #reads the csv and adds the messages
    abbott_id = get_user_id("Abbott")
    costello_id = get_user_id("Costello")
    with open(csv_file_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        headers = next(reader)
        headers = [header.strip() for header in headers]
        reader = csv.DictReader(file, fieldnames=headers)
        for row in reader:
            sender_name = row["Sender"].strip()
            message = row["Message"].strip()
            if sender_name == "Abbott":
                sender_id = abbott_id
            elif sender_name == "Costello":
                sender_id = costello_id
            else:
                continue
            receiver_id = costello_id if sender_name == 'Abbott' else abbott_id
            insert_chat_data(sender_id, receiver_id, message, 1, 2)


def insert_chat_data(sender_id, receiver_id, message, community_id, channel_id):
    #inserts the data for messages
    sql = """
    INSERT INTO Messages (sender_id, receiver_id, message, timestamp, is_unread, community_id, channel_id)
    VALUES (%s, %s, %s, CURRENT_TIMESTAMP, TRUE, %s, %s);
    """
    exec_commit(sql, [sender_id, receiver_id, message, community_id, channel_id])


def join_channel(user_id, channel_id, community_id):
    #makes user joins with channel from membership
    sql = """
    INSERT INTO Memberships (user_id, channel_id, community_id)
    VALUES (%s, %s, %s);
    """
    exec_commit(sql, [user_id, channel_id, community_id])

def leave_community(user_id, community_id):
    #makes the user leave community from their membership
    sql = """
    DELETE FROM Memberships
        WHERE user_id = %s AND community_id = %s;
    """
    exec_commit(sql, [user_id, community_id])

def get_unread_counts(user_id, community_id, channel_id):
     #gets the unread counts in messages
     sql = """
        SELECT COUNT(*) FROM Messages
        WHERE receiver_id = %s AND is_unread = TRUE
    """
     params = [user_id]
     if community_id:
        sql += " AND community_id = %s"
        params.append(community_id)
        
     if channel_id:
        sql += " AND channel_id = %s"
        params.append(channel_id)
        
     return exec_get_one(sql, params)[0]

# def search_messages(query, community_id):
#     """
#     Search messages in a community with full-text search.
    
#     shows:
#         query (str): Search query.
#         community_id (int): Community ID.
    
#     Returns:
#         list: List of messages matching the search query.
#     """
#     query_terms = query.split()
#     tsquery = ' & '.join([f"{term}:" for term in query_terms])
#     sql = """
#         SELECT * FROM Messages
#         WHERE community_id = %s AND to_tsvector(message) @@ to_tsquery(%s);
#     """
#     return exec_get_all(sql, [community_id, tsquery])

    
def search_messages(community_id, search_string):
    tsquery = ' & '.join(search_string.split())
    sql = """
    SELECT id, sender_id, receiver_id, message, timestamp
    FROM Messages
    WHERE community_id = %s AND search_vector @@ to_tsquery(%s);
    """
    return exec_get_all(sql, [community_id, tsquery])

def activity_summary():
    sql = """
    SELECT
      c.name AS community,
      ROUND(COUNT(m.id)::numeric / 30, 2) AS avg_num_messages,
      COUNT(DISTINCT m.sender_id) AS active_users
    FROM Communities c
    JOIN Messages m ON c.id = m.community_id
    WHERE m.timestamp > CURRENT_DATE - INTERVAL '30 days' AND LENGTH(m.message) > 5
    GROUP BY c.name;
    """
    summary = exec_get_all(sql)
    return [{'community': row[0], 'avg_num_messages': row[1], 'active_users': row[2]} for row in summary]

def get_suspended_users(start_date, end_date):
    sql = """
    SELECT DISTINCT u.username
    FROM Users u
    JOIN Messages m ON u.id = m.sender_id
    JOIN Suspensions s ON u.id = s.user_id
    WHERE m.timestamp BETWEEN %s AND %s AND s.suspended_until > CURRENT_TIMESTAMP;
    """
    return [row[0] for row in exec_get_all(sql, [start_date, end_date])]


def send_message_3(sender_id, receiver_id, message, community_id, channel_name):
    current_timestamp = datetime.now()
    suspended_until = get_suspension_status(sender_id, current_timestamp)
    if suspended_until:
        raise Exception(f"User is suspended until {suspended_until[0]}.")
    channel_id = exec_get_one("SELECT id FROM Channels WHERE name = %s", [channel_name])
    if channel_id is None:
        raise ValueError(f"Channel '{channel_name}' does not exist")
    sql = """
    INSERT INTO Messages (sender_id, receiver_id, message, community_id, channel_id, timestamp, is_unread, search_vector)
    VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP, TRUE, to_tsvector(%s))
    """
    exec_commit(sql, [sender_id, receiver_id, message, community_id, channel_id, message])



# def activity_summary(date, community_id):
#     """
#     Get activity summary for a community.
    
#     Args:
#         date (str): Date (YYYY-MM-DD) for which to calculate activity.
#         community_id (int): Community ID.
    
#     Returns:
#         dict: Activity summary with average messages per day and active users.
#     """
#     date = datetime.strptime(date, "%Y-%m-%d")
#     start_date = date - timedelta(days=30)
#     sql = """
#         SELECT 
#             AVG(DAILY_COUNT) AS avg_num_messages,
#             COUNT(DISTINCT sender_id) AS active_users
#         FROM (
#             SELECT 
#                 DATE(timestamp) AS date,
#                 COUNT(*) AS DAILY_COUNT
#             FROM Messages
#             WHERE community_id = %s AND timestamp > %s AND message != '' AND LENGTH(message) > 5
#             GROUP BY DATE(timestamp)
#         ) AS daily_counts;
#     """
#     result = exec_get_one(sql, [community_id, start_date])
#     return {
#         'community': exec_get_one("SELECT name FROM Communities WHERE id = %s;", [community_id])[0],
#         'avg_num_messages': result[0],
#         'active_users': result[1]
#     }


# def moderator_query(start_date, end_date):
#     """
#     List users who sent messages in a date range and are currently suspended.
    
#     Args:
#         start_date (str): Start date (YYYY-MM-DD) for the date range.
#         end_date (str): End date (YYYY-MM-DD) for the date range.
    
#     Returns:
#         list: List of users who sent messages and are suspended.
#     """
#     start_date = datetime.strptime(start_date, "%Y-%m-%d")
#     end_date = datetime.strptime(end_date, "%Y-%m-%d")
#     sql = """
#         SELECT DISTINCT u.username
#         FROM Messages m
#         JOIN Suspensions s ON m.sender_id = s.user_id
#         JOIN Users u ON m.sender_id = u.id
#         WHERE m.timestamp > %s AND m.timestamp < %s;
#     """
#     return [row[0] for row in exec_get_all(sql, [start_date, end_date])]







    