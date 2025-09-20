from selenium import webdriver
import csv, argparse
import pandas as pd

from get_property_links import get_links
from get_property_data import scrape_multiple
from website_attributes import RIGHTMOVE
from os.path import exists

parser = argparse.ArgumentParser()
parser.add_argument("input_url", type=str, help="Required input url")
parser.add_argument("--rescrape", action="store_true", help="Optional arg to rescrape all links")
args = parser.parse_args()

INPUT_URL = args.input_url
RESCRAPE_ALL = args.rescrape

if not INPUT_URL:
    print("Source url not provided")
    quit()

driver = webdriver.Chrome()
links = get_links(driver, INPUT_URL, RIGHTMOVE, max_links=None)

if exists('output.csv'):
    df = pd.read_csv('output.csv')#.iloc[0:100]
    df = df.fillna("")

    existing_data = []
    new_links = []
    if RESCRAPE_ALL:
        new_links = links
    else:
        for link in links:
            matching_row = df[df["LINK"] == link]
            if not matching_row.empty:
                existing_data.append(matching_row.iloc[0].to_dict())
            else:
                new_links.append(link)

    details = existing_data + scrape_multiple(new_links, driver)

else:
    details = scrape_multiple(links, driver)

unique_keys_list = list(dict.fromkeys(k for d in details for k in d.keys()))

with open("output.csv", "w", newline='') as csvfile:
    # Create a DictWriter object, using keys of the first dict as fieldnames
    writer = csv.DictWriter(csvfile, fieldnames=unique_keys_list)
    
    # Write the header (column names)
    writer.writeheader()
    
    # Write the rows (list of dictionaries)
    writer.writerows(details)