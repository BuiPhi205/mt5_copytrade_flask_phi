from app import redis_client

class Product:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def save(self):
        data = {key: getattr(self, key) for key in vars(self) if not key.startswith('_')}
        redis_client.hmset(f'product:{self.id}', data)

    @staticmethod
    def find_by_id(product_id):
        data = redis_client.hgetall(f'product:{product_id}')
        if data:
            return Product(**data)
        return None

    @staticmethod
    def find_by_name(product_name):
        product_id = redis_client.get(f'product_name:{product_name}')
        if product_id:
            return Product.find_by_id(product_id.decode())
        return None
