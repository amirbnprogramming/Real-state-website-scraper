import requests
from bs4 import BeautifulSoup

from Utils.csv_saver import main_links_saver
from Utils.directory_creator import directory_creator


def scrape_states_links(url) -> dict:
    submenu_links = {}
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    submenus = soup.select("#menu-header > li:nth-child(1) > ul:nth-child(2) a")
    for submenu in submenus:
        submenu_links[submenus.index(submenu) + 1] = submenu["href"]

    # region:Save report
    created_direcctory = directory_creator('csv_files/States/')
    main_links_saver(submenu_links, created_direcctory + 'States_links.csv')
    # endregion:Save report

    return submenu_links
