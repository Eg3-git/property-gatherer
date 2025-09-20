from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions
from tqdm import tqdm
import re
from PIL import Image
import pytesseract
import requests
from io import BytesIO

def scrape_property(link, driver):
    driver.get(link)

    WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "_1gfnqJ3Vtd1z40MlC0MzXu")))

    price_div = driver.find_element(By.CLASS_NAME, "_1gfnqJ3Vtd1z40MlC0MzXu")
    price = price_div.find_element(By.TAG_NAME, "span").text

    location = driver.find_element(By.CLASS_NAME, "_2uQQ3SV0eMHL1P6t5ZDo2q").text

    main_img_spans = driver.find_elements(By.CLASS_NAME, "_2uGNfP4v5SSYyfx3rZngKM")[0]
    main_img_src = main_img_spans.find_element(By.TAG_NAME, "img").get_attribute("src")

    gmap = driver.find_element(By.CLASS_NAME, "_1kck3jRw2PGQSOEy3Lihgp")
    driver.execute_script("arguments[0].scrollIntoView(true);", gmap)
    WebDriverWait(gmap, 10).until(expected_conditions.presence_of_element_located((By.TAG_NAME, "img")))
    gmap_src = gmap.find_element(By.TAG_NAME, "img").get_attribute("src")
    property_coords = re.search(r"latitude=([\-.\d]+)&longitude=([\-.\d]+)", gmap_src)
    if property_coords:
        property_lat = property_coords.group(1)
        property_lon = property_coords.group(2)
    else:
        property_lat, property_lon = 0, 0

    property_attributes = [attribute.text for attribute in driver.find_elements(By.CLASS_NAME, "ZBWaPR-rIda6ikyKpB_E2")]
    property_attribute_values = [attribute.text for attribute in driver.find_elements(By.CLASS_NAME, "_1hV1kqpVceE9m-QrX_hWDN")]
    
    additional_attributes = [attribute.text for attribute in driver.find_elements(By.CLASS_NAME, "_17A0LehXZKxGHbPeiLQ1BI")]
    additional_attribute_values = [attribute.text for attribute in driver.find_elements(By.CLASS_NAME, "_2zXKe70Gdypr_v9MUDoVCm")]

    attribute_dict = dict(zip(property_attributes, property_attribute_values)) | dict(zip(additional_attributes, additional_attribute_values))

    property_details = {"LINK": link, 
                        "LAT": property_lat, 
                        "LON": property_lon,
                        "IMG": main_img_src,
                        "PRICE": price, 
                        "LOCATION": location} | attribute_dict
    
    if "SIZE" in property_details: 
        if "ASK" in property_details["SIZE"].upper():
            property_details["SIZE"] = extract_size_from_floorplan(driver, link)
        elif "ft" in property_details["SIZE"].lower() or "feet" in property_details["SIZE"].lower():
            property_details["SIZE"] = int(property_details["SIZE"].split(" ")[0].replace(",", ""))
            property_details["SIZE"] = int(property_details["SIZE"] / 10.764)

    return property_details

def extract_size_from_floorplan(driver, url):
    floorplan_url = url.split("?")[0] + "floorplan"

    try:
        driver.get(floorplan_url)
        WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "react-transform-component")))
        img_div = driver.find_element(By.CLASS_NAME, "react-transform-component")
        floorplan_img_src = img_div.find_element(By.TAG_NAME, "img").get_attribute("src")
    except:
        return "COULD NOT FIND FLOORPLAN"
    
    floorplan_img_data = Image.open(BytesIO(requests.get(floorplan_img_src).content))

    text = pytesseract.image_to_string(floorplan_img_data)

    pattern = r"[+-]?\s*\d+(?:\.\d+)?\s*(?:square meters|square metres|sq[.\s]?m|sqm|m2|m²|m\?)"

    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        matching_text = match.group().strip()

        try:
            value = int(float(matching_text.split(" ")[0]))
        except Exception as e:
            value = matching_text
        return value
    else:
        return "COULD NOT FIND SIZE"

def scrape_multiple(links, driver):
    all_details = []

    print("Scraping property data...")
    for link in tqdm(links):
        try:
            all_details.append(scrape_property(link, driver))
        except Exception as e:
            print(f"Encountered problem with {link}")
            print(e)

    return all_details

if __name__ == "__main__":
    driver = webdriver.Chrome()
    link = "https://www.rightmove.co.uk/properties/160333841#/?channel=RES_BUY"

    print(scrape_property(link, driver))
    

