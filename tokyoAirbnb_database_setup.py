# Import the dependencies.
import warnings
warnings.filterwarnings('ignore')

from flask import Flask, render_template_string, send_file

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func
import numpy as np
import base64
import plotly.express as px
import json
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/tokyoAirbnb.sqlite")

# reflect an existing database into a new model

Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True, schema='main')


# Create our session (link) from Python to the DB
session = Session(engine)


# Save references to each table

tokyo_airbnb = Base.classes.tokyoAirbnb

# #################################################
# # Flask Setup
# #################################################

from flask import Flask, jsonify

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return ("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Tokyo Airbnbs</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f9f9f9;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .container {
                background-color: #cfe0e8;
                max-width: 800px;
                width: 90%;
                padding: 20px;
                margin-top: 50px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                border-radius: 8px;
            }
            h1 {
                text-align: center;
                color: #333;
            }
            p {
                color: #000000;
                line-height: 1.6;
            }
            .members, .routes, .data, .cleaning{
                margin: 20px 0;
            }
            .members ul, .routes ul, .data ul, .cleaning ul{
                list-style-type: none;
                padding: 0;
            }
            .members li, .github p, .routes li, .data li, .cleaning li {
                background-color: #b7d7e8;
                margin: 5px 0;
                padding: 10px;
                border-radius: 4px;
            }
            .data li li {
                background-color: #87bdd8;
                margin: 10px;
                padding: 10px;
                border-radius: 4px;
            }
            .data a {
                color: #000000;
                text-decoration: none;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Listing Activity of Tokyo Airbnbs</h1>
            <p>With the rise in travel post-pandemic and increased popularity of unique Airbnb travel accommodations, we wanted to explore the best locations and prices for Airbnbs in Tokyo, Japan.</p>
            
                <div class="members">
                    <h2>Members</h2>
                    <ul>
                        <li>Abel Dumecha</li>
                        <li>Amanda Liu</li>
                        <li>Cassidy Schultheis</li>
                        <li>Sophia Emanuel</li>
                    </ul>
                </div>
            <div class="data">
                <h2>Data</h2>
                <ul>
                    <li>
                        <a href="https://www.kaggle.com/datasets/lucamassaron/tokyo-airbnb-open-data-2023?select=reviews.csv" target="_blank">Kaggle Dataset</a>
                        <ul>
                            <li>- summery_listings.csv</li>
                            <li>- Neighborhoods.geojson</li>
                        </ul>
                    </li>
                </ul>
            </div>
            
            <div class ="cleaning">
                <h2>Data Cleaning/Transforming/Storing</h2>
                <ul>
                    <li>Deleted unwanted columns</li>
                    <li>Split specific columns (e.g., split name column into separate beds and baths columns)</li>
                    <li>Removed unwanted symbols and null values</li>
                    <li>Modified data types of certain column values and reordered columns</li>
                    <li>Uploaded cleaned CSV file as 'updated_summarylist.csv' and imported the data into a SQLite database named 'tokyoAirbnb.sqlite'.</li>
                </ul>
            </div>
                
            <div class = "routes">
                <h2>Visualization Routes</h2>
                <ul>
                    <li><a href="/api/v1.0/Listings_Counts_By_Neighborhood"><button>Number of Listings by Neighborhood in Tokyo, Japan</button></a></li>
                    <li><a href="/api/v1.0/Overall_Prices"><button>Distribution of Airbnb Prices in Tokyo, Japan</button></a></li>
                    <li><a href="/api/v1.0/Price_Distribution_Top15_Neighborhoods"><button>Price Distribution for Top 15 Neighborhoods in Tokyo, Japan</button></a></li>
                    <li><a href="/api/v1.0/HeatMapTop15AveragePricebyNeighbourhoodandRoomType"><button>Average Price for Top 15 Neighborhoods by Room Type in Tokyo, Japan</button></a></li>
                    <li><a href="/api/v1.0/HeatMapAllAveragePricebyNeighbourhoodandRoomType"><button>Average Price for All Neighborhoods by Room Type in Tokyo, Japan</button></a></li>
                    <li><a href="/api/v1.0/HeatMapTop15AveragePricebyNeighborhoodandBedroom"><button>Average Price for Top 15 Neighborhoods by Number of Bedrooms in Tokyo, Japan</button></a></li>
                    <li><a href="/api/v1.0/choropleth_map_neighborhoods"><button>Choropleth Map Airbnb Neighborhoods in Tokyo, Japan</button></a></li>
                    <li><a href="/api/v1.0/Tokyo_Airbnb_Map_Room_Type"><button>Airbnb Locations Filtered By Room Type in Tokyo, Japan</button></a></li>
                </ul>
            </div>

            <div class="github">
                <h2>Github Repository</h2>
                <p><a href="https://github.com/sophiagemanuel/Tokyo-Airbnb" target="_blank">Github Repository</a></p>
            </div>   

        </div>
    </body>
    </html>
    """)



##############################################
#Route for listings by neighbhorhood barchart
##############################################
@app.route("/api/v1.0/Listings_Counts_By_Neighborhood")
def neighbourhoods():
    # Read the saved PNG file and encode it to base64
    with open('Resources/barchart_of_neighborhoodlistings_in_tokyo.png', 'rb') as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    # Create an HTML string with the base64 image embedded
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <style>
        body {{
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        h1 {{
            text-align: center;
            color: black;
        }}
    </style>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Number of Listings by Neighborhood in Tokyo, Japan</title>
    </head>
    <body>
        <h1>Number of Listings by Neighborhood in Tokyo, Japan</h1>
        <img src="data:image/png;base64,{image_base64}" alt="Number of Listings by Neighborhood in Tokyo, Japan">
    </body>
    </html>
    """
    return render_template_string(html_content)

@app.route("/api/v1.0/Overall_Prices")
def prices():
    with open('Resources/histogram_of_prices_in_tokyo.png', 'rb') as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    # Create an HTML string with the base64 image embedded
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <style>
        body {{
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        h1 {{
            text-align: center;
            color: black;
        }}
    </style>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Distribution of Airbnb Prices in Tokyo, Japan</title>
    </head>
    <body>
        <h1>Distribution of Airbnb Prices in Tokyo, Japan</h1>
        <img src="data:image/png;base64,{image_base64}" alt="Distribution of Airbnb Prices in Tokyo, Japan">
    </body>
    </html>
    """
    return render_template_string(html_content)



##############################################
#Route for boxplot showing price distribution for top 15 neighborhoods
##############################################
@app.route("/api/v1.0/Price_Distribution_Top15_Neighborhoods")
def top15pricedistribution():
    with open('Resources/price_distribution.png', 'rb') as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    # Create an HTML string with the base64 image embedded
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <style>
        body {{
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        h1 {{
            text-align: center;
            color: black;
        }}
    </style>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Price Distribution for Top 15 Neighborhoods in Tokyo</title>
    </head>
    <body>
        <h1>Price Distribution for Top 15 Neighborhoods in Tokyo</h1>
        <img src="data:image/png;base64,{image_base64}" alt="Price Distribution for Top 15 Neighborhoods in Tokyo">
    </body>
    </html>
    """
    return render_template_string(html_content)

##############################################
#Price Disribution for Top 15 Neighborhoods Including Room Type
##############################################
@app.route("/api/v1.0/HeatMapTop15AveragePricebyNeighbourhoodandRoomType")
def top15priceroom():
    with open('Resources/HeatMapTop15AveragePricebyNeighbourhoodandRoomType.png', 'rb') as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    # Create an HTML string with the base64 image embedded
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <style>
        body {{
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        h1 {{
            text-align: center;
            color: black;
        }}
    </style>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Average Price for Top 15 Neighborhoods by Room Type in Tokyo, Japan </title>
    </head>
    <body>
        <h1>Average Price for Top 15 Neighborhoods by Room Type in Tokyo, Japan </h1>
        <img src="data:image/png;base64,{image_base64}" alt="Average Price for Top 15 Neighborhoods by Room Type in Tokyo, Japan">
    </body>
    </html>
    """
    return render_template_string(html_content)

##############################################
#Price Disribution for All Neighborhoods Including Room Type
##############################################
@app.route("/api/v1.0/HeatMapAllAveragePricebyNeighbourhoodandRoomType")
def allpriceroom():
    with open('Resources/HeatMapAllAveragePricebyNeighbourhoodandRoomType.png', 'rb') as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    # Create an HTML string with the base64 image embedded
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <style>
        body {{
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        h1 {{
            text-align: center;
            color: black;
        }}
    </style>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Average Price for All Neighborhoods by Room Type in Tokyo, Japan </title>
    </head>
    <body>
        <h1>Average Price for All Neighborhoods by Room Type in Tokyo, Japan </h1>
        <img src="data:image/png;base64,{image_base64}" alt="Average Price for All Neighborhoods by Room Type in Tokyo, Japan">
    </body>
    </html>
    """
    return render_template_string(html_content)

##############################################
#Price Disribution for All Neighborhoods Including Room Type
##############################################
@app.route("/api/v1.0/HeatMapTop15AveragePricebyNeighborhoodandBedroom")
def top15pricebedrooms():
    with open('Resources/HeatMapTop15AveragePricebyNeighborhoodandBedrooms.png', 'rb') as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

    # Create an HTML string with the base64 image embedded
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <style>
        body {{
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        h1 {{
            text-align: center;
            color: black;
        }}
    </style>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Average Price for Top 15 Neighborhoods by Number of Bedrooms in Tokyo, Japan</title>
    </head>
    <body>
        <h1>Average Price for Top 15 Neighborhoods by Number of Bedrooms in Tokyo, Japan </h1>
        <img src="data:image/png;base64,{image_base64}" alt="Average Price for Top 15 Neighborhoods by Number of Bedrooms in Tokyo, Japan">
    </body>
    </html>
    """
    return render_template_string(html_content)

##############################################
#Route for choropleth map of neighborhoods
##############################################

@app.route("/api/v1.0/choropleth_map_neighborhoods")
def generate_choropleth_map():
# Function to calculate centroid of a polygon
    def calculate_centroid(coords):
        x = [p[0] for p in coords]
        y = [p[1] for p in coords]
        centroid_x = sum(x) / len(coords)
        centroid_y = sum(y) / len(coords)
        return [centroid_y, centroid_x]

    # Read the GeoJSON file
    geojson_file_path = 'Resources/neighbourhoods.geojson'  
    with open(geojson_file_path) as f:
        geojson_data = json.load(f)

    # Read the CSV file
    csv_file_path = 'Resources/updated_summarylist.csv'
    airbnb_data = pd.read_csv(csv_file_path)

    #Extract necessary columns from the CSV
    airbnb_data = airbnb_data[['latitude', 'longitude', 'name','neighbourhood', 'room_type', 'price']]

    # Step 4: Extract polygons and properties from GeoJSON
    features = geojson_data['features']

    polygons = []
    neighborhood_names = []

    for feature in features:
        geometry_type = feature['geometry']['type']
        neighborhood = feature['properties'].get('neighbourhood', 'Unknown')
        
        if geometry_type == 'MultiPolygon':
            for polygon in feature['geometry']['coordinates']:
                # Flatten the polygon coordinates
                flat_polygon = []
                for coord in polygon[0]:
                    flat_polygon.append(coord)
                
                polygons.append(flat_polygon)
                neighborhood_names.append(neighborhood)

    # Convert to DataFrame for Plotly
    neighborhood_df = pd.DataFrame({
        'polygon': polygons,
        'neighborhood': neighborhood_names
    })

    # Create Plotly figure with GeoJSON
    fig = px.choropleth_mapbox(
        neighborhood_df,
        geojson=geojson_data,
        locations='neighborhood',
        featureidkey="properties.neighbourhood",
        color='neighborhood',
        center={"lat": 35.6895, "lon": 139.6917},
        mapbox_style="carto-positron",
        zoom=10,
        opacity=0.5
    )

    fig.update_geos(fitbounds="locations", visible=True)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    # Save the choropleth map as an HTML file
    fig.write_html("Resources/choropleth_map.html")

    # Return the HTML content as a response with the appropriate Content-Type
    return send_file("Resources/choropleth_map.html", mimetype='text/html')

##############################################
#Route for map with dropdown of room type
##############################################
@app.route("/api/v1.0/Tokyo_Airbnb_Map_Room_Type")
def roomtypemap():
    import plotly.graph_objs as go
    from plotly.subplots import make_subplots

    # Read the CSV file
    csv_file_path = 'Resources/updated_summarylist.csv'
    airbnb_data = pd.read_csv(csv_file_path)

    #Extract necessary columns from the CSV
    airbnb_data = airbnb_data[['latitude', 'longitude', 'name','neighbourhood', 'room_type', 'price']]
    airbnb_data['room_type'].value_counts()
    airbnb_home = airbnb_data[airbnb_data['room_type']=='Entire home/apt']
    airbnb_private = airbnb_data[airbnb_data['room_type']=='Private room']
    airbnb_shared = airbnb_data[airbnb_data['room_type']=='Shared room']
    airbnb_hotel = airbnb_data[airbnb_data['room_type']=='Hotel room']

    # Making the text for hoverinfo
    airbnb_home['text'] = airbnb_home.apply(
    lambda row: f"Name: {row['name']}<br>Neighbourhood: {row['neighbourhood']}<br>Price: ¥{row['price']}", axis=1)
    airbnb_private['text'] = airbnb_private.apply(
    lambda row: f"Name: {row['name']}<br>Neighbourhood: {row['neighbourhood']}<br>Price: ¥{row['price']}", axis=1)
    airbnb_shared['text'] = airbnb_shared.apply(
    lambda row: f"Name: {row['name']}<br>Neighbourhood: {row['neighbourhood']}<br>Price: ¥{row['price']}", axis=1)
    airbnb_hotel['text'] = airbnb_hotel.apply(
    lambda row: f"Name: {row['name']}<br>Neighbourhood: {row['neighbourhood']}<br>Price: ¥{row['price']}", axis=1)

    # Create traces for the dropdown
    home = go.Scattermapbox(
        lat=airbnb_home['latitude'],
        lon=airbnb_home['longitude'],
        mode='markers',
        marker=dict(size=10, color='blue'),
        text=airbnb_home['text'],
        hoverinfo='text',
        name='Entire Homes',
    )
    private = go.Scattermapbox(
        lat=airbnb_private['latitude'],
        lon=airbnb_private['longitude'],
        mode='markers',
        marker=dict(size=10, color='green'),
        text=airbnb_private['text'],
        hoverinfo='text',
        name='Private Rooms',
    )
    shared = go.Scattermapbox(
        lat=airbnb_shared['latitude'],
        lon=airbnb_shared['longitude'],
        mode='markers',
        marker=dict(size=10, color='red'),
        text=airbnb_shared['text'],
        hoverinfo='text',
        name='Shared Rooms',
    )
    hotel = go.Scattermapbox(
        lat=airbnb_hotel['latitude'],
        lon=airbnb_hotel['longitude'],
        mode='markers',
        marker=dict(size=10, color='yellow'),
        text=airbnb_hotel['text'],
        hoverinfo='text',
        name='Hotel Rooms',
    )

    # Create layout with dropdown
    layout = go.Layout(
        title='Airbnb Locations Filtered By Room Type in Tokyo, Japan',
        mapbox=dict(
            style='open-street-map',
            zoom=10,
            center=dict(lat=35.6895, lon=139.6917)
        ),
        updatemenus=[
            {
                'buttons': [
                    {
                        'label': 'Entire Homes/Apts',
                        'method': 'update',
                        'args': [{'visible': [True, False, False, False]}, {'title': 'Entire Homes'}]
                    },
                    {
                        'label': 'Private Rooms',
                        'method': 'update',
                        'args': [{'visible': [False, True, False, False]}, {'title': 'Private Rooms'}]
                    },
                    {
                        'label': 'Shared Rooms',
                        'method': 'update',
                        'args': [{'visible': [False, False, True, False]}, {'title': 'Shared Rooms'}]
                    },
                    {
                        'label': 'Hotel Rooms',
                        'method': 'update',
                        'args': [{'visible': [False, False, False, True]}, {'title': 'Hotel Rooms'}]
                    },
                ],
                'direction': 'down',
                'showactive': True,
            }
        ]
    )

    # Create figure
    ddMap = make_subplots(rows=1, cols=1, subplot_titles=('Interactive Dropdown Map',))
    ddMap.add_trace(home)
    ddMap.add_trace(private)
    ddMap.add_trace(shared)
    ddMap.add_trace(hotel)
    ddMap.update_layout(layout)

    # Return the HTML content of the Plotly map
    return ddMap.to_html(include_plotlyjs='cdn')

if __name__ == "__main__":
    app.run(debug=True)

session.close()
