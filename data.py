# Import the basic libraries
import pandas as pd
import numpy as np
import folium
from pandas import ExcelWriter
from pandas import ExcelFile

# Get the latest pleiades data
pleid = pd.read_csv('http://atlantides.org/downloads/pleiades/dumps/pleiades-places-latest.csv.gz')

# Creation of a mining/metal-specific dataframe: cutting nulls to allow mapping
metal = pleid[pleid['featureTypes'].astype(str).str.contains('mine')]
metal = metal[(metal.description.notnull()) & (metal.timePeriods.notnull())]
metal = metal[(metal.reprLat.notnull()) & (metal.reprLong.notnull())]

# Build the map, focsusing on Europe
latitude = 36
longitude = 18

# Create map and display it
edm_map = folium.Map(
    location=[latitude, longitude], zoom_start=3, tiles='Stamen Toner'
)

# function to populate the map with points and labels that include
# information like title, time period active, etc.
def adder(this,colour):
    resource = metal[metal['tags'].astype(str).str.contains(this)]
    sign = folium.map.FeatureGroup()
    resource['title'] = resource['title'].astype(str)
    resource['title'] = resource['title'].astype(str)
    resource['timePeriods'] = resource['timePeriods'].astype(str)
    resource['timePeriods'] = resource['timePeriods'].astype(str)
    # add pop-up text to each marker on the map
    signlatitudes = list(resource.reprLat)
    signlongitudes = list(resource.reprLong)
    labels = list(
        resource.title +
        ' was active in ' + resource.timePeriods + '. ' + resource.description + '.'
    )
    for lat, lng, label in zip(signlatitudes, signlongitudes, labels):
        sign.add_child(
            folium.features.CircleMarker(
                [lat, lng],
                radius=4,  # define how big you want the circle markers to be
                color=colour,
                fill=True,
                fill_color=colour,
                fill_opacity=1,
                popup=folium.Popup(label, parse_html=True)
            )
        )
    edm_map.add_child(sign)

# Run the function for the following metals, w color
adder('iron','red')
adder('silver','grey')
adder('gold','yellow')
adder('marble','blue')
adder('copper','#995303')
adder('tin', '#02eb41')

# Produce a map: for now an HTML file works
edm_map.save(outfile='mines_map.html')
