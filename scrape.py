import requests
import sys
from bs4 import BeautifulSoup as bs

def scrape(url="https://speeches.byu.edu/speakers/kevin-j-worthen/"):
    base_content = requests.get(url).content
    soup = bs(base_content, 'html.parser')
    tags = str(soup.find_all("a", href=True))
    with open("base_content", "w") as fout:
        fout.write(tags)

def test():
    raise NotImplementedError

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "scrape":
        scrape()
    elif cmd == "test":
        test()

