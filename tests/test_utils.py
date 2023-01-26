from datetime import datetime
from unittest import TestCase, mock

from freezegun import freeze_time

from utils import should_generate_new_pairs


class ShouldGenerateNewPairsTests(TestCase):

    @freeze_time('2023-01-08')
    def test_returns_true_when_update_interval_is_one_week_and_current_time_is_seven_days_after_ref_date(self):
        with (mock.patch('utils.UPDATE_INTERVAL', 7),
              mock.patch('utils.REFERENCE_DATE', datetime(2023, 1, 1))):
            self.assertTrue(should_generate_new_pairs())

    @freeze_time('2023-01-07')
    def test_returns_false_when_update_interval_is_one_week_and_current_time_is_six_days_after_ref_date(self):
        with (mock.patch('utils.UPDATE_INTERVAL', 7),
              mock.patch('utils.REFERENCE_DATE', datetime(2023, 1, 1))):
            self.assertFalse(should_generate_new_pairs())

    @freeze_time('2023-01-09')
    def test_returns_false_when_update_interval_is_one_week_and_current_time_is_eight_days_after_ref_date(self):
        with (mock.patch('utils.UPDATE_INTERVAL', 7),
              mock.patch('utils.REFERENCE_DATE', datetime(2023, 1, 1))):
            self.assertFalse(should_generate_new_pairs())
