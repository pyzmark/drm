# Import the basic libraries
import pandas as pd
import numpy as np
import folium
from pandas import ExcelWriter
from pandas import ExcelFile

pd.set_option('display.max_columns', 500)

# Get the latest pleiades data
!wget --output-document pleiades.csv.gz http://atlantides.org/downloads/pleiades/dumps/pleiades-places-latest.csv.gz
pleid = pd.read_csv('pleiades.csv.gz', compression='infer')

# Creation of a mining/metal only database: cutting nulls to allow mapping
metal = pleid[pleid['featureTypes'].astype(str).str.contains('mine')]
metal = metal[(metal.description.notnull()) & (metal.timePeriods.notnull())]
metal = metal[(metal.reprLat.notnull()) & (metal.reprLong.notnull())]

# Build the map
latitude = 36
longitude = 18

# Create map and display it
edm_map = folium.Map(
    location=[latitude, longitude], zoom_start=3, tiles='Stamen Toner'
)

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

adder('iron','red')
adder('silver','grey')
adder('gold','yellow')
adder('marble','blue')
adder('copper','#995303')
adder('tin', '#02eb41')

edm_map.save(outfile='/Users/Mark/Inbox/mines_map.html')
