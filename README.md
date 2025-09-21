# property-gatherer
The purpose of this short program is to get all relevant properties from Rightmove, scrape the important details (location, size, council tax band etc.) and plot them onto a map to be browsed easily. The advantage is that you can see the key information for a property without having to open its page.

## Requirements

The main requirements are Python 3 and the Chrome browser. Additionally, part of the script involves using the Tesseract OCR engine to exract the total size from floor plans. This will be made optional in the future. Follow the instructions from the [Github page](https://github.com/tesseract-ocr/tesseract) to install Tesseract. See [here](https://pypi.org/project/pytesseract/) for more information on how it interacts with Python. 

## Setup

- Firstly, clone the repository to a folder on your device and ensure that you meet the requirements.
- Go to the ```property-gatherer``` root folder and install the dependencies by running ```pip install -r "requirements.txt"```


## How to run

The program is split into two scripts: ```pg_get_data``` and ```pg_plot_data``` which scrapes the property information from Rightmove and plots said data respectively.

### Scrape property information

- Go to Rightmove
- Search within your desired area and configure the filters
- Copy the URL
- Run ```python pg_get_data.py INPUT_URL``` where ```INPUT_URL``` is the URL that you just copied
- The script will automatically open Chrome and iterate through the search results. It then opens each property page to extract its key data.
- When finished, results are saved to ```outputs/output.csv```

Optional flags
- ```--rescrape```: To save time, by default properties that already exist in ```outputs/output.csv``` are skipped. Enable this flag to force all properties to be scraped.

### Plot property information

- Ensure that the above section has been completed
- Run ```python pg_plot_data.py```. You can pass in a string argument to name the output map. Example: ```python pg_plot_data.py my_flat_map```
- This creates an html file in the ```outputs/``` folder. By default, it is named ```output.html``` unless specified otherwise
- Open the html file in any browser

Optional flags
- ```--filters```: You can choose to enable filters which are specified in ```parameters/filters.json```. A filter is in the form ```COLUMN: [OPERATOR: [VALUES]],```
    - ```COLUMN``` refers to the specific column in ```outputs/output.csv```
    - ```OPERATOR``` specifies the action to take and can be one of the follow:
        - ```BETWEEN```: Select all items between values (inclusive)
        - ```INCLUDE```: Only select items included in the values
        - ```EXCLUDE```: Do not select items in the values
    - ```VALUES```: A comma-separated list of the values used by the Operator
