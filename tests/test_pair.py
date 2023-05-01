import random
from unittest import TestCase

from pair import ConfigParser, generate_pairs


class GeneratePairsTests(TestCase):

    def test_even_groups_with_even_total(self):
        pairs = generate_pairs(['roger', 'rafa'], ['novak', 'andy'])
        self.assertEqual(
            pairs,
            [('rafa', 'novak'), ('roger', 'andy')]
        )

    def test_uneven_groups_with_even_total(self):
        pairs = generate_pairs(['holger', 'casper'],
                               ['andrei', 'hubert', 'frances', 'daniil'])
        self.assertEqual(
            pairs,
            [('casper', 'hubert'), ('holger', 'frances'), ('andrei', 'daniil')]
        )

    def test_uneven_groups_with_odd_total(self):
        pairs = generate_pairs(['stan', 'cameron', 'jannik'],
                               ['stefanos', 'diego'])
        self.assertEqual(
            pairs,
            [('stan', 'diego'), ('jannik', 'stefanos', 'cameron')]
        )

    def test_empty_second_list(self):
        pairs = generate_pairs(['taylor', 'jj', 'dennis', 'felix'])
        self.assertEqual(
            pairs,
            [('dennis', 'felix'), ('jj', 'taylor')]
        )

    def test_assertion_error_if_first_list_is_empty(self):
        with self.assertRaises(AssertionError):
            generate_pairs([])

    def test_assertion_error_if_total_size_is_less_than_two(self):
        with self.assertRaises(AssertionError):
            generate_pairs(['john'], [])

    @classmethod
    def setUpClass(cls):
        random.seed(5)  # set to some constant for consistent results


class ConfigParserTests(TestCase):

    def test_parses_list_one_with_no_list_two(self):
        parser = ConfigParser(config_path='tests/configs/list_one.yml')
        self.assertEqual(parser.list_one, ['roger', 'rafa', 'novak'])
        self.assertEqual(parser.list_two, [])

    def test_parses_list_one_and_list_two(self):
        parser = ConfigParser(config_path='tests/configs/both_lists.yml')
        self.assertEqual(parser.list_one, ['holger', 'casper'])
        self.assertEqual(parser.list_two, ['andrei', 'hubert'])
