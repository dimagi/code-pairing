# coding: utf-8

import os
import random
import yaml
from itertools import zip_longest

from email_utils import build_email_from_usernames, get_email_client


class CodePairs(object):

    def __init__(self, config_path=None, sg_path=None):
        self.config_path = config_path or os.path.join(os.path.dirname(__file__), 'config.yml')
        self.sg_path = sg_path or os.path.join(os.path.dirname(__file__), 'sg.yml')

        self.config = self.load_config()
        self.sg_config = self.load_sg()

    def load_config(self):
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f.read())

    def load_sg(self):
        with open(self.sg_path, 'r') as f:
            return yaml.safe_load(f.read())

    @property
    def email_client(self):
        return get_email_client(self.sg_config['sg']['api_key'])

    @property
    def email_sender(self):
        return self.sg_config['sg']['from']

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
        print(pairs)
        for usernames in pairs:
            message = build_email_from_usernames(self.email_sender, usernames)
            status, msg = self.email_client.send(message)
            print(status)
            print(msg)
