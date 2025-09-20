import pandas as pd
from tqdm import tqdm
import folium

filters = {
    "BEDROOMS": ["BET", [2, 10]],
    "COUNCIL TAX": ["EXC", ["Band: F", "Band: G", "Band: H"]]
}
enable_filters = True
map_name = "output"

# Configure progress bars
tqdm.pandas()

# Load Data
print("Reading spreadsheet data")
df = pd.read_csv('output.csv')#.iloc[0:100]
df = df.fillna("")

# Create Map
print("Generating map")
m = folium.Map(location=[df['LAT'].mean(), df['LON'].mean()], zoom_start=12)
for _, row in df.iterrows():
    if enable_filters:
        to_skip = False
        for detail, (action, items) in filters.items():
            if action == "INC" and row[detail] not in items:
                to_skip = True
                break
            elif action == "EXC" and row[detail] in items:
                to_skip = True
                break
            elif action == "BET" and (row[detail] < items[0] or row[detail] > items[1]):
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
m.save(map_name + ".html")
