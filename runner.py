#!/usr/bin/env python
# coding: utf-8
from pair import ConfigParser, generate_pairs, send_email

if __name__ == '__main__':
    parser = ConfigParser()
    pairs = generate_pairs(parser.list_one, parser.list_two)
    print(pairs)
    send_email(pairs)
