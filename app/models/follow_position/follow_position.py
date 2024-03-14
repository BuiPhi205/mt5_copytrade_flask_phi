from flask import Flask
from redis import Redis

app = Flask(__name__)
redis = Redis(host='localhost', port=6379)

class FollowPosition:
    def __init__(self, signal_position_no=None, signal_position_id=None,
                 follow_account_no=None, follow_position_no=None, follow_account_tenant=None,
                 follow_account_id=None, follow_server_name=None,
                 copy_type=None, symbol=None, start_volume=None, remain_volume=None,
                 volume_close_before_withdraw=None, copy_rate=None, type=None, status=None):
        self.signal_position_no = signal_position_no
        self.signal_position_id = signal_position_id
        self.follow_account_no = follow_account_no
        self.follow_position_no = follow_position_no
        self.follow_account_tenant = follow_account_tenant
        self.follow_account_id = follow_account_id
        self.follow_server_name = follow_server_name
        self.copy_type = copy_type
        self.symbol = symbol
        self.start_volume = start_volume
        self.remain_volume = remain_volume
        self.volume_close_before_withdraw = volume_close_before_withdraw
        self.copy_rate = copy_rate
        self.type = type
        self.status = status

    def after_create(self):
        # Thực hiện các hành động sau khi tạo
        pass

    @classmethod
    def by_follower_and_server(cls, follow_account_no, follow_position_no, server):
        return cls.query.filter_by(follow_account_no=follow_account_no,
                                    follow_position_no=follow_position_no,
                                    follow_server_name=server).all()

    @classmethod
    def by_follow_account_id_and_status(cls, follow_account_id, status):
        return cls.query.filter_by(follow_account_id=follow_account_id, status=status).all()

    @classmethod
    def by_signal_position_id_and_status(cls, signal_position_id, status):
        return cls.query.filter_by(signal_position_id=signal_position_id, status=status).all()

    @classmethod
    def process_positions_related_to_follower(cls, follow_account_id):
        return cls.query.filter_by(follow_account_id=follow_account_id, status='PROCESS').all()

    @classmethod
    def by_follower_and_signal_position(cls, follow_account_no, follow_account_tenant, signal_position_no):
        return cls.query.filter_by(follow_account_no=follow_account_no,
                                    follow_account_tenant=follow_account_tenant,
                                    signal_position_no=signal_position_no).all()

    def get_opposite_type(self):
        if self.type == MtOrderType.OP_BUY:
            return MtOrderType.OP_SELL
        elif self.type == MtOrderType.OP_SELL:
            return MtOrderType.OP_BUY

if __name__ == '__main__':
    app.run(debug=True)
