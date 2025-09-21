import pandas as pd
from tqdm import tqdm
import folium, argparse
import json
from os.path import exists, isdir
from os import makedirs

if not isdir("outputs"):
    makedirs("outputs")

with open("parameters/filters.json") as f:
    filters = json.load(f)

parser = argparse.ArgumentParser()
parser.add_argument("map_name", type=str, nargs="?", default="output", help="Name of output map")
parser.add_argument("--filters", action="store_true", help="Optional arg to enable filters")
args = parser.parse_args()

ENABLE_FILTERS = args.filters
MAP_NAME = args.map_name.split(".")[0]

# Configure progress bars
tqdm.pandas()

# Load Data
print("Reading spreadsheet data")

if not exists('outputs/output.csv'):
    print("No spreadsheet to read data from")
    quit()

df = pd.read_csv('outputs/output.csv')#.iloc[0:100]
df = df.fillna("")

# Create Map
print("Generating map")
m = folium.Map(location=[df['LAT'].mean(), df['LON'].mean()], zoom_start=12)
for _, row in df.iterrows():
    if ENABLE_FILTERS:
        to_skip = False
        for detail, (action, items) in filters.items():
            if action == "INCLUDE" and row[detail] not in items:
                to_skip = True
                break
            elif action == "EXCLUDE" and row[detail] in items:
                to_skip = True
                break
            elif action == "BETWEEN" and (row[detail] < items[0] or row[detail] > items[1]):
                to_skip = True
                break
        if to_skip:
            continue

    popup_html=f"""
        <img src='{row['IMG']}' width='200'><br>
        <b>{row['LOCATION']}</b><br>
        Price: {row['PRICE']}<br>
        Size (sq m): {row['SIZE']}<br>
        Coucil Tax Band: {row['COUNCIL TAX']}<br>
        No Bedrooms: {row['BEDROOMS']}<br>
        No Bathrooms: {row['BATHROOMS']}<br>
        <a href='{row['LINK']}' target='_blank'>Link to source</a>
    """

    folium.Marker(
        location=[row['LAT'], row['LON']],
        popup=folium.Popup(popup_html, max_width=300)
    ).add_to(m)
m.save(f"outputs/{MAP_NAME}.html")
