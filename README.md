# Listing Activity of Tokyo Airbnbs
With the rise in travel post-pandemic and increased popularity of unique Airbnb accomodations, we explore the best locations and prices for Airbnbs in Tokyo, Japan.

Presented by Abel Dumecha, Amanda Liu, Cassidy Schultheis, and Sophia Emanuel.

## Data Sources
- Found in the 'Resources' directory
  - [Kaggle Dataset: Tokyo Airbnb Open Data 2023](https://www.kaggle.com/datasets/lucamassaron/tokyo-airbnb-open-data-2023?select=reviews.csv)
  - Summary_listings.csv
  - Neighborhoods.geojson

## Data Transforming/Cleaning/Storage
- Deleted unwanted columns
- Split specific columns (e.g., split name column into separate beds and baths columns)
- Removed unwanted symbols and null values
- Modified data types of certain column values and reordered columns
- Uploaded cleaned CSV file as 'updated_summarylist.csv' and imported the data into a SQLite database named 'tokyoAirbnb.sqlite'.
 
 ## Visualizations and Interactivity
 
We created a Flask App to serve as a welcome page and display our visualiations. <br>
![FlaskAppScreenshot] <br>
A bar chart, created with Matplotlib, displays the number of Airbnb listings by neighborhood in Tokyo, Japan.
![Number of Listings by Neighborhood in Tokyo, Japan](Resources/barchart_of_neighborhoodlistings_in_tokyo.png) <br>

Seaborn was used to design the following visualizations:
- A histogram was developed to illustrate the overall distribution of Airbnb prices in Tokyo, Japan. <br>
![Distribution of Airbnb Prices in Tokyo, Japan](Resources/histogram_of_prices_in_tokyo.png) <br>

- A box and whisker plot was created to visualize the price distributions of the top 15 neighborhoods with the most listings. <br>
![Price Distribution for Top 15 Neighborhoods in Tokyo, Japan](Resources/price_distribution.png)<br>

- To analyze the average prices by neighborhood, we created a heatmap showing the top 15 neighborhoods with the most listings and the average price for each room type. <br>
![Average Price for Top 15 Neighborhoods by Room Type in Tokyo, Japan](Resources/HeatMapTop15AveragePricebyNeighbourhoodandRoomType.png) <br>

- Another heatmap was designed to display the average prices for all neighborhoods by room type.<br>
![Average Price for All Neighborhoods by Room Type in Tokyo, Japan](Resources/HeatMapAllAveragePricebyNeighbourhoodandRoomType.png) <br>

- We created an additional heatmap to show the top 15 neighborhoods with the most listings and the average price based on the number of bedrooms. <br>
![Average Price by Number of Bedrooms and Neighborhood](Resources/HeatMapTop15AveragePricebyNeighborhoodandBedrooms.png) <br>

Ploty was used to develop the following visualizations: <br>

- We developed a choropleth map to visualize each neighborhood in Tokyo, Japan, color-coded by average price. <br>
![Choropleth Map Neighboorhoods](Resources/choropleth_map_neighborhoods.png) <br>

- An interactive map was created to display all Airbnb listings, allowing users to filter by room type via a dropdown menu. <br>
![Airbnb Locations Filtered By Room Type in Tokyo, Japan](Resources/Tokyo_Airbnb_Map_Room_Type.png) <br>

## GitHub Repository

[Tokyo-Airbnb](https://github.com/sophiagemanuel/Tokyo-Airbnb)
