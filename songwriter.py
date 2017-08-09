'''
Adapted from HaikuBot
'''
from . import sylco, config, rhymer, model_io
# import twitter
import markovify
import threading, time
import os, sys
from string import punctuation
from random import randint

class Songwriter(object):
    def __init__(self, modelname):
        self.config = config.Config()
        self.rhymer = rhymer.Rhymer()
        self.text_model = model_io.read_model(modelname)
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
        input_string = input("Input your phrase!")
        self.generate_song(input_string, 15, rhymelevel = 2)
        # self.api.PostUpdate(haiku)
        threading.Timer(self.config.generation_frequency, self.start).start()

    '''
    1. Create a Markovify text model from all inputs
    2. Generate a random text snippet using markov chains
    3. Proceed if syllable count is correct, otherwise go to (2)
    4. Concat all haiku lines
    '''
    def generate_song(self, input_string, linecount, rhymelevel = 9000):
        start = time.time()
        last_word = input_string.split(' ')[-1]
        def syl_thresh_check(actual, target):
            return abs(actual - target) > self.config.syl_diff_threshold
        target_syls = sylco.getsyls(input_string)
        rhymes = self.rhymer.rhyme(last_word, rhymelevel)
        lines = [input_string]
        last = start
        for i in range(linecount):
            line = None
            while not line or syl_thresh_check(sylco.getsyls(line), target_syls) or line.split(' ')[-1].lower().translate(str.maketrans("", "", punctuation)) not in rhymes:
                line = self.text_model.make_short_sentence(
                    2 * len(input_string),
                    min_chars = len(input_string) / 2,
                    tries=10,
                    max_overlap_ratio=self.config.markovify_max_overlap_ratio,
                    max_words = target_syls
                    # max_overlap_total=self.config.markovify_max_overlap_total
                )
                if time.time() - last > 5:
                    last = time.time()
                    if self.config.syl_diff_threshold <= 3: self.config.syl_diff_threshold += 1
                    if self.config.markovify_max_overlap_ratio > .6: self.config.markovify_max_overlap_ratio *= .95
                    print('Adjust: {0}, {1}'.format(self.config.syl_diff_threshold, self.config.markovify_max_overlap_ratio))
                    sys.stdout.flush()
                    if self.config.markovify_max_overlap_ratio <= .6:
                        self.config.markovify_max_overlap_ratio = .9
                        self.config.syl_diff_threshold = 0
                        return "Couldn't find a rhyme.\nSo far:\n" + "\n".join(lines)
            lines.append(line)
            last = time.time()
            print('Found line {0} at {1} secs.'.format(i + 1, last - start))
            sys.stdout.flush()
            self.config.syl_diff_threshold = 0
            self.config.markovify_max_overlap_ratio = .9
        song = "\n".join(lines)
        print("***********************")
        print("-----------------------")
        print(song)
        print("-----------------------")
        print("***********************")
        end = time.time()
        print("Generation took {0} secs.".format(end - start))
        sys.stdout.flush()
        return song
