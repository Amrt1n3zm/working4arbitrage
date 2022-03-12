from orderbookbase import *

"""
Intersango
https://intersango.com/
"""

class OrderBook_intrsng(OrderBookBase):
  def config(self):
    self.market = "intrsng"
    self.shortmarketname = "intrsng"

    dct_cur2 = {
      'GBP': 1,
      'EUR': 2,
      'USD': 3,
      'PLN': 4
    }

    if self.cur2 not in dct_cur2 or self.cur1!="BTC":
      raise(Exception("Symbol {symbol} not supported".format(symbol=self.symbol)))
    
    id_cur2 = dct_cur2[self.cur2]

    self.url = "https://intersango.com/api/depth.php?currency_pair_id={id_cur2}".format(id_cur2=id_cur2)
    
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
    
    self.convert_data()