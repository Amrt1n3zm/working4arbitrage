from orderbookbase import *

class OrderBook_btc24(OrderBookBase):
  def config(self):
    self.market = "btc24"
    self.shortmarketname = "btc24"

    if not (self.cur2 in ["USD", "EUR"]) or self.cur1!="BTC":
      raise(Exception("BTCUSD or BTCUSD"))

    self.url = "https://bitcoin-24.com/api/{cur2}/orderbook.json".format(cur2=self.cur2)

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
