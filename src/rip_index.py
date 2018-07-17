import sys
from bs4 import BeautifulSoup
import requests
import re
import os

import chankiu
log = chankiu.log(sys.argv[0])

def get_links_from_index(index_url, log):
    r = requests.get(index_url)
    base_url = os.path.dirname(index_url)
    soup = BeautifulSoup(r.text, 'html.parser')

    # print(soup.prettify())
    sections = soup.body.findAll("section")
    links = sections[1].table.tbody.findAll("a", href=True)
    real_links = []
    for link in links:
        real_links.append("{0}/{1}".format(base_url, str(link['href'])))

    return real_links


if __name__ == "__main__":
    log.info("Ripping childcare data")

    links = get_links_from_index("https://www.toronto.ca/data/children/dmc/a2z/a2za.html", log)

    for link in links:
        print(link)











