from scraper import ProductScraper
from mongodb import MongoDBManager

def main():
  
    scraper = ProductScraper('lonca-sample.xml')  
    products = scraper.extract_products() 

    db = MongoDBManager(db_name="ProductDB", collection_name="Products")

   
    for product in products:
        db.insert_or_update_product(product) 

    db.close_connection()

if __name__ == "__main__":
    main()
