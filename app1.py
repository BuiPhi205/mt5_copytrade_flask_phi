import MetaTrader5 as mt5
from flask import Flask

import pdb

app = Flask(__name__)

# Khởi tạo kết nối tới MetaTrader 5 terminal
    
if not mt5.initialize():
    print("Không thể kết nối tới terminal MetaTrader 5")
    quit()

# Kết nối tới tài khoản giao dịch
account = 10001282017
password = "CsAx*a5w"
server = "MetaQuotes-Demo"

authorized = mt5.login(account, password=password, server=server)
if authorized:
    print("Kết nối thành công với tài khoản #{}".format(account))
else:
    print("Đăng nhập thất bại vào tài khoản #{}, mã lỗi: {}".format(account, mt5.last_error()))
    mt5.shutdown()
    quit()

pdb.set_trace()

# Gửi lệnh mua vào một cặp tiền tệ cụ thể
symbol = "USDJPY"
symbol_info = mt5.symbol_info(symbol)
if symbol_info is None:
    print("{} không tồn tại, không thể gửi lệnh mua".format(symbol))
    mt5.shutdown()
    quit()

if not symbol_info.visible:
    print("{} không hiển thị, thử chọn hiển thị".format(symbol))
    if not mt5.symbol_select(symbol, True):
        print("symbol_select({}) thất bại, thoát".format(symbol))
        mt5.shutdown()
        quit()

lot = 0.1
point = mt5.symbol_info(symbol).point
price = mt5.symbol_info_tick(symbol).ask
deviation = 20

request = {
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

result = mt5.order_send(request)
pdb.set_trace()

# Kiểm tra kết quả thực hiện
if result.retcode == mt5.TRADE_RETCODE_DONE:
    print("Gửi lệnh thành công từ tài khoản:", result.request)
else:
    print("Gửi lệnh thất bại với mã lỗi:", result.retcode)

# Đóng kết nối tới terminal MetaTrader 5
mt5.shutdown()
