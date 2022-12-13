from unittest import TestCase

from email_utils import build_email_from_usernames


class SendgridTests(TestCase):

    def test_email_for_pair_succeeds(self):
        usernames = ('user', 'user2')
        build_email_from_usernames('sender', usernames)  # should not raise

    def test_email_for_trio_succeeds(self):
        usernames = ('user', 'user2', 'user3')
        build_email_from_usernames('sender', usernames)  # should not raise


