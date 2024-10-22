import xml.etree.ElementTree as ET
import re
import html  
from product import Product

class ProductScraper:
    def __init__(self, xml_file):
        self.tree = ET.parse(xml_file)
        self.root = self.tree.getroot()

    def extract_products(self):
        products = []
        for item in self.root.findall('Product'): # burda XML yapısındaki her bir Product Elemanını tarıyoruz (findall)
            product = Product( # Önceden oluşturduğumuz Product sınıfına göre nesneleri oluşturuyoruz
                stock_code=item.attrib['ProductId'],
                name=item.attrib['Name'].capitalize(), #capitalize ile ilk harfi büyük harfe çevrilir
                images=[img.attrib['Path'] for img in item.find('Images').findall('Image')], #bütün image kısımları dolaşılır 
                price=float(item.find('ProductDetails').find("ProductDetail[@Name='Price']").attrib['Value'].replace(',', '.')), # burda vermiş oldugunuz JSON formatında fiyat kısmı nokta ile verildiği için nokta yapıldı
                discounted_price=float(item.find('ProductDetails').find("ProductDetail[@Name='DiscountedPrice']").attrib['Value'].replace(',', '.')), #Aynı şekilde indirimli fiyaat içinde nokta yapıldı
                is_discounted=self.is_discounted(item), # fonksiyon çağırıyorum aşağıda açıklıyorum fonksiyonu
                product_type=item.find('ProductDetails').find("ProductDetail[@Name='ProductType']").attrib['Value'],
                quantity=int(item.find('ProductDetails').find("ProductDetail[@Name='Quantity']").attrib['Value']),
                color=[item.find('ProductDetails').find("ProductDetail[@Name='Color']").attrib['Value']],
                series=item.find('ProductDetails').find("ProductDetail[@Name='Series']").attrib['Value'],
                fabric=self.extract_fabric(item),
                model_measurements=self.extract_model_measurements(item),
                product_measurements=self.extract_product_measurements(item)
            )
            products.append(product) # Hepsi products içine eklendi 
        return products

    def is_discounted(self, item): # bu fonksiyonda amaç indirimli fiyat ile normal fiyat kıyaslaması yapılır 
        price = float(item.find('ProductDetails').find("ProductDetail[@Name='Price']").attrib['Value'].replace(',', '.'))
        discounted_price = float(item.find('ProductDetails').find("ProductDetail[@Name='DiscountedPrice']").attrib['Value'].replace(',', '.'))
        return discounted_price < price # eğer indirimli fiyat normal fiyattan küçük ise true değil ise false dönecektir. 

    def extract_fabric(self, item):
        description = item.find('Description').text
        if 'Kumaş Bilgisi:' in description:
            try:
                fabric_info = description.split('Kumaş Bilgisi:')[1].split('</li>')[0].strip()
                return self.clean_html(fabric_info)
            except IndexError:
                return None
        return None

    def extract_model_measurements(self, item): 
        description = item.find('Description').text
        if 'Model Ölçüleri:' in description:
            try:
                model_info = description.split('Model Ölçüleri:')[1].split('</li>')[0].strip()
                return self.clean_html(model_info)
            except IndexError:
                return None
        return None

    def extract_product_measurements(self, item): # burda gelen  açıklamada bazı bilgiler HTML ile geldi amaç o HTML yapılarını temizlemekti.
        description = item.find('Description').text
        if 'Ürün Ölçüleri' in description:
            try:
                product_info = description.split('Ürün Ölçüleri:')[1].split('</li>')[0].strip()
                return self.clean_html(product_info)
            except IndexError:
                return None
        return None

    def clean_html(self, raw_text):
  
        clean = re.compile('<.*?>')
        no_tags = re.sub(clean, '', raw_text)
        clean_text = html.unescape(no_tags)
        return clean_text.replace('\xa0', ' ')
