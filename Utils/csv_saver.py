from encodings.utf_8 import decode

import pandas as pd

from Utils.logger import logger


def main_links_normalizer(data):
    processed_data = []
    for key, value in data.items():
        row = {
            'Id': key,
            'Link': value
        }
        processed_data.append(row)
    return processed_data


def main_links_saver(data, path):
    pre_processed_data = main_links_normalizer(data)
    df = pd.DataFrame(pre_processed_data)
    df.to_csv(path, index=False)
    logger.warning(f"Item's File saved to {path}")


def items_normalizer(data):
    processed_data = []
    for key, value in data.items():
        row = {
            'Id': key,
            'Link': value['Link'],
            'Img_Link': value['Img_Link'],
            'Time_On_Market': value['Time_On_Market'],
            'Price': value['Price'],
            'Cashback': value['Cashback'],
            'Ownership_Regime': value['Ownership_Regime'],
            'Bedrooms': value['Bedrooms'],
            'Bathrooms': value['Bathrooms'],
            'Meters': value['Meters'],
            'Listed_by_User': value['Listed_by_User']
        }
        processed_data.append(row)
    return processed_data


def items_saver(data, path):
    pre_processed_data = items_normalizer(data)
    df = pd.DataFrame(pre_processed_data)
    df.to_csv(path, index=False)
    logger.warning(f"Item's File saved to {path}")
