# coding: utf-8

from __future__ import unicode_literals, print_function

import os
import random
import sendgrid
import yaml
from itertools import zip_longest
from datetime import datetime


class CodePairs(object):

    COPY = """
    Your new code review buddy for the next two weeks has been chosen! Buddy <b>{}</b> and buddy <b>{}</b>, go forth and embark on an epic
    journey together!

    {}
    
    P.S. Remember to schedule some time to catch up with your buddy(s).
    """

    TROLL_COPY = """
    Your journey also includes the rare, but equally awesome, troll: <b>{}</b>

    Note: the troll is necessary for when we have an odd number of developers and need to have a group of 3.
    """

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
    def sg_client(self):
        return sendgrid.SendGridClient(self.sg_config['sg']['username'], self.sg_config['sg']['password'])

    @property
    def sg_from(self):
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
        no_pair = map(lambda p: p[0] or p[1], filter(lambda p: not p[0] or not p[1], zipped))
        pairs = filter(lambda p: p[0] and p[1], zipped)

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
        for pair in pairs:
            is_trio = len(pair) == 3
            message = sendgrid.Mail()
            message.add_to(map(lambda username: "{}@{}.com".format(username, 'dimagi'), pair))

            subject = 'Your code review {}: {}'.format(
                'duo' if not is_trio else 'trio',
                ', '.join(pair)
            )

            if is_trio:
                troll_copy = self.TROLL_COPY.format(pair[2])
            else:
                troll_copy = ''

            message.set_subject(subject)
            message.set_html(self.COPY.format(pair[1], pair[0], troll_copy))
            message.set_text(self.COPY.format(pair[1], pair[0], troll_copy))
            message.set_from(self.sg_from)
            status, msg = self.sg_client.send(message)
            print(status)
            print(msg)
