# Scraper Pipeline

This project scrapes product data from an XML file and inserts it into a MongoDB collection. The data is transformed to match a predefined schema and ensures no duplicate entries on subsequent executions.

# Features
Extracts product data (e.g., stock code, name, price, images) from XML.
Cleans and formats the data (e.g., removing HTML tags, capitalizing product names).
Inserts or updates products in MongoDB, ensuring no duplicates.
Modular and object-oriented code for easy maintenance and extension.

## Setup

1. Install dependencies:
pip install pymongo
2. Run the scraper:
3. MongoDB should be running locally or update the MongoDB URI in `mongodb.py`.