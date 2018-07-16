import sys
from bs4 import BeautifulSoup
import requests

import chankiu
log = chankiu.log(sys.argv[0])

if __name__ == "__main__":
    log.info("Ripping childcare data")

    r = requests.get("https://www.toronto.ca/data/children/dmc/a2z/a2za.html")

    soup = BeautifulSoup(r.text, 'html.parser')

    # print(soup.prettify())


