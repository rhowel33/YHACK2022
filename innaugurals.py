#python3
import nltk
import nltk.corpus as corpus
from nltk.corpus import inaugural

def get_speeches(n=6):
    nltk.download()

    ids = inaugural.fileids()[-n:]
    address = [f'<start> {inaugural.raw(fileids=f"{id}")} <stop>' for id in ids]

    return address

print(get_speeches())