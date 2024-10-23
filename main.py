from scraper import ProductScraper
from mongodb import MongoDBManager

def main():
    try:
        scraper = ProductScraper('lonca-sample.xml')  # Öncelikle vermiş olduğunuz xml dosyasını buluyorum
        products = scraper.extract_products()  # sonra bu xml dosyasını extract ederek products içine kaydediyorum

        db = MongoDBManager(db_name="ProductDB", collection_name="Products") # MongoDB üstünde ProductDB adında bir database açıyorum ve Products koleksiyonu açıyorum ürünleri Products koleksiyonuna kayıt edeceğim

   
        for product in products:
            db.insert_or_update_product(product) # for ile bütün products ürünlerini dönüp teker teker databaseye ekliyorum bu işlemi yaparken insert_or_update_product adındaki fonksiyonu çağırıyorum

        db.close_connection() #Bütün işlemlerden sonra database bağlantısını kapatıyorum
    except:
        print(f"An error occurred: {e}")
    finally:
        db.close_connection() # sorunlu işlem olsa bile bağlantı kapanmalı

if __name__ == "__main__":
    main()
