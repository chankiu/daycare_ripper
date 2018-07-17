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


def get_az_links(index_url, log):
    r = requests.get(index_url)
    base_url = os.path.dirname(index_url)
    soup = BeautifulSoup(r.text, 'html.parser')

    sections = soup.body.findAll("section")
    links = sections[1].div.div.div.div.div.ul.findAll('a', href=True)
    real_links = []
    for link in links:
        real_links.append("{0}/{1}".format(base_url, str(link['href'])))

    return real_links


def get_details(url, log):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    return soup.findAll(class_='content-page')


if __name__ == "__main__":
    log.info("Ripping childcare data")

    # all_links_az = []
    # starting_point_url = "https://www.toronto.ca/data/children/dmc/a2z/a2za.html"
    # all_indexs_links = get_az_links(starting_point_url, log)
    # for index_link in all_indexs_links:
    #    all_links_az += index_link

    #print(len(all_links_az))

    print(get_details("https://www.toronto.ca/data/children/dmc/webreg/gcreg1288.html", log))














