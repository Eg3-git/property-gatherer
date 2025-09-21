from selenium.webdriver.common.by import By

RIGHTMOVE = {
    "base_url":"https://www.rightmove.co.uk/property-for-sale/find.html?",

    "variables": {
        #"minBedrooms": 2,
        #"dontShow": "retirement%2CsharedOwnership",
        #"channel": "BUY",
        #"index": 0,
        #"retirement": "false",
        #"maxBedrooms": 10,
        #"partBuyPartRent": "false",
        #"sortType": 2,
        #"areaSizeUnit": "sqm",
        #"viewType": "LIST",
        #"maxPrice": 200000,
        #"radius" : 0.0,
        #"locationIdentifier": "REGION%5E550",
        #"transactionType": "BUY",
        #"displayLocationIdentifier": "Glasgow.html"
    },

    "search-attributes": {
        "results-list": (By.ID, "l-searchResults"),
        "link-elements": (By.CLASS_NAME, "propertyCard-link")
    },

    "property-details": {
        "price_div": (By.CLASS_NAME, "_1gfnqJ3Vtd1z40MlC0MzXu")
    }
}

#rm_url = "https://www.rightmove.co.uk/property-for-sale/find.html?minBedrooms=3&dontShow=retirement%2CsharedOwnership&channel=BUY&index=0&retirement=false&maxBedrooms=10&partBuyPartRent=false&sortType=2&areaSizeUnit=sqm&viewType=LIST&maxPrice=200000&radius=0.0&locationIdentifier=REGION%5E550&transactionType=BUY&displayLocationIdentifier=Glasgow.html"
#alt_url = "https://www.rightmove.co.uk/property-for-sale/find.html?searchLocation=Glasgow&useLocationIdentifier=true&locationIdentifier=REGION%5E550&radius=0.0&_includeSSTC=on"
def update_variables(user_url, rightmove_variable_dict={}):
    variables = user_url.split("?")
    if len(variables) < 2:
        print("Url is malformed")
        quit()

    variable_list = "".join(variables[1:]).split("&")

    for variable_and_value in variable_list:
        variable, value = variable_and_value.split("=")
        rightmove_variable_dict[variable] = value

    return rightmove_variable_dict
