from unittest import TestCase

from email_utils import build_email_from_usernames


class SendgridTests(TestCase):

    def test_email_for_pair_succeeds(self):
        user_infos = [
            {'name': 'User', 'email': 'user@dimagi.com',
             'preference': 'sync'},
            {'name': 'User2', 'email': 'user2@dimagi.com',
             'preference': 'async'}]
        message = build_email_from_usernames('sender', user_infos)
        self.assertIsNotNone(message.get())

    def test_email_for_trio_succeeds(self):
        user_infos = [
            {'name': 'User', 'email': 'user@dimagi.com',
             'preference': 'sync'},
            {'name': 'User2', 'email': 'user2@dimagi.com',
             'preference': 'async'},
            {'name': 'User3', 'email': 'user3@dimagi.com',
             'preference': 'async'}
        ]
        message = build_email_from_usernames('sender', user_infos)
        self.assertIsNotNone(message.get())

    def test_recipients_is_correct(self):
        user_infos = [
            {'name': 'User', 'email': 'user@dimagi.com',
             'preference': 'sync'},
            {'name': 'User2', 'email': 'user2@dimagi.com',
             'preference': 'async'}]
        message = build_email_from_usernames('sender', user_infos)
        msg_json = message.get()
        recipients = [p['email'] for p in msg_json['personalizations'][0]['to']]
        self.assertEqual(recipients, ['user@dimagi.com', 'user2@dimagi.com'])
