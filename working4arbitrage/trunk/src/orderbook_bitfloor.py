from orderbookbase import *

class OrderBook_bitfloor(OrderBookBase):
  def config(self):
    self.market = "bitfloor"
    self.shortmarketname = "bitfloor"

    if self.cur2!="USD" or self.cur1!="BTC":
      raise(Exception("BTCUSD only"))

    self.url = "https://api.bitfloor.com/book/L2/1"

  def convert_to_DataFrame(self):
    cur1_amount = "{cur1}_amount".format(cur1=self.cur1.lower())
    columns=['price', cur1_amount]
    
    self.orders['asks'] = pd.DataFrame(self.data['asks'], columns=columns)
    self.orders['bids'] = pd.DataFrame(self.data['bids'], columns=columns)
    
    # convert unicode to float
    self.orders['asks']['price'] = self.orders['asks']['price'].map(float)
    self.orders['asks'][cur1_amount] = self.orders['asks'][cur1_amount].map(float)
    self.orders['bids']['price'] = self.orders['bids']['price'].map(float)
    self.orders['bids'][cur1_amount] = self.orders['bids'][cur1_amount].map(float)
