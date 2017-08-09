import nltk, pronouncing

class Rhymer(object):
	VOWELS = ['AA', 'AH', 'AW', 'AH', 'AO', 'AY', 'EH','ER', 'EY', 'IH', 'IY', 'OY', 'OW', 'UW', 'UH']
	def rhyme(self, inp, level, exact = True):
		inp = inp.lower()
		entries = nltk.corpus.cmudict.entries()
		syllables = [(word, syl) for word, syl in entries if word == inp]
		strip_stress = lambda syl: [s[0:2] if len(s) > 2 else s for s in syl]
		strip = lambda syl: [strip_stress(s) for s in syl if s == 'L' or s[0:2] in self.VOWELS]
		rhyme_check = lambda test, syl, f: all([len(f(test)) >= i and f(test)[-i] == f(syl)[-i] for i in range(1, min(level, len(f(syl)), len(f(test)) + 1) + 1)])
		vowel_end = lambda pron: len(pron[-2]) > 2 and pron[-1] == 'Z' or len(pron[-1]) > 2 if len(pron) > 2 else len(pron[-1])
		vowel_check = lambda test, syl: vowel_end(test) if vowel_end(syl) else True
		rhymes = []
		for (word, syllable) in syllables:
			rhymes += [word for word, pron in entries if vowel_check(pron, syllable) and rhyme_check(pron, syllable, strip)]
		rhymes.append(inp)
		return set(rhymes)| set(pronouncing.rhymes(inp))
