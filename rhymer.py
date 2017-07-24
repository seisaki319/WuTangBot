import nltk, pronouncing

class Rhymer(object):
	VOWELS = ['AA', 'AH', 'AW', 'AH', 'AO', 'AY', 'EH','ER', 'EY', 'IY', 'OY', 'OW', 'UW', 'UH']
	def rhyme(self, inp, level, exact = False):
		inp = inp.lower()
		entries = nltk.corpus.cmudict.entries()
		syllables = [(word, syl) for word, syl in entries if word == inp]
		strip_stress = lambda syl: [s[0:2] for s in syl if len(s) > 2]
		strip = lambda syl: [s for s in syl if len(s) > 2]
		rhyme_check = lambda test, syl, f: all([len(f(test)) >= i and f(test)[-i] == f(syl)[-i] for i in range(1, min(level, len(f(syl))) + 1)])
		vowel_end = lambda pron: len(pron[-2]) > 2 and pron[-1] == 'Z' or len(pron[-1]) > 2 if len(pron) > 2 else len(pron[-1])
		vowel_check = lambda test, syl: vowel_end(test) if vowel_end(syl) else True
		rhymes = []
		for (word, syllable) in syllables:
			rhymes += [word for word, pron in entries if vowel_check(pron, syllable) and rhyme_check(pron, syllable, strip if exact else strip_stress)]
		rhymes.append(inp)
		return set(rhymes)| set(pronouncing.rhymes(inp))