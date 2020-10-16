from binance.client import Client

class binanceCore:

    def __init__(self, *args, **kwargs):
        a = kwargs.get('apikey',None)
        b = kwargs.get('apisecret',None)
        if a != None  and b != None:
            self.api_key = a
            self.api_secret = b
        else:
            self.api_key     = '3pglz1IibLTrrV0nG5fVDn765hAq2QWN1MoGyhyQBQA0UNvZXxqzNYrftmRXiCh1'
            self.api_secret  = 'gmqxD6BiHvSbr7BYPOYo4kWQFwnhhEg1TtNxrry7Wp2HnTOL7IN1RMAh5BcxtR1m'
        
        
        self.client = Client(self.api_key,self.api_secret)
        self.client.API_URL = 'https://testnet.binance.vision/api'

        self.proxies     = {
        'http': 'http://10.10.1.10:3128',
        'https': 'http://10.10.1.10:1080'
        }


    def get_ping_binance(self):
        print("apikey -> {}, apisecret -> {}".format(self.api_key,self.api_secret))
        return self.client.ping()



    def get_serverTime_binance(self):
        print("apikey -> {}, apisecret -> {}".format(self.api_key,self.api_secret))
        res = self.client.get_server_time()
        return res['serverTime']

    
    def get_systemStatus_binance(self):
        print("apikey -> {}, apisecret -> {}".format(self.api_key,self.api_secret))
        return self.client.get_system_status()
    
    
    def get_exchangeinfo_binance(self):
        return self.client.get_exchange_info()


    def get_symbol_info(self,symbol):
        print("apikey -> {}, apisecret -> {}".format(self.api_key,self.api_secret))
        return self.client.get_symbol_info(symbol)


    def get_products_binance(self):
        return self.client.get_products()