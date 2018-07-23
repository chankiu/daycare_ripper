import sys
from bs4 import BeautifulSoup
import requests
import re
import os

from scrapy.selector import Selector
from scrapy.http import HtmlResponse

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
    content = soup.find(class_='content-page')

    name = chankiu.clean_string(content.find("h2").contents[0])
    address = chankiu.clean_string(content.p.next).splitlines()[0]
    t_capacity_text = str(Selector(text=r.text).xpath('//*[@id="pfrComplexDescr_sml"]/div[2]/div/table[1]/tbody/tr[2]/td[2]').extract())
    t_capacity_text = chankiu.clean_string((t_capacity_text))
    t_capacity = 0
    t_rating = 0
    t_rating_url = str(Selector(text=r.text).xpath('//*[@id="pfrComplexDescr_sml"]/div[2]/div/table[1]/tbody/tr[2]/td[2]').extract())
    toddler_program = {'capacity': t_capacity, 'rating': t_rating, 'rating_url': t_rating_url}
    p_capactiy = 0
    p_rating = 0
    p_rating_url = ""
    preschool_program = {'capacity': p_capactiy, 'rating': p_rating, 'rating_url': p_rating_url};
    contact_info = chankiu.clean_string(str(content.find(class_='nudge')))

    return {'url': url,
            'name': name,
            'address': address,
            'toddler_program': toddler_program,
            'preschool_program': preschool_program,
            'contact_info': contact_info,
            'content': content
            }



if __name__ == "__main__":
    log.info("Ripping childcare data")

    # all_links_az = []
    # starting_point_url = "https://www.toronto.ca/data/children/dmc/a2z/a2za.html"
    # all_indexs_links = get_az_links(starting_point_url, log)
    # for index_link in all_indexs_links:
    #    all_links_az += index_link

    #print(len(all_links_az))

    print(get_details("https://www.toronto.ca/data/children/dmc/webreg/gcreg1288.html", log))














