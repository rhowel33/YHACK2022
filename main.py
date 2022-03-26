#python3


"""
YHACK 2022  group project

Group: Eli Cox, Christian and Reagan Howell

Given a text using a markov model with nlp to identify the types of speech generate a similar text

Pass in N and filename in the terminal
"""

from ngrams import NGRAM
import sys

if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise ValueError("main.py takes 3 sysargs: N (number of previous words to use), filename (corpus), pickled (boolean if you want to load a pickle file")

    N = int(sys.argv[1])
    filename = sys.argv[2]
    if sys.argv[3] == "False":
        pickled = False
    else:
        pickled = True
    if not pickled:
        ngram = NGRAM(N,filename,pickled)
        print(ngram.fit().pickle())
    else:
        ngram = NGRAM(N,filename,pickled)

