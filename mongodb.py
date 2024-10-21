from pymongo import MongoClient
from datetime import datetime

class MongoDBManager:
    def __init__(self, db_name, collection_name, uri="mongodb://localhost:27017/"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_or_update_product(self, product):
        product_dict = product.to_dict()

      
        collation = {'locale': 'en', 'strength': 2}
        existing_product = self.collection.find_one({'stock_code': product.stock_code}, collation=collation)


        current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

        if existing_product:
           
            product_dict['updatedAt'] = current_time
            self.collection.update_one(
                {'stock_code': product.stock_code},
                {'$set': product_dict},
                collation=collation
            )
            print(f"Product {product.stock_code} updated at {current_time}.")
        else:
  
            product_dict['createdAt'] = current_time
            product_dict['updatedAt'] = current_time
            self.collection.insert_one(product_dict)
            print(f"Product {product.stock_code} inserted at {current_time}.")

    def close_connection(self):
        self.client.close()
