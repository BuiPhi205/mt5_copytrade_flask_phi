import MetaTrader5 as mt5
from flask import Flask, request, jsonify
import pdb

app = Flask(__name__)

# Route cho trang chính
@app.route('/')
def hello():
    return 'Hello, World!'

# Route cho action login
@app.route('/login', methods=['POST'])
def login():
    account = request.json.get('account')
    password = request.json.get('password')
    server = request.json.get('server')

    if not mt5.initialize():
        return jsonify({'error': 'Không thể kết nối tới terminal MetaTrader 5'}), 500

    authorized = mt5.login(account, password=password, server=server)
    if authorized:
        return jsonify({'message': 'Kết nối thành công với tài khoản #{}'.format(account)})
    else:
        return jsonify({'error': 'Đăng nhập thất bại vào tài khoản #{}'.format(account), 'error_code': mt5.last_error()}), 401

# Route để gửi lệnh mua
@app.route('/send_order', methods=['POST'])
def send_order():
    symbol = request.json.get('symbol')
    lot = request.json.get('lot')

    if not mt5.initialize():
        return jsonify({'error': 'Không thể kết nối tới terminal MetaTrader 5'}), 500

    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        mt5.shutdown()
        return jsonify({'error': '{} không tồn tại, không thể gửi lệnh mua'.format(symbol)}), 404

    if not symbol_info.visible:
        mt5.shutdown()
        return jsonify({'error': '{} không hiển thị, thử chọn hiển thị'.format(symbol)}), 400

    point = mt5.symbol_info(symbol).point
    price = mt5.symbol_info_tick(symbol).ask
    deviation = 20

    request_data = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": price - 100 * point,
        "tp": price + 100 * point,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }

    result = mt5.order_send(request_data)

    if result.retcode == mt5.TRADE_RETCODE_DONE:
        mt5.shutdown()
        return jsonify({'message': 'Gửi lệnh thành công từ tài khoản: {}'.format(result.request)}), 200
    else:
        mt5.shutdown()
        return jsonify({'error': 'Gửi lệnh thất bại với mã lỗi: {}'.format(result.retcode)}), 400

# Route để nhận yêu cầu POST từ Rails
@app.route('/hook/signals', methods=['POST'])
def receive_signal():
    data = request.json  # Trích xuất dữ liệu từ yêu cầu POST
    # Xử lý dữ liệu nhận được từ Rails ở đây
    pdb.set_trace()

    # In ra dữ liệu nhận được từ yêu cầu POST từ Rails
    print("Received data from Rails:", data)

    # Trả về một phản hồi cho Rails
    return jsonify({'status': 'success', 'message': 'Dữ liệu đã được nhận thành công từ Rails'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')