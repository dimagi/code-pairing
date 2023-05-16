from unittest import TestCase

from email_utils import (_get_recipients_from_usernames,
                         build_email_from_usernames)


class SendgridTests(TestCase):

    def test_email_for_pair_succeeds(self):
        usernames = ['user', 'user2']
        message = build_email_from_usernames('sender', usernames)
        self.assertIsNotNone(message.get())

    def test_email_for_trio_succeeds(self):
        usernames = ['user', 'user2', 'user3']
        message = build_email_from_usernames('sender', usernames)
        self.assertIsNotNone(message.get())

    def test_recipients_is_correct(self):
        usernames = ['user', 'user2']
        message = build_email_from_usernames('sender', usernames)
        msg_json = message.get()
        recipients = [p['email'] for p in msg_json['personalizations'][0]['to']]
        self.assertEqual(recipients, ['user@dimagi.com', 'user2@dimagi.com'])

    # test _get_recipients_from_username
    
    def test_email_with_period(self):
        emails = _get_recipients_from_usernames(['user.test'])
        self.assertEqual(emails, ['user.test@dimagi.com'])
