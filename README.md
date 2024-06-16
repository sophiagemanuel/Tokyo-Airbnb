# Tokyo-Airbnb
## Project Three
With the rise in travel post-pandemic and increased popularity of unique Airbnb accomodations, we explore the best locations and prices for Airbnbs in Tokyo, Japan.

Presented by Abel Dumecha, Amanda Liu, Cassidy Schultheis, and Sophia Emanuel.

## GitHub Repository

[Tokyo-Airbnb](https://github.com/sophiagemanuel/Tokyo-Airbnb)


## Data Sources
- Found in the 'Resources' file
- [Kaggle Dataset: Tokyo Airbnb Open Data 2023](https://www.kaggle.com/datasets/lucamassaron/tokyo-airbnb-open-data-2023?select=reviews.csv)
- Summary_listings.csv
- Cholorpleth_map.html

## Data Transforming/Cleaning/Storage for Summary_listings.csv
  - Removed unnecessary columns:  neighborhood_group, last_reviewed, calculated_host_listing_count, number_of_reviews_ltm, and license.
  - Extracted and created new columns for review, bed/bedrooms, and baths.
  - Uploaded cleaned csv file as 'updated_summarylist.csv' and uploaded the data into a SQLite file named 'tokyoAirbnb.sqlite'
 
 ## Visualizations and Interactivity
    - Flask App with different rounds showing a map (using Leaflets.js) with filterable dropdown menus.
    - Heatmap of Prices by Neighborhoos, wisualizing the price differences using Plotly.
    - Box plot of Prices by Neighborhood, displaying the price variation using Seaborn.
    - Histogram of Prices using Seaborn to show overall price distribution.
    - Bar Chart of Neighborhoods versus the Listing Count, using MatplotLib to identify the neighborhoods with the most listings.
