from orderbookbase import *

class OrderBook_bitcurex(OrderBookBase):
  def config(self):
    self.market = "bitcurex"
    self.shortmarketname = "bitcurex"

    if self.cur2 not in ["EUR", "PLN", "USD"] or self.cur1!="BTC":
      raise(Exception("BTCEUR BTCPLN BTCUSD only"))

    self.url = "https://{cur2}.bitcurex.com/data/orderbook.json".format(cur2=self.cur2.lower())
    # ToFix BTCUSD http://bitcurex.us/ ???

  def convert_to_DataFrame(self):
    cur1_amount = "{cur1}_amount".format(cur1=self.cur1.lower())
    columns = ['price', cur1_amount]
        
    self.orders['asks'] = pd.DataFrame(self.data['asks'], columns=columns)
    self.orders['bids'] = pd.DataFrame(self.data['bids'], columns=columns)
    
    # convert unicode to float
    self.orders['asks']['price'] = self.orders['asks']['price'].map(float)
    self.orders['asks'][cur1_amount] = self.orders['asks'][cur1_amount].map(float)
    self.orders['bids']['price'] = self.orders['bids']['price'].map(float)
    self.orders['bids'][cur1_amount] = self.orders['bids'][cur1_amount].map(float)
