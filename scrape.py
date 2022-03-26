import re
import requests
import sys
from bs4 import BeautifulSoup as bs

URL_LIST_FILENAME = "links.txt"
CORPUS_FILENAME = "fake_corpus.txt"

def get_links(url="https://speeches.byu.edu/speakers/kevin-j-worthen/"):
    """
    Writes all urls linking to speeches to file URL_LIST_FILENAME.
    """
    url_re = re.compile(
            r"^https://speeches.byu.edu/talks/kevin-j-worthen/.*/\n?$"
            )
    base_content = requests.get(url).content
    soup = bs(base_content, 'html.parser')
    tags = soup.find_all("a", href=True)
    tags = {tag.get('href') for tag in tags}
    with open(URL_LIST_FILENAME, "w") as fout:
        fout.writelines(tag + "\n" for tag in tags if url_re.search(tag))

def scrape():
    """
    Scrapes text from each url written to URL_LIST_FILENAME.
    """
    with open(URL_LIST_FILENAME) as fin:
        for link in fin.readlines():
            try:
                content = requests.get(link.strip()).content
                soup = bs(content)
                with open(CORPUS_FILENAME, "a") as fout:
                    fout.write(soup.text)
            except requests.exceptions.ConnectionError:
                continue

def clean():
    """
    Strips excessive newlines from corpus file.
    """
    with open(CORPUS_FILENAME) as fin:
        text = fin.read()
    with open(CORPUS_FILENAME, "w") as fout:
        fout.write(re.sub(r"\n{2,}", "\n", text))

def annotate():
    """
    Adds <start> tags to the beginning of each speech in corpus file.
    """
    with open(CORPUS_FILENAME) as fin:
        text = fin.read()
    with open(CORPUS_FILENAME + "_tagged.txt", "w") as fout:
        text = re.sub(r"<stop>.*\n\n", "<stop>\n\n<start> ", text)
        fout.write(text)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "scrape":
        scrape()
    elif cmd == "get_links":
        get_links()
    elif cmd == "clean":
        clean()
    elif cmd == "annotate":
        annotate()

