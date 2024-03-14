from app import redis_client

class FollowAccount:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

# Using **kwargs to accept any number of arguments and then setting the object's attributes based on these arguments using the setattr method.            


    # def __init__(self, id, signal_account_no, signal_account_balance, signal_account_tenant, signal_server_name,
    #              follow_account_no, follow_account_tenant, follow_server_name, investment_id, type, start_balance,
    #              balance, balance_to_withdraw, random_entry, random_volume_from, random_volume_to, copy_rate,
    #              copy_volume, limited_volume, copy_mixes, copy_symbols, is_entry_exist_order, allow_copy,
    #              round_mode, volume_mode, status, is_same_volume, is_round_up):
    #     self.id = id
    #     self.signal_account_no = signal_account_no
    #     self.signal_account_balance = signal_account_balance
    #     self.signal_account_tenant = signal_account_tenant
    #     self.signal_server_name = signal_server_name
    #     self.follow_account_no = follow_account_no
    #     self.follow_account_tenant = follow_account_tenant
    #     self.follow_server_name = follow_server_name
    #     self.investment_id = investment_id
    #     self.type = type
    #     self.start_balance = start_balance
    #     self.balance = balance
    #     self.balance_to_withdraw = balance_to_withdraw
    #     self.random_entry = random_entry
    #     self.random_volume_from = random_volume_from
    #     self.random_volume_to = random_volume_to
    #     self.copy_rate = copy_rate
    #     self.copy_volume = copy_volume
    #     self.limited_volume = limited_volume
    #     self.copy_mixes = copy_mixes
    #     self.copy_symbols = copy_symbols
    #     self.is_entry_exist_order = is_entry_exist_order
    #     self.allow_copy = allow_copy
    #     self.round_mode = round_mode
    #     self.volume_mode = volume_mode
    #     self.status = status
    #     self.is_same_volume = is_same_volume
    #     self.is_round_up = is_round_up

    def save(self):
        redis_client.hmset(f'follow_account:{self.id}', self.__dict__)

    @staticmethod
    def find_by_id(account_id):
        account_data = redis_client.hgetall(f'follow_account:{account_id}')
        if account_data:
            return FollowAccount(**account_data)
        return None
