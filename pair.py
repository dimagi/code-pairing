# coding: utf-8

import os
import random
from itertools import zip_longest

import yaml
from python_http_client import HTTPError

from email_utils import build_email_from_usernames, get_email_client


class ConfigParser(object):

    def __init__(self, config_path=None):
        self.config_path = config_path or os.path.join(os.path.dirname(__file__), 'config.yml')
        self.config = self.load_config()

    def load_config(self):
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f.read())

    @property
    def group_one(self):
        return self.config['group_one'] if 'group_one' in self.config else []

    @property
    def group_two(self):
        return self.config['group_two'] if 'group_two' in self.config else []


def generate_pairs(group_one, group_two=None):
    """

    :param group_one:
    :param group_two: optional to enable generating pairs across groups
    :return:
    """
    assert group_one, "group_one is empty"
    group_two = group_two if group_two else []
    assert len(group_one) + len(group_two) > 1, "Total must be larger than 1 item"
    
    random.shuffle(group_one)
    random.shuffle(group_two)

    zipped = list(zip_longest(group_one, group_two))
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
