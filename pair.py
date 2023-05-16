# coding: utf-8

import os
import random
from itertools import zip_longest

import yaml
from python_http_client import HTTPError

from email_utils import build_email_from_usernames, get_email_client


class ConfigParser(object):
    """
    Expects an input yaml file as follows:
    At a minimum, a value of ``group_one`` must be defined

    group_one:
      - first
      - second
      - ...

    Optionally, you can include a second group to create pairs between group_one
    and group_two, defined as the value ``group_two``:

    group_one:
      - first
      - second
      - ...

    group_two:
      - third
      - fourth
      - ...
    """

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
    :param group_one: required list of items to generate pairs with
    :param group_two: optional to enable generating pairs across groups
    :return:
    """
    assert group_one, "group_one is empty"
    group_two = group_two if group_two else []
    assert len(group_one) + len(group_two) > 1, "Total must be larger than 1 item"
    
    random.shuffle(group_one)
    random.shuffle(group_two)

    zipped = list(zip_longest(group_one, group_two))
    # extract values from incomplete pairs (<value>, None) or (None, <value>)
    no_pair = list(map(lambda p: p[0] or p[1], filter(lambda p: not p[0] or not p[1], zipped)))
    pairs = list(filter(lambda p: p[0] and p[1], zipped))

    # Handle the values missing pairs (called a "troll")
    while no_pair:
        troll = no_pair.pop()
        if no_pair:
            another_troll = no_pair.pop()
            pairs.append((troll, another_troll))
        else:
            random_pair_index = random.randint(0, len(pairs) - 1)
            pairs[random_pair_index] = pairs[random_pair_index] + (troll, )

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
