import telebot

base_url = "https://wahi.com/"
url = ""
profile_path = ''

# region :Bot Settings
API_TOKEN = ''

supertypes_button = telebot.types.InlineKeyboardButton('Scrape Super Types', callback_data='supertypes')
offers_button = telebot.types.InlineKeyboardButton('Scrape All Offers', callback_data='offers')
newproducts_button = telebot.types.InlineKeyboardButton('Scrape New Products', callback_data='newproducts')
brands_button = telebot.types.InlineKeyboardButton('Scrape Brands', callback_data='brands')
products_by_brands_button = telebot.types.InlineKeyboardButton('Scrape Products By Brands',
                                                               callback_data='productsbybrand')

markup = telebot.types.InlineKeyboardMarkup(row_width=1)
markup.add(supertypes_button, offers_button, newproducts_button, brands_button, products_by_brands_button)
# endregion :Bot Settings
