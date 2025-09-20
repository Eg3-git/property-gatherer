from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions
from tqdm import tqdm
from website_attributes import update_variables

def construct_rightmove_url(base_url, variables, index=0):
    variables["index"] = index

    first_variable = list(variables.keys())[0]
    generated_url = base_url + f"{first_variable}={variables[first_variable]}"

    for var, val in list(variables.items())[1:]:
        generated_url += f"&{var}={val}"

    return generated_url

url = "https://www.zoopla.co.uk/for-sale/details/70414688/"

#otm_url = https://www.onthemarket.com/for-sale/property/glasgow/?auction=false&max-price=200000&min-bedrooms=2&retirement=false&shared-ownership=false&view=map-list

def get_links(driver, input_url, website_attributes, max_links=None):
    base_url = website_attributes["base_url"]
    variables = update_variables(input_url, website_attributes["variables"])
    search_attributes = website_attributes["search-attributes"]

    generated_url = construct_rightmove_url(base_url, variables, index=0)

    driver.get(generated_url)
    WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located(search_attributes["results-list"]))

    dropdown_div = driver.find_element(By.CLASS_NAME, "Pagination_pageSelect__dUffQ")
    select_element = dropdown_div.find_element(By.TAG_NAME, "select")

    # Wrap select element with Select class
    select = Select(select_element)

    # Get all option value attributes
    option_values = [option.get_attribute("value") for option in select.options]

    property_links = []

    print("Getting property links...")
    for index in tqdm(option_values):
        next_url = construct_rightmove_url(base_url, variables, index=index)

        driver.get(next_url)
        WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.ID, "l-searchResults")))

        link_elements = driver.find_elements(*search_attributes["link-elements"])
        property_links.extend([link.get_attribute("href") for link in link_elements])

        if max_links and max_links < len(property_links):
            return property_links[:max_links]

    return set(property_links)
