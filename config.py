'''
MIT License Copyright(c) 2016 Balys Valentukevicius

Configuration for Twitter client and Haiku generator
'''

import os

class Config(object):
    def __init__(self):
        # Genius
        self.genius_api_key = "xxxxxx"
        # Twitter
        self.twitter_consumer_key="xxxxxxxx"
        self.twitter_consumer_secret="xxxxxxxx"
        self.twitter_access_token_key="xxxxxxxx"
        self.twitter_access_token_secret="xxxxxxxx"

        # Markovify
        self.markovify_input_dir = "./input/"
        self.markovify_max_overlap_total = 25
        self.markovify_max_overlap_ratio = 0.9

        # Haiku
        self.syl_diff_threshold = 0


        self.generation_frequency = 1
