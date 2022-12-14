from unittest import TestCase

from pair import CodePairs


class GeneratePairsTests(TestCase):

    def test_even_groups_with_even_total(self):
        cp = CodePairs(config_path='tests/configs/even_groups.yml')
        pairs = cp._generate_pairs()
        self.assertEqual(len(pairs), 2)

    def test_uneven_groups_with_even_total(self):
        cp = CodePairs(config_path='tests/configs/uneven_groups_even_total.yml')
        pairs = cp._generate_pairs()
        self.assertEqual(len(pairs), 3)

    def test_uneven_groups_with_odd_total(self):
        cp = CodePairs(config_path='tests/configs/uneven_groups_odd_total.yml')
        pairs = cp._generate_pairs()
        self.assertEqual(len(pairs), 2)
        self.assertTrue(any([len(p) == 3 for p in pairs]))
