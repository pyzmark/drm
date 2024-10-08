# Import the basic libraries
import pandas as pd
import folium

# Get the latest pleiades data
pleid = pd.read_csv('http://atlantides.org/downloads/pleiades/dumps/pleiades-places-latest.csv.gz')

# Creation of a mining/metal-specific dataframe: cutting nulls to allow mapping
metal = pleid[pleid['featureTypes'].astype(str).str.contains('mine')]
metal = metal[(metal.description.notnull()) & (metal.timePeriods.notnull())]
metal = metal[(metal.reprLat.notnull()) & (metal.reprLong.notnull())]

# Build the map, focusing on Europe
latitude = 36
longitude = 18

# Create map and display it
edm_map = folium.Map(
				location=[latitude, longitude], zoom_start=4, tiles='https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png', attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
)

# function to populate the map with points and labels that include
# information like title, time period active, etc.
def adder(this,colour):
    resource = metal[metal['tags'].astype(str).str.contains(this)]
    sign = folium.map.FeatureGroup()
    resource['title'] = resource['title'].astype(str)
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
    sign.layer_name = this
    
# Run the function for the following metals, w color
# Add a '#' to the start of each line to turn each one off
adder('iron','#FF5964')
adder('silver','#818479')
adder('gold','#E8AA14')
adder('marble','#35A7FF')
adder('copper','#23F0C7')
adder('tin', '#B118C8')
adder('lapis','blue')

# add the layer control
folium.LayerControl(collapsed=False).add_to(edm_map)

# Produce a map: for now an HTML file works
edm_map.save(outfile='index.html')
