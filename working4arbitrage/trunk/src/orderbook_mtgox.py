from orderbookbase import *

class OrderBook_mtgox(OrderBookBase):
  def config(self):
    self.market = "mtgox"
    self.shortmarketname = "mtgox"

    #self.url = "https://mtgox.com/api/1/{cur1}{cur2}/fulldepth".format(cur1=self.cur1, cur2=self.cur2)
    #self.data['return']['asks']
    
    self.url = "https://data.mtgox.com/api/2/{cur1}{cur2}/money/fulldepth".format(cur1=self.cur1, cur2=self.cur2)
    #self.data['data']['asks']

  def convert_to_DataFrame(self):
    # API v2
    if self.data['result']=='success':
      self.orders['asks'] = pd.DataFrame(self.data['data']['asks'])
      self.orders['bids'] = pd.DataFrame(self.data['data']['bids'])
      
      # Rename columns
      self.orders['asks'] = self.orders['asks'].rename(columns={'amount': "{cur1}_amount".format(cur1=self.cur1.lower())})
      self.orders['bids'] = self.orders['bids'].rename(columns={'amount': "{cur1}_amount".format(cur1=self.cur1.lower())})
     
      # Keep only useful columns
      # ToDo ,btc_amount,amount_int,price,price_int,stamp
      self.orders['asks'] = self.orders['asks'][['price', "{cur1}_amount".format(cur1=self.cur1.lower())]]
      self.orders['bids'] = self.orders['bids'][['price', "{cur1}_amount".format(cur1=self.cur1.lower())]]
      
      # inverser sens pour cumsum
      #self.orders['bids'] = self.orders['bids'].sort_index(ascending=False) # inverser sens pour cumsum
      #self.orders['bids'].index = len(self.orders['bids'].index)-1-self.orders['bids'].index
    else:
      raise Exception("Can't convert to DataFrame")

    """
    # API v1
    if self.data['result']=='success':
      self.orders['asks'] = pd.DataFrame(self.data['return']['asks'])
      self.orders['bids'] = pd.DataFrame(self.data['return']['bids'])
      
      # Rename columns
      self.orders['asks'] = self.orders['asks'].rename(columns={'amount': "{cur1}_amount".format(cur1=self.cur1.lower())})
      self.orders['bids'] = self.orders['bids'].rename(columns={'amount': "{cur1}_amount".format(cur1=self.cur1.lower())})
      
      # Keep only useful columns
      # ToDo ,btc_amount,amount_int,price,price_int,stamp
      self.orders['asks'] = self.orders['asks'][['price', "{cur1}_amount".format(cur1=self.cur1.lower())]]
      self.orders['bids'] = self.orders['bids'][['price', "{cur1}_amount".format(cur1=self.cur1.lower())]]
      
      # inverser sens pour cumsum
      #self.orders['bids'] = self.orders['bids'].sort_index(ascending=False) # inverser sens pour cumsum
      #self.orders['bids'].index = len(self.orders['bids'].index)-1-self.orders['bids'].index
    else:
      raise Exception("Can't convert to DataFrame")
    """