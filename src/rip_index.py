import sys
from bs4 import BeautifulSoup
import requests
import re
import os

from scrapy.selector import Selector
from scrapy.http import HtmlResponse

from urllib.parse import urlparse, urljoin

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

    try:
        name = chankiu.clean_string(content.find("h2").contents[0])
        address = chankiu.clean_string(content.p.next).splitlines()[0]
    except (RuntimeError, TypeError, NameError) as e:
        name = "na"
        address = "na"
        log.warn("Error in name and address")
        log.debug(e)

    try:
        t_capacity = Selector(text=r.text).xpath('//*[@id="pfrComplexDescr_sml"]/div[2]/div/table[1]/tbody/tr[2]/td[2]/text()').extract()[0].strip()
        t_rating = Selector(text=r.text).xpath('//*[@id="pfrComplexDescr_sml"]/div[2]/div/table[1]/tbody/tr[2]/td[3]/a/text()').extract()[0].strip()
        t_rating_url = Selector(text=r.text).xpath('//*[@id="pfrComplexDescr_sml"]/div[2]/div/table[1]/tbody/tr[2]/td[1]/a/@href').extract()[0].strip()
        toddler_program = {'capacity': t_capacity, 'rating': t_rating, 'rating_url': t_rating_url}
    except (RuntimeError, TypeError, NameError) as e:
        toddler_program = {'capacity': 0, 'rating': 0, 'rating_url': ""}
        log.warn("Error with Toddler data")
        log.debug(e)

    try:
        p_capacity = Selector(text=r.text).xpath('//*[@id="pfrComplexDescr_sml"]/div[2]/div/table[1]/tbody/tr[3]/td[2]/text()').extract()[0].strip()
        p_rating = Selector(text=r.text).xpath('//*[@id="pfrComplexDescr_sml"]/div[2]/div/table[1]/tbody/tr[3]/td[3]/a/text()').extract()[0].strip()
        p_rating_url = Selector(text=r.text).xpath('//*[@id="pfrComplexDescr_sml"]/div[2]/div/table[1]/tbody/tr[3]/td[1]/a/@href').extract()[0].strip()
        preschool_program = {'capacity': p_capacity, 'rating': p_rating, 'rating_url': p_rating_url}
    except (RuntimeError, TypeError, NameError) as e:
        preschool_program = {'capacity': 0, 'rating': 0, 'rating_url': ""}
        log.warn("Error with Preschool data")
        log.debug(e)

    try:
        contact_info = Selector(text=r.text).xpath('//*[@id="pfrComplexDescr_sml"]/div[3]/ul/li/text()').extract()[0].strip()
        contact_info = re.sub('[^a-zA-Z0-9\n\.]', ' ', contact_info)
        contact_info = re.sub(' +',' ', contact_info)
    except (RuntimeError, TypeError, NameError):
        contact_info = "na"
        log.warn("Error in contact info")
        log.debug(e)


    return {'url': url,
            'name': name,
            'address': address,
            'toddler_program': toddler_program,
            'preschool_program': preschool_program,
            'contact_info': contact_info,
            'content': ""
            }


def get_details_from_index(index_url, log):
    all_details = []
    for index_link in get_az_links(index_url, log):
        all_details += get_details(index_link, log)

    return all_details


if __name__ == "__main__":
    log.info("Ripping childcare data")

    log.info("Get All Index Links")
    all_index_links_az = []
    for index_link in get_az_links("https://www.toronto.ca/data/children/dmc/a2z/a2za.html", log):
        all_index_links_az += get_az_links(index_link, log)

    all_detail_links = []
    for links in all_index_links_az:
        all_detail_links += get_links_from_index(links, log)

    log.info("Get all detail links")
    for detail_links in all_detail_links:
        print(detail_links)

    print(len(all_detail_links))
















