from orderbookbase import *

class OrderBook_cbx(OrderBookBase):
  def config(self):
    self.market = "cbx"
    self.shortmarketname = "cbx"

    if not (self.cur2 in ["USD"]) or self.cur1!="BTC":
      raise(Exception("Symbol {symbol} not supported".format(symbol=self.symbol)))
      #raise(Exception("BTCUSD or BTCUSD"))

    self.url = "http://campbx.com/api/xdepth.php"
    
  def convert_to_DataFrame(self):
    cur1_amount = "{cur1}_amount".format(cur1=self.cur1.lower())
    columns = ['price', cur1_amount]
        
    self.orders['asks'] = pd.DataFrame(self.data['Asks'], columns=columns)
    self.orders['bids'] = pd.DataFrame(self.data['Bids'], columns=columns)
    
    self.convert_data() # convert unicode to float