#python3


import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

import numpy as np
import pickle

START = "<start>"
STOP = "<stop>"
PUNCT = [',', '.', ';', ':', '!', '?']

class NGRAM:
    def __init__(self,N,filename='short_fake_corpus.txt',pickled=False):
        self.N = N
        self.file = filename
        self.words = []
        self.vocabulary = set()
        self.wordmap = {}
        self.temp = None
        self.nopunct = None
        self.state = []
        self.rng = np.random.default_rng()
        self.pickled = pickled

    def token_pos(self):
        with open(self.file,'r') as fin:
            data = fin.read()
        self.tokens = nltk.word_tokenize(data)
        self.pos_pairs = nltk.pos_tag(self.tokens)
        self.word_pos = {}
        self.pos_word = {}
        for pair in self.pos_pairs:
            word,pos = pair
            if word not in self.word_pos:
                self.word_pos[word] = {pos:1}
            else:
                if pos not in self.word_pos[word]:
                    self.word_pos[word][pos] = 1
                else:
                    self.word_pos[word][pos] += 1

            if pos not in self.pos_word:
                self.pos_word[pos] = {word:1}
            else:
                if word not in self.pos_word[pos]:
                    self.pos_word[pos][word] = 1
                else:
                    self.pos_word[pos][word] += 1


        return self

    def fit(self):
        PUNCT = [',', '.', ';', ':', '!', '?']
        self.token_pos()
        with open(self.file) as fin:
            data = fin.read().split(' ')



        for word in data:
            self.nopunct = ''
            punct_flag = False

            for char in word:
                punct_char = ''
                if char.isalpha():
                    self.nopunct+=char

                else:
                    for punc in PUNCT:
                        if punc == char:
                            punct_char += punc
                            punct_flag = True
                            break
                    if punct_flag:
                        self.words.append(self.nopunct)
                        self.words.append(punct_char)
                        break



            if not punct_flag:
                self.words.append(self.nopunct)

        for i in range(self.N):
            self.state.append(START)

        for word in self.words:
            try:
                self.wordmap[' '.join(self.state)].append(word)
            except KeyError:
                self.wordmap[' '.join(self.state)] = [word]
            self.state.append(word)
            self.state = self.state[1:]

        try:
            self.wordmap[' '.join(self.state)].append(STOP)
        except KeyError:
            self.wordmap[' '.join(self.state)] = [STOP]
        return self

    def pickle(self,write_type='wb'):
        with open(f'NGRM_wordmap.pk',f'{write_type}') as fout:
            pickle.dump(self.wordmap,fout)
            print("pickle complete")
        return self

    def _load(self):
        with open(f'NGRM_wordmap.pk','rb') as fin:
            self.wordmap = pickle.load(fin)
        return self


    def predict(self):
        state = []
        output = []
        for i in range(self.N):
            state.append(START)
        while STOP not in state:
            no_space_flag = False
            index = self.rng.integers(0,15) % len(self.wordmap[" ".join(state)])
            for symbol in PUNCT:
                if symbol == self.wordmap[" ".join(state)][int(index)]:
                    no_space_flag = True
                    break
            if not no_space_flag: output += " "
            output.append(self.wordmap[" ".join(state)][index])
            state.append(self.wordmap[" ".join(state)][index])
            state = state[1:]
        return "".join(output)

    def _stop(self, state):
        for item in state:
            if item == STOP:
                return True
        return False

if __name__ == "__main__":
    nmf = NGRAM(3)
    nmf.fit()
    print(nmf.word_pos)
    # print(nmf.wordmap)
    # print(nmf.predict())





