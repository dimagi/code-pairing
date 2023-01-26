#!/usr/bin/env python
# coding: utf-8
from pair import CodePairs
from utils import should_generate_new_pairs

if __name__ == '__main__':
    if should_generate_new_pairs():
        cp = CodePairs()
        cp.email_pairs()
