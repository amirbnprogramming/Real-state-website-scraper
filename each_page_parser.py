import random
import time

from Utils.logger import logger
from Utils.constants import base_url


class EachStateParser:

    def __init__(self):
        self.un_id = 1
        self.state_items = {}
        self.state_title = ""

    def each_page_parser(self, browser):
        time.sleep(random.randint(10, 20))
        soup = browser.get_current_soup()
        posts = soup.find_all('div', class_='lg:rounded-lg border h-full')
        for post in posts:
            item = {}

            try:
                link = base_url + post.find('a').attrs['href']
            except Exception:
                link = "No data"
            try:
                img_link = post.select_one('img').attrs.get('src')
            except Exception:
                img_link = "No data"
            try:
                time_on_market = post.find('span',
                                           class_='inline-flex items-center py-1 rounded-full text-primary-text-color bg-secondary-off-white text-caption p-1 mr-2 pl-1 pr-3').find(
                    'span').text
            except Exception:
                time_on_market = "No data"
            try:
                price = post.find('div', class_='w-full text-xl font-black text-primary-text-color').text
            except Exception:
                price = "No data"
            try:
                cashback = post.find('span', class_='text-success-green font-black').text
            except Exception:
                cashback = "No data"
            try:
                details = post.find_all('span', class_='align-middle')
            except Exception:
                details = "No data"

            ownership_regime = details[0].text
            bedrooms = details[1].text
            bathrooms = details[2].text
            meters = details[3].text
            listed_by = post.find('div', class_='text-[10px] text-secondary-text-light-gray mt-2 truncate').text

            item = {
                'Link': link,
                'Img_Link': img_link,
                'Time_On_Market': time_on_market,
                'Price': price,
                'Cashback': cashback,
                'Ownership_Regime': ownership_regime,
                'Bedrooms': bedrooms,
                'Bathrooms': bathrooms,
                'Meters': meters,
                'Listed_by_User': listed_by,
            }
            self.state_items[self.un_id] = item
            self.un_id += 1
            logger.info(link)
            logger.info(img_link)
            logger.info(time_on_market)
            logger.info(price)
            logger.info(cashback)
            logger.info(ownership_regime)
            logger.info(bedrooms)
            logger.info(bathrooms)
            logger.info(meters)
            logger.info(listed_by)
