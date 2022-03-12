from orderbookbase import *

class OrderBook_bitme(OrderBookBase):
  def config(self):
    self.market = "bitme"
    self.shortmarketname = "bitme"

    if self.cur2!="USD" or self.cur1!="BTC":
      raise(Exception("BTCUSD only"))

    self.url = "https://bitme.com/rest/orderbook/{cur1}{cur2}".format(cur1=self.cur1, cur2=self.cur2)

  def convert_to_DataFrame(self):
    cur1_amount = "{cur1}_amount".format(cur1=self.cur1.lower())
    columns=['price', cur1_amount]
    
    self.orders['asks'] = pd.DataFrame(self.data['orderbook']['asks'])
    self.orders['bids'] = pd.DataFrame(self.data['orderbook']['bids'])
    
    # Rename columns
    columns={
      'rate': 'price',
      'quantity': "{cur1}_amount".format(cur1=self.cur1.lower())
    }
    self.orders['asks'] = self.orders['asks'].rename(columns=columns)
    self.orders['bids'] = self.orders['bids'].rename(columns=columns)
    
    # convert unicode to float
    self.orders['asks']['price'] = self.orders['asks']['price'].map(float)
    self.orders['asks'][cur1_amount] = self.orders['asks'][cur1_amount].map(float)
    self.orders['bids']['price'] = self.orders['bids']['price'].map(float)
    self.orders['bids'][cur1_amount] = self.orders['bids'][cur1_amount].map(float)
    
    # sort ask price ascending / bid price descending
    #self.orders['asks'] = self.orders['asks'].sort_index(ascending=True)
    #self.orders['bids'] = self.orders['bids'].sort_index(ascending=False)
    #self.orders['bids'].index = len(self.orders['bids'].index)-1-self.orders['bids'].index
