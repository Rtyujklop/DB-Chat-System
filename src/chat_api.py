# import csv
# import datetime
# from src.swen344_db_utils import *


# def create_user(username):
#     sql = """
#     INSERT INTO message_user (username, created_at, last_username_change, suspended, suspension_reason)
#     VALUES (%s, NOW(), NOW(), FALSE, NULL)
#     RETURNING user_id;
#     """
#     return exec_get_one(sql, (username,))


# def suspend_user(user_id, duration):
#     sql = """
#         UPDATE message_user
#         SET is_suspended = TRUE,
#             suspension_end = NOW() + INTERVAL %s
#         WHERE user_id = %s;
#     """
#     exec_commit(sql, (duration, user_id))


# def lift_suspension(user_id):
#     sql = """
#         UPDATE message_user
#         SET is_suspended = FALSE,
#             suspension_end = NULL
#         WHERE user_id = %s;
#     """
#     exec_commit(sql, (user_id,))


# def send_message(sender_id, receiver_id, content):
#     sql = """
#         INSERT INTO messages (sender_id, receiver_id, sent_at, is_read, content)
#         VALUES (%s, %s, NOW(), FALSE, %s);
#     """
#     exec_commit(sql, (sender_id, receiver_id, content))


# def get_unread_message_count(user_id):
#     sql = """
#         SELECT COUNT(*)
#         FROM messages
#         WHERE receiver_id = %s AND is_read = FALSE;
#     """
#     count = exec_get_one(sql, (user_id,))
#     return count[0] if count else 0


# def get_conversation_between_users(user_id1, user_id2):
#     sql = """
#         SELECT sender_id, receiver_id, sent_at, content, is_read
#         FROM messages
#         WHERE (sender_id = %s AND receiver_id = %s) OR (sender_id = %s AND receiver_id = %s)
#         ORDER BY sent_at ASC;
#     """
#     return exec_get_all(sql, (user_id1, user_id2, user_id2, user_id1))




# def get_users_with_unread_messages(user_id):
#     sql = """
#         SELECT sender_id, COUNT(*) AS unread_count
#         FROM messages
#         WHERE receiver_id = %s AND is_read = FALSE
#         GROUP BY sender_id;
#     """
#     return exec_get_all(sql, (user_id,))


# def mark_message_as_read(sender_id, receiver_id, sent_at):
#     sql = """
#         UPDATE messages
#         SET is_read = TRUE
#         WHERE sender_id = %s AND receiver_id = %s AND sent_at = %s;
#     """
#     exec_commit(sql, (sender_id, receiver_id, sent_at))


# def change_username(user_id, new_username):
#     if can_change_username(user_id):
#         sql = """
#             UPDATE message_user
#             SET username = %s, last_username_change = NOW()
#             WHERE user_id = %s;
#         """
#         exec_commit(sql, (new_username, user_id))
#     else:
#         raise Exception("Username change is not allowed within six months of the last change.")


# def can_change_username(user_id):
#     sql = """
#         SELECT last_username_change
#         FROM message_user
#         WHERE user_id = %s;
#     """
#     last_change = exec_get_one(sql, (user_id,))
#     if last_change:
#         last_change_time = last_change[0]
#         six_months_ago = datetime.datetime.now() - datetime.timedelta(days=180)
#         return last_change_time < six_months_ago
#     return True


# def get_all_messages_count():
#     select_sql = """
#         SELECT COUNT(*) FROM messages;
#     """
#     result = exec_get_one(select_sql)
#     return result

