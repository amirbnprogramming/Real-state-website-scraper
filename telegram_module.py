import functools
import os
import random
import threading
import time

import requests
import telebot
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from Utils.bs4_selenium import FirefoxBrowser
from Utils.constants import API_TOKEN, base_url
from Utils.csv_dict_convertor import csv_to_dict
from Utils.csv_saver import main_links_saver, items_saver
from Utils.directory_creator import directory_creator
from Utils.get_time import get_time
from Utils.logger import logger

# region :Bot creating
bot = telebot.TeleBot(API_TOKEN)
# endregion :Bot creating


class TelegramScrapper:
    def __init__(self):
        self.browser = None
        self.submenus = None
        self.un_id = 1
        self.state_items = {}
        self.state_title = ""

        self.link_button = telebot.types.InlineKeyboardButton(text='More Info')
        self.markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        self.chat_id = None

        self.welcome_logo = None

    @staticmethod
    def print_function_start(name, dir_name):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                bot.send_message(scrapper.chat_id, f"🟢 Scraping ({name}) Started . . .")
                logger.info(f" Scraping ({name}) Started . . .")

                bot.send_message(scrapper.chat_id, '⭕️ Bot is Working .... be patient 🙏')

                directory = directory_creator(f'{dir_name}/')

                func(*args, **kwargs, directory=directory)

                logger.info(f" Scraping ({name}) Finished . . .")
                bot.send_message(scrapper.chat_id, f"🟢 Scraping ({name}) Finished")

            return wrapper

        return decorator

    @print_function_start("States Links", dir_name='tele_files/csv_files/States')
    def states_scraper(self, directory) -> dict:
        submenu_links = {}
        res = requests.get(base_url)
        soup = BeautifulSoup(res.text, "html.parser")

        self.welcome_logo = soup.select(
            '#new-footer-col1 > div.et_pb_module.et_pb_image.et_pb_image_0_tb_footer.wahiLogoLinkFooter > a > span > img')[
            -1]['data-src']
        submenus = soup.select("#menu-header > li:nth-child(1) > ul:nth-child(2) a")

        for submenu in submenus:
            button = telebot.types.InlineKeyboardButton(submenu.text,
                                                        callback_data=submenu.text.lower().replace(" ", "_"))
            self.markup.add(button)
            submenu_links[button.callback_data] = submenu["href"]

        # region:Save report
        main_links_saver(submenu_links, directory + 'States_links.csv')
        # endregion:Save report

        self.submenus = submenu_links

        bot.send_photo(chat_id=scrapper.chat_id,
                       photo=scrapper.welcome_logo,
                       caption="🔎Select the State on(Wahi.com)",
                       reply_markup=scrapper.markup)

    @print_function_start("All Posts In Selected State", dir_name='tele_files/csv_files/States')
    def all_posts(self, callback_data, directory):
        if os.path.isfile(directory + 'States_links.csv'):
            self.browser = FirefoxBrowser()
            self.submenus = csv_to_dict(directory + 'States_links.csv')
            link = self.submenus[callback_data]
            self.browser.get_url(link)
            self.state_title = callback_data
            i = 1

            while True:
                bot.send_message(self.chat_id, f"🟢 Start Scraping in Page : ({i})")

                try:
                    self.each_page_parser(self.browser)

                    pagination_section = self.browser.driver.find_element(By.CSS_SELECTOR,
                                                                          '#result-list-container > div > div > div.flex.flex-col.items-center.justify-center.mt-5.lg\:mt-0.gap > div')
                    next_button = pagination_section.find_elements(By.XPATH, './*')[-1]

                    WebDriverWait(self.browser.driver, 15).until(EC.element_to_be_clickable(next_button))
                    next_button.click()
                    i += 1
                    if i == 3:
                        break
                except Exception as e:
                    logger.error(f"Error:({e})")
                    bot.send_message(self.chat_id, f"Error has occuredw while scraping.")
                    break
            state_result = self.state_items
            # Save report
            items_saver(state_result, f'tele_files/csv_files/{self.state_title}.csv')
            # Send File
            bot.send_document(self.chat_id, open(f'tele_files/csv_files/{self.state_title}.csv', 'r'),
                              caption=f"Report Items for State({self.state_title}) at ({get_time()})")

        else:
            logger.info("You Should '/Start' At First .")
            bot.send_message(self.chat_id, "🛑 You Should '/Start' At First .")

    def each_page_parser(self, browser):
        time.sleep(random.randint(10, 20))
        soup = browser.get_current_soup()
        posts = soup.find_all('div', class_='lg:rounded-lg border h-full')
        for post in posts:

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

            self.link_button.url = link
            new_markup = telebot.types.InlineKeyboardMarkup(row_width=1)
            new_markup.add(self.link_button)
            bot.send_photo(self.chat_id,
                           photo=img_link,
                           caption=f"On Market:  {time_on_market}\nPrice:  {price}\nCashback:  {cashback}\nOwnership: {ownership_regime}\nBedrooms:  {bedrooms}\nBathrooms:  {bathrooms}\nMeters:  {meters}\nListed_by_User: {listed_by}",
                           reply_markup=new_markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    scrapper.chat_id = call.message.chat.id
    timer_thread = threading.Thread(target=scrapper.all_posts, args=(call.data,))
    timer_thread.start()
    timer_thread.join()


@bot.message_handler(commands=['start'])
def send_start(message):
    scrapper.chat_id = message.chat.id
    # States scraping
    scrapper.states_scraper()


def start_bot():
    bot.polling()


if __name__ == '__main__':
    scrapper = TelegramScrapper()
    logger.info("Please send /Start command in bot")
    bot_thread = threading.Thread(target=start_bot, )
    bot_thread.start()
