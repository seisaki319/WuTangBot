'''
Adapted from HaikuBot
'''

import config
import markovify
# import twitter
import sylco
import threading
import rhymer
import os
from string import punctuation
from random import randint

class Songwriter(object):
    def __init__(self):
        self.config = config.Config()
        self.rhymer = rhymer.Rhymer()
        # self.api = twitter.Api(
        #     consumer_key=self.config.twitter_consumer_key,
        #     consumer_secret=self.config.twitter_consumer_secret,
        #     access_token_key=self.config.twitter_access_token_key,
        #     access_token_secret=self.config.twitter_access_token_secret
        # )

    '''
    Begin looping haiku generation and Twitter posts
    '''
    def start(self):
        song = self.generate_song()
        # self.api.PostUpdate(haiku)
        threading.Timer(self.config.generation_frequency, self.start).start()

    '''
    1. Create a Markovify text model from all inputs
    2. Generate a random text snippet using markov chains
    3. Proceed if syllable count is correct, otherwise go to (2)
    4. Concat all haiku lines
    '''
    def generate_song(self, input_string, linecount):
        last_word = input_string.split(' ')[-1]
        def syl_thresh_check(actual, target):
            return abs(actual - target) > self.config.syl_diff_threshold 
        target_syls = sylco.getsyls(input_string)
        all_text = "";
        rhymes = self.rhymer.rhyme(last_word) 
        for i in os.listdir(self.config.markovify_input_dir):
            with open(self.config.markovify_input_dir + i) as f:
                all_text += f.read()
        text_model = markovify.NewlineText(all_text)
        lines = [input_string]
        for i in range(linecount):
            count, line = 0, None
            while not line or syl_thresh_check(sylco.getsyls(line), target_syls) or line.split(' ')[-1].lower() not in rhymes:
                line = text_model.make_short_sentence(
                    2 * len(input_string),
                    min_chars = .75 * len(input_string),
                    tries=10,
                    max_overlap_ratio=self.config.markovify_max_overlap_ratio,
                    max_overlap_total=self.config.markovify_max_overlap_total
                )
                count += 1
                if line:
                    line = line.translate(str.maketrans("", "", punctuation))
                # print(line)
            lines.append(line)
        song = "\n".join(lines)

        print("")
        print("***********************")
        print("-----------------------")
        print(song)
        print("-----------------------")
        print("***********************")
        print(sylco.getsyls(line))
        return song