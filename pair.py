# coding: utf-8

import os
import random
from itertools import zip_longest

import yaml
from python_http_client import HTTPError

from email_utils import build_email_from_usernames, get_email_client


class CodePairs(object):

    def __init__(self, config_path=None):
        self.config_path = config_path or os.path.join(os.path.dirname(__file__), 'config.yml')
        self.config = self.load_config()

    def load_config(self):
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f.read())

    @property
    def email_client(self):
        return get_email_client(os.environ['SENDGRID_API_KEY'])

    @property
    def email_sender(self):
        return os.environ['FROM_EMAIL']

    @property
    def hobbits(self):
        return self.config['hobbits']

    @property
    def enchantresses(self):
        return self.config['enchantresses']

    def _generate_pairs(self):
        random.shuffle(self.hobbits)
        random.shuffle(self.enchantresses)

        zipped = list(zip_longest(self.hobbits, self.enchantresses))
        no_pair = list(map(lambda p: p[0] or p[1], filter(lambda p: not p[0] or not p[1], zipped)))
        pairs = list(filter(lambda p: p[0] and p[1], zipped))

        # Handle the odd numbers
        one = two = None
        while True:
            try:
                one = no_pair.pop()
            except IndexError:
                break

            try:
                two = no_pair.pop()
            except IndexError:
                # Take care of the troll
                group_idx = random.randint(0, len(pairs) - 1)
                pairs[group_idx] = (pairs[group_idx][0], pairs[group_idx][1], one)
                break
            else:
                pairs.append((one, two))

        return pairs

    def email_pairs(self):
        pairs = self._generate_pairs()
        for usernames in pairs:
            message = build_email_from_usernames(self.email_sender, usernames)
            try:
                response = self.email_client.send(message)
            except HTTPError as e:
                print(e)
            print(f"Request received with response: {response.status_code}\n{response.body}")


def generate_pairs(list_one, list_two=None):
    """

    :param list_one:
    :param list_two: optional list to allow generating pairs between two
    different groups
    :return:
    """
    assert list_one, "list_one is empty"
    list_two = list_two if list_two else []
    assert len(list_one) + len(list_two) > 1, "Total must be larger than 1 item"
    
    random.shuffle(list_one)
    random.shuffle(list_two)

    zipped = list(zip_longest(list_one, list_two))
    no_pair = list(
        map(lambda p: p[0] or p[1], filter(lambda p: not p[0] or not p[1], zipped)))
    pairs = list(filter(lambda p: p[0] and p[1], zipped))

    # Handle the odd numbers
    one = two = None
    while True:
        try:
            one = no_pair.pop()
        except IndexError:
            break

        try:
            two = no_pair.pop()
        except IndexError:
            # Take care of the troll
            group_idx = random.randint(0, len(pairs) - 1)
            pairs[group_idx] = (pairs[group_idx][0], pairs[group_idx][1], one)
            break
        else:
            pairs.append((one, two))

    return pairs


def send_email(pairs):
    sender = os.environ.get('FROM_EMAIL')
    client = get_email_client(os.environ.get('SENDGRID_API_KEY'))

    for usernames in pairs:
        message = build_email_from_usernames(sender, usernames)
        try:
            response = client.send(message)
        except HTTPError as e:
            print(e)
        print(
            f"Request received with response: {response.status_code}\n{response.body}")
