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



    """
        General Data Endpoint
    """


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


    """
        Market Data Endpoint
    """


    def get_order_book_binance(self,symbol,limit=None):
        if limit != None and limit > 100 and limit < 1000 :
            return self.client.get_order_book(symbol=symbol)
        else:    
            return self.client.get_order_book(symbol=symbol)


    def get_recent_trades_binance(self,symbol, limit=None):
        if limit != None and limit < 500 and limit > 0 :
            return self.client.get_recent_trades(symbol=symbol)
        else:
            return self.client.get_recent_trades(symbol=symbol)


    def get_historical_trades_binance(self,symbol,limit=None):
        if limit != None and limit < 500 and limit > 0 :
            return self.client.get_historical_trades(symbol=symbol,limit=limit)
        else:
            return self.client.get_historical_trades(symbol=symbol)

    
    def get_aggregate_trades_binance(self,symbol,limit):
        if limit != None and limit < 500 and limit > 0 :
            return self.client.get_aggregate_trades(symbol=symbol,limit=limit)
        else:
            return self.client.get_aggregate_trades(symbol=symbol)


    def get_klines_binance(self,symbol,interval):
        return  self.client.get_klines(symbol=symbol,interval=interval)


    def get_historical_klines_binance(self,symbol,interval):
        return self.client.get_historical_klines(symbol=symbol,interval=interval)


    def get_avg_price_binance(self,symbol):
        return self.client.get_avg_price(symbol=symbol)


    def get_ticker_binance(self,symbol):
        return self.client.get_ticker(symbol=symbol)

    
    def get_all_tickers_binance(self):
        return self.client.get_all_tickers()

    
    def get_orderbook_tickers_binance(self):
        return self.client.get_orderbook_tickers()