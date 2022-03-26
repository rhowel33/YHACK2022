from django.db import models

class SpeechGenerator(models.Model):
    """
    Speech generator. Currently reads generated text from a file
    and returns it.
    """
    def __init__(self, filename):
        with open(filename) as fin:
            self.text = fin.read()
        return self

