import requests
import sys
from bs4 import BeautifulSoup as bs

def scrape(url="https://speeches.byu.edu/speakers/kevin-j-worthen/"):
    base_content = requests.get(url).content
    with open("base_content.txt", "wb") as fout:
        fout.write(base_content)

def test(fname="base_content.txt"):
    with open(fname, "rb") as fin:
        base_content = fin.read()
    soup = bs(base_content, 'html.parser')
    tags = soup.find_all("a", href=True)
    for tag in tags:
        if not tag.text:
            print(tag)

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "scrape":
        scrape()
    elif cmd == "test":
        test()

