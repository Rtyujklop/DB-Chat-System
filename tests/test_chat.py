import unittest
from src.chat import *
from src.chat import *
from src.swen344_db_utils import *


class TestChat(unittest.TestCase):


    def test_setUp(self):
        rebuildTables()
       
    def test_1(self):
        rebuildTables()
        messages = get_messages_between_users_1(1, 2)
        # print(messages)
        self.assertGreater(len(messages), 0, "There should be messages between Abbott and Costello")
        #checks for messages bewteen users but there aren't any

    def test_2(self):
        rebuildTables()
        messages = get_messages_between_users_1(3, 4)
        filtered = [msg for msg in messages if msg[4].year == 1995]
        self.assertGreater(len(filtered), 0, "There should be messages between Moe and Larry in 1995")
        # there are messages bewteen users

    def test_3(self):
        rebuildTables()
        unread_count = get_unread_message_count(1)
        self.assertEqual(unread_count[0], 1, "Abbott should have 1 unread message")
        #there is an unread messages

    def test_4(self):
        rebuildTables()
        suspension_status = get_suspension_status(4, '2012-05-04')
        self.assertIsNotNone(suspension_status, "Larry should be suspended on May 4, 2012")
        # checks suspension status

    def test_5(self):
        rebuildTables()
        suspension_status = get_suspension_status(5, '2000-02-29')
        self.assertIsNone(suspension_status, "Curly should not be suspended on February 29, 2000")
        # user should not be suspended

    def test_6(self):
        rebuildTables()
        create_user('Bob', 'bob@gmail.com')
        self.dr_marvin_id = get_user_id("DrMarvin")
        self.bob_id = get_user_id("Bob")
        self.dr_marvin_id = get_user_id("DrMarvin")
        send_message_1(self.bob_id, self.dr_marvin_id, "I'm doing the work, I'm baby-stepping", 1, 2)
        messages = get_messages_between_users_2(self.dr_marvin_id, self.bob_id)
        self.assertEqual(len(messages), 1, "DrMarvin should have one message from Bob.")
        self.assertEqual(messages[0]['message'], "I'm doing the work, I'm baby-stepping", "The message content should match.")
        self.assertTrue(messages[0]['is_unread'], "The message should be marked as unread.")
        # make a mess_channel to connect messages and channel
       
    def test_7(self):
        rebuildTables()
        create_user('Bob', 'bob@gmail.com')
        self.bob_id = get_user_id("Bob")
        update_last_username_change("Bob", datetime(1991, 5, 16))
        change_username(self.bob_id, "BabySteps2Door")
        self.assertEqual(get_user_id("BabySteps2Door"), self.bob_id, "Username should be updated.")
        with self.assertRaises(Exception) as context:
            change_username(self.bob_id, "BabySteps2Elevator")
        self.assertEqual(str(context.exception), "You cannot change your username again yet.", "Should raise an exception indicating the six-month rule violation.")
        # username changes but makes sure you can only do it once

    def test_8(self):
        rebuildTables()
        create_user('Bob', 'bob@gmail.com')
        self.dr_marvin_id = get_user_id("DrMarvin")
        self.bob_id = get_user_id("Bob")
        update_last_username_change("Bob", datetime(1991, 5, 16))
        change_username(self.bob_id, "BabySteps2Door")
        send_message_1(self.bob_id, self.dr_marvin_id, "Hey DrMarvin", 1, 2)
        messages = get_messages_between_users_1(self.dr_marvin_id, self.bob_id)
        message_id = messages[0][0]
        mark_message_as_read(message_id)
        messages = get_messages_between_users_1(self.dr_marvin_id, self.bob_id)
        self.assertFalse(messages[0][5], "The message should be marked as read.")
        #user change username and then checks bewteen users if message is read

    def test_9(self):
        rebuildTables()
        self.moe_id = get_user_id("Moe")
        self.larry_id = get_user_id("Larry")
        with self.assertRaises(Exception) as context:
            send_message_1(self.larry_id, self.moe_id, "Hey Moe", 1, 2)
        self.assertIn("suspended until", str(context.exception).lower(), "Should show suspension end message.")
        clear_suspension(self.larry_id)
        send_message_1(self.larry_id, self.moe_id, "Message after unsuspend", 1, 2)
        messages = get_messages_between_users_1(self.moe_id, self.larry_id)
        self.assertEqual(len(messages), 3, "Larry's message should be sent successfully after unsuspension.")
        self.assertEqual(messages[2][3], "Message after unsuspend", "The content of the message should match.")
        # message is sent succussful after clearing suspension

    def test_10(self):
        rebuildTables()
        csv_file_path = "src/whos_on_first.csv"
        import_chat_data(csv_file_path)
        abbott_id = get_user_id("Abbott")
        costello_id = get_user_id("Costello")
        all_messages = get_all_messages()
        self.assertGreater(len(all_messages), 0, "There should be messages in the Messages table")
        messages = get_messages_between_users_1(abbott_id, costello_id)
        for message in messages:
            self.assertTrue(message[4], "All messages should be marked as unread")
        #reads and adds messages form Abbott and Costello from csv
    def test_11(self):
        rebuildTables()
        create_user('Paul', 'paul@example.com')
        create_user('SpiceLover', 'spicelover@gmail.com')
        self.paul_id = get_user_id('Paul')
        self.spice_lover_id = get_user_id('SpiceLover')
        self.moe_id = get_user_id('Moe')
        self.assertIsNotNone(self.paul_id, "User Paul was not created")

        # Paul joins Arrakis community
        self.arrakis_id = exec_get_one("SELECT id FROM Communities WHERE name = 'Arrakis';")
        join_channel(self.paul_id, self.arrakis_id, self.arrakis_id)
        self.membership = exec_get_one("SELECT * FROM Memberships WHERE user_id = %s AND community_id = %s;", [self.paul_id, self.arrakis_id])
        self.assertIsNotNone(self.membership, "Paul did not join the Arrakis community")

        # Paul sends message in Arrakis
        send_message_2(sender_id=self.paul_id, receiver_id='SpiceLover', message="Hello everyone!", community_id=self.arrakis_id, channel_name='Worms')
        self.message_1 = exec_get_one("SELECT * FROM Messages WHERE sender_id = %s AND message = 'Hello everyone!';", [self.paul_id])
        self.assertIsNotNone(self.message_1, "Message was not sent by Paul")

        # Unread message count for SpiceLover
        self.unread_count = get_unread_message_count(self.spice_lover_id)
        self.assertEqual(self.unread_count[0], 1, "Unread message count for SpiceLover should be 1")

        # Paul mentions SpiceLover in Arrakis
        send_message_2(sender_id=self.paul_id, receiver_id='SpiceLover', message="Hey @spicelover, check this out!", community_id=self.arrakis_id, channel_name='Worms')
        self.mentions = exec_get_all("SELECT * FROM Messages WHERE message LIKE %s;", ['%@spicelover%'])
        self.assertGreater(len(self.mentions), 0, "There should be messages mentioning @spicelover")
        self.assertIn("Hey @spicelover, check this out!", [m[3] for m in self.mentions], "The message should be present in the mentions")

        # Moe joins Comedy community
        self.comedy_id = exec_get_one("SELECT id FROM Communities WHERE name = 'Comedy';")
        join_channel(self.moe_id, self.comedy_id, self.comedy_id)

        # Moe sends message mentioning SpiceLover in Comedy (SpiceLover won't receive this mention)
        send_message_2(sender_id=self.moe_id, receiver_id='SpiceLover', message="Hey @spicelover, this is a test!", community_id=self.comedy_id, channel_name='Comedy')
        self.mentions_comedy = exec_get_all("SELECT * FROM Messages WHERE message LIKE %s AND sender_id != %s;", ['%@spicelover%', self.moe_id])
        self.assertEqual(len(self.mentions_comedy), 1, "Moe's mention of @spicelover in Comedy should not be received by SpiceLover")

        # Paul suspended in Arrakis
        suspend_user(self.paul_id, '2025-01-01')
        with self.assertRaises(Exception) as context:
            send_message_2(sender_id=self.paul_id, receiver_id='SpiceLover', message="Hey @spicelover, Hello from Arrakis!", community_id=self.arrakis_id, channel_name='Worms')
        self.assertIn("User is suspended until", str(context.exception), "Paul should not be able to send a message while suspended in Arrakis")

        # Clear Paul's suspension
        clear_suspension(self.paul_id)
        # Paul joins Comedy community
        join_channel(self.paul_id, self.comedy_id, self.comedy_id)

        # Paul sends message to Moe in Comedy (should succeed)
        send_message_2(sender_id=self.paul_id, receiver_id='Moe', message="Hello Moe!", community_id=self.comedy_id, channel_name='Comedy')
        # print(send_message_2)
        # send_message_1(sender_id=self.paul_id, receiver_id=self.moe_id, message= "hey")
        # send_message_1(sender_id=self.moe_id, receiver_id=self.paul_id, message= "hey")
        self.message_count = get_messages_between_users_1(self.paul_id, self.moe_id)
        self.assertGreater(len(self.message_count), 0, "There should be messages between Paul and Moe")
        #tests leave community
        leave_community(self.paul_id, self.arrakis_id)
        self.membership_after_leave = exec_get_one("SELECT * FROM Memberships WHERE user_id = %s AND community_id = %s;", [self.paul_id, self.arrakis_id])
        self.assertIsNone(self.membership_after_leave, "Paul should have left the Arrakis community")


    def test_setup_data(self):
        rebuildTables()
        create_user('Paul', 'paul@example.com')
        create_user('SpiceLover', 'spicelover@gmail.com')
        self.paul_id = get_user_id('Paul')
        self.spice_lover_id = get_user_id('SpiceLover')
        # exec_commit("INSERT INTO Communities (name) VALUES ('Arrakis')")
        # exec_commit("INSERT INTO Communities (name) VALUES ('Comedy')")
        self.arrakis_id = exec_get_one("SELECT id FROM Communities WHERE name = 'Arrakis';")[0]
        self.comedy_id = exec_get_one("SELECT id FROM Communities WHERE name = 'Comedy';")[0]
        # exec_commit("INSERT INTO Channels (name, community_id) VALUES ('Worms', %s)", [self.arrakis_id])
        # exec_commit("INSERT INTO Channels (name, community_id) VALUES ('Laughter', %s)", [self.comedy_id])
        join_channel(self.paul_id, self.arrakis_id, self.arrakis_id)
        join_channel(self.spice_lover_id, self.arrakis_id, self.arrakis_id)
        send_message_3(self.paul_id, self.spice_lover_id, "please reply", self.arrakis_id, "Worms")
        send_message_3(self.spice_lover_id, self.paul_id, "i replied already!", self.arrakis_id, "Worms")
        suspend_user(self.paul_id, '2025-01-01')


    def test_12(self):
        rebuildTables()
        self.test_setup_data()
        results = search_messages(self.arrakis_id, "reply")
        self.assertEqual(len(results), 2, "Search should return two messages containing 'reply'.")
        results = search_messages(self.arrakis_id, "reply please")
        self.assertEqual(len(results), 1, "Search should return only one message with both 'reply' and 'please'.")


    def test_13(self):
        rebuildTables()
        self.test_setup_data()
        results = get_suspended_users(datetime(2024, 1, 1), datetime(2025, 12, 31))
        self.assertIn('Paul', results, "Paul should be listed as a suspended user in the Arrakis community.")


    def test_14(self):
        rebuildTables()
        self.test_setup_data()
        summary = activity_summary()
        arrakis_summary = next((s for s in summary if s['community'] == 'Arrakis'), None)
        self.assertIsNotNone(arrakis_summary, "Arrakis community should have an activity summary.")
        self.assertGreater(arrakis_summary['avg_num_messages'], 0, "Average number of messages for Arrakis should be greater than 0.")
        self.assertGreater(arrakis_summary['active_users'], 0, "Number of active users for Arrakis should be greater than 0.")


    # def test_search_messages(self):
    #     rebuildTables()
    #     query = "reply"
    #     community_id = exec_get_one("SELECT id FROM Communities WHERE name = 'Arrakis';")[0]
    #     results = search_messages(query, community_id)
    #     print(results)
    #     self.assertEqual(len(results), 2, "Two messages should match the search query")
    #     self.assertEqual(results[0][3], "please reply", "First message should match")
    #     self.assertEqual(results[1][3], "i replied already!", "Second message should match")
    #fixing this
    # def test_search_messages_multiple_terms(self):
    #     rebuildTables()
    #     query = "reply please"
    #     community_id = exec_get_one("SELECT id FROM Communities WHERE name = 'Arrakis';")[0]
    #     results = search_messages(query, community_id)
    #     self.assertEqual(len(results), 1, "One message should match the search query")
    #     self.assertEqual(results[0][3], "please reply", "Message should match")

    # def test_moderator_query(self):
    #     rebuildTables()
    #     start_date = "2022-01-01"
    #     end_date = "2022-12-31"
    #     suspended_users = moderator_query(start_date, end_date)
    #     self.assertIn("Paul", suspended_users, "Paul should be listed as suspended")

    # def test_activity_summary(self):
    #     rebuildTables()
    #     date = "2022-06-15"
    #     community_id = exec_get_one("SELECT id FROM Communities WHERE name = 'Arrakis';")[0]
    #     summary = activity_summary(date, community_id)
    #     self.assertIsInstance(summary, dict, "Summary should be a dictionary")
    #     self.assertIn('community', summary, "Summary should contain community name")
    #     self.assertIn('avg_num_messages', summary, "Summary should contain average messages")
    #     self.assertIn('active_users', summary, "Summary should contain active users")


if __name__ == '__main__':
    unittest.main()



