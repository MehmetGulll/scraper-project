from pymongo import MongoClient
from datetime import datetime

class MongoDBManager:
    def __init__(self, db_name, collection_name, uri="mongodb://localhost:27017/"): # Bağlantı girdilerini oluşturuyoruz
        self.client = MongoClient(uri) # bağlantı adresi: bağlantı burdaki adresten kurulur 
        self.db = self.client[db_name] # database adı 
        self.collection = self.db[collection_name] # belirleyeceğimiz database koleksiyonu

    def insert_or_update_product(self, product): # bu fonksiyon hem ekleme hem güncelleme işlemini yapmaktadır. 
        #burası main.py kısmında for ile döndüğümüz product nesneleridir. Product sınıfından gelir dict ise mongoDB formatına uygun düzenlenmesi için oluşşturulan JSON formatı
        product_dict = product.to_dict() 

      # burada strength:2 yapılma sebebi küçük büyük harfe duyarlı olmaması için yapıldı. Yani xml yapısından herhangi bir güncelleme de küçük büyük harfe göre karşılaştırma yapmaması için yapıldı
        collation = {'locale': 'en', 'strength': 2} # collation metin karşılaştırmalarının nasıl yapıldıgını bize söyler.
        existing_product = self.collection.find_one({'stock_code': product.stock_code}, collation=collation) # burda amaç tekrar uygulama çalıştıgında stock_code kısmına göre bir karşılaştırma yapılır yani daha önceden böyle bir stock_code ile eşleşen ürün var mı


        current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z' #bu satır sizin örnek olarak vermiş olduğunuz JSON formatındaki ISO 8601 formatına benzetme amaçlı kullanılmıştır.

        if existing_product: # daha önce collation göre yaptıgımız eşleşmede eşleşen bir ürün varsa 
           
            product_dict['updatedAt'] = current_time # program tekrar çalıştıgı için güncellenme zamanı ekliyoruz 
            self.collection.update_one(
                {'stock_code': product.stock_code}, # update_one ile değişmiş olan değer product_dict ten hangisi ise o güncellenir 
                {'$set': product_dict},
                collation=collation
            )
            print(f"Product {product.stock_code} updated at {current_time}.")
        else:
  
            product_dict['createdAt'] = current_time # eğer ürün ilk defa oluşuyorsa yani existing_product yok ise oluşturulma zamanıda createdAt kısmıda eklensin.
            product_dict['updatedAt'] = current_time
            self.collection.insert_one(product_dict)
            print(f"Product {product.stock_code} inserted at {current_time}.")

    def close_connection(self):
        self.client.close() #mongoDB bağlantısını kapat komutu verilir.
