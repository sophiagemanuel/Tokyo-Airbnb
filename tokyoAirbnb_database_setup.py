# Import the dependencies.
import warnings
warnings.filterwarnings('ignore')

from flask import Flask, render_template_string

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func
import numpy as np
import base64

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
                background-color: #fff;
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
                color: #555;
                line-height: 1.6;
            }
            .members, .routes, .data {
                margin: 20px 0;
            }
            .members ul, .routes ul, .data ul {
                list-style-type: none;
                padding: 0;
            }
            .members li, .routes li, .data li {
                background-color: #f1f1f1;
                margin: 5px 0;
                padding: 10px;
                border-radius: 4px;
            }
            .data a {
                color: #1a73e8;
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
                    <li>Sophia</li>
                    <li>Cassidy</li>
                    <li>Amanda</li>
                    <li>Abel</li>
                </ul>
            </div>

            <div class="data">
                <h2>Data</h2>
                <ul>
                    <li><a href="https://www.kaggle.com/datasets/lucamassaron/tokyo-airbnb-open-data-2023?select=reviews.csv" target="_blank">Kaggle Dataset</a></li>
                    <li>summery_listings.csv</li>
                    <li>Neighborhoods.geojson</li>
                </ul>
            </div>

            <div class="github">
                <h2>Github Repository</h2>
                <p><a href="https://github.com/sophiagemanuel/Tokyo-Airbnb" target="_blank">https://github.com/sophiagemanuel/Tokyo-Airbnb</a></p>
            </div>
            
            <div class = "routes">
                <h2>Visualization Routes</h2>
                <ul>
                    <li>/api/v1.0/Listings_Counts_By_Neighborhood</li>
                    <li>"/api/v1.0/Overall_Prices"</li>
                    <li>"/api/v1.0/Price_Distribution_Top15_Neighborhoods"</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    """)

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
        <title>Histogram of Airbnb Prices in Tokyo, Japan</title>
    </head>
    <body>
        <h1>Histogram of Airbnb Prices in Tokyo, Japan</h1>
        <img src="data:image/png;base64,{image_base64}" alt="Histogram of Airbnb Prices in Tokyo, Japan">
    </body>
    </html>
    """
    return render_template_string(html_content)

#Route for boxplot showing price distribution for top 15 neighborhoods
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


if __name__ == "__main__":
    app.run(debug=True)

session.close()
