import numpy as np
import pickle

START = "<start>"
STOP = "<stop>"
PUNCT = [',', '.', ';', ':', '!', '?']

class NGRAM:
    def __init__(self,N,filename='corpus.txt',pickled=False):
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

    def fit(self):
        PUNCT = [',', '.', ';', ':', '!', '?']

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
        for i in range(self.N):
            state.append(START)
        # state = " ".join(state)
        # output = ""
        output = []
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
        return " ".join(output)

    def _stop(self, state):
        for item in state:
            if item == STOP:
                return True
        return False

if __name__ == "__main__":
    nmf = NGRAM(3)
    nmf.fit()
    print(nmf.wordmap)
    print(nmf.predict())



