class Product:
    # burdaki init kısmı Product sınıfını tanımlamak amacıyla yapıldı yani burası constructor kısmı. Uygulama çalıştığı zaman constructor sadece 1 defa çalışır. Amaç xml yapısından gelecek olan değerlerin nesnenin fieldlarını oluşturmasıdır. Vermiş oldugunuz örnek JSON yapısında USD ve Active statik oldugu için kendi elimle ekledim.
    def __init__(self, stock_code, name, images, price, discounted_price, product_type, quantity, color, series, fabric, model_measurements, product_measurements, is_discounted, price_unit="USD", status="Active"):
        self.stock_code = stock_code
        self.name = name
        self.images = images
        self.price = price
        self.discounted_price = discounted_price
        self.is_discounted = is_discounted
        self.product_type = product_type
        self.quantity = quantity
        self.color = color
        self.series = series
        self.fabric = fabric
        self.model_measurements = model_measurements
        self.product_measurements = product_measurements
        self.price_unit = price_unit
        self.status = status
    
    def to_dict(self): # burda ise gelen değerlerin fieldlarını belirledikten sonra uygun JSON formatına getirmek amacıyla dict yani dictionary haline getirilir.
        return {
            'stock_code': self.stock_code,
            'name': self.name,
            'images': self.images,
            'price': self.price,
            'discounted_price': self.discounted_price,
            'is_discounted': self.is_discounted,
            'product_type': self.product_type,
            'quantity': self.quantity,
            'color': self.color,
            'series': self.series,
            'fabric': self.fabric,
            'model_measurements': self.model_measurements,
            'product_measurements': self.product_measurements,
            'price_unit': self.price_unit,
            'status': self.status
        }
