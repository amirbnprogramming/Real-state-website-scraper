from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from Utils.bs4_selenium import FirefoxBrowser
from Utils.csv_saver import items_saver
from Utils.directory_creator import directory_creator
from Utils.logger import logger
from Utils.constants import base_url
from each_page_parser import EachStateParser
from states_links_scraper import scrape_states_links

browser = FirefoxBrowser()
created_direcctory = directory_creator('csv_files/')

state_links = scrape_states_links(base_url)
for state_link in state_links.values():
    state_parser = EachStateParser()
    browser.get_url(state_link)
    state_parser.state_title = browser.get_current_soup().find("title").text.replace(" | ", "_").replace(" ", "_")
    logger.info(f"Items for ({state_parser.state_title})")
    i = 1

    while True:
        try:
            logger.info(f"Page:({i})")
            current_url = browser.driver.current_url
            state_parser.each_page_parser(browser)

            pagination_section = browser.driver.find_element(By.CSS_SELECTOR, '#result-list-container > div > div > div.flex.flex-col.items-center.justify-center.mt-5.lg\:mt-0.gap > div')
            next_button = pagination_section.find_elements(By.XPATH, './*')[-1]

            WebDriverWait(browser.driver, 15).until(EC.element_to_be_clickable(next_button))
            next_button.click()
            i += 1
            # if i == 3:
            #     break
        except Exception as e:
            logger.error(f"Error:({e})")
            break
    state_result = state_parser.state_items
    # Save report
    items_saver(state_result, created_direcctory + f'{state_parser.state_title}.csv')
