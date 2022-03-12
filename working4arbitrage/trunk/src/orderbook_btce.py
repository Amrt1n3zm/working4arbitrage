from orderbookbase import *

class OrderBook_btce(OrderBookBase):
  def config(self):
    self.market = "btce"
    self.shortmarketname = "btce"

    self.url = "https://btc-e.com/api/2/{cur1}_{cur2}/depth".format(cur1=self.cur1.lower(), cur2=self.cur2.lower())

  def convert_to_DataFrame(self):
    columns=['price', "{cur1}_amount".format(cur1=self.cur1.lower())]
    self.orders['asks'] = pd.DataFrame(self.data['asks'], columns=columns)
    self.orders['bids'] = pd.DataFrame(self.data['bids'], columns=columns)
