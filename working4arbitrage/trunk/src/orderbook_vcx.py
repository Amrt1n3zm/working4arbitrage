from orderbookbase import *

class OrderBook_vcx(OrderBookBase):
  def config(self):
    self.market = "vcx"
    self.shortmarketname = "vcx"

    #self.symbols_allowed = ['BTC/EUR', 'BTC/USD', 'DVC/BTC', 'IXC/BTC', 'LTC/BTC', 'NMC/BTC', 'PPC/BTC', 'SC/BTC', 'TRC/BTC', 'EUR/USD']
    #self.symbols_allowed = ['BTC/EUR', 'BTC/USD', 'DVC/BTC', 'IXC/BTC', 'LTC/BTC', 'NMC/BTC', 'PPC/BTC', 'SC/BTC', 'TRC/BTC', 'EUR/USD']
    # swap

    #if not (self.cur2 in ["USD", "EUR"]) or self.cur1!="BTC": #'BTC', 'DVC', 'GG', 'I0C', 'IXC', 'LQC', 'LTC', 'NMC', 'PPC', 'SC', 'TRC'
    #  raise(Exception("BTCUSD or BTCUSD"))
    #if not self.symbol in self.symbols_allowed:
    #  raise(Exception("{symbol} not allowed ; use only {symbols_allowed}".format(symbol=self.symbol, symbols_allowed=self.symbols_allowed)))
      
    self.url = "https://vircurex.com/api/orderbook.json?base={cur1}&alt={cur2}".format(cur1=self.cur1, cur2=self.cur2)

  def convert_to_DataFrame(self):
    cur1_amount = "{cur1}_amount".format(cur1=self.cur1.lower())
    columns = ['price', cur1_amount]
    
    try:
      self.orders['asks'] = pd.DataFrame(self.data['asks'], columns=columns)
    except:
      self.orders['asks'] = pd.DataFrame(columns=columns)
    
    try:
      self.orders['bids'] = pd.DataFrame(self.data['bids'], columns=columns)
    except:
      self.orders['bids'] = pd.DataFrame(columns=columns)
    
    self.convert_data() # convert unicode to float
