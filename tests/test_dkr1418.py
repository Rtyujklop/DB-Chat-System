# import unittest
# from src.chat import *
# from src.dkr1418 import rebuildTables
# from src.swen344_db_utils import connect, exec_get_all

# class TestChat(unittest.TestCase):

#     def test_rebuildTables(self):
#         """Build the tables"""
#         rebuildTables()
#         result = exec_get_all('SELECT * FROM messages')
#         expected = [(1, 1996, 'read', 'Curly')]
#         self.assertEqual([(1, 1996, 'read', 'Curly')], expected, "no rows in messages")

#     def test_rebuild_tables_is_idempotent(self):
#       """Drop and rebuild the tables twice"""
#       rebuildTables()
#       rebuildTables()
#       result = exec_get_all('SELECT * FROM messages')
#       expected = [(1, 1996, 'read', 'Curly')]
#       self.assertEqual([(1, 1996, 'read', 'Curly')], expected, "no rows in messages")