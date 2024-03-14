from flask import Flask
from flask_redis import FlaskRedis

app = Flask(__name__)
app.config['REDIS_URL'] = 'redis://localhost:6379/0'  # Thay đổi URL kết nối Redis tùy theo cài đặt của bạn
redis_client = FlaskRedis(app)