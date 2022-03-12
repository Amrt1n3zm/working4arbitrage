from orderbookbase import *

class OrderBook__model(OrderBookBase):
  def config(self):
    self.market = "_model"
    self.shortmarketname = "_model"

    #if self.cur2!="EUR" or self.cur1!="BTC":
    #  raise(Exception("BTCUSD only"))
    if not (self.cur2 in ["USD", "EUR"]) or self.cur1!="BTC":
      raise(Exception("Symbol {symbol} not supported".format(symbol=self.symbol)))
      #raise(Exception("BTCUSD or BTCUSD"))

    self.url = "https://www.....json"
    
    raise(Exception("ToDo"))

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