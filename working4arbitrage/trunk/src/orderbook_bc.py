from orderbookbase import *

from datetime import datetime

class OrderBook_bc(OrderBookBase):
  def config(self):
    self.market = "bc"
    self.shortmarketname = "bc"

    if self.cur2 not in ["USD", "EUR", "GBP"] or self.cur1!="BTC":
      raise(Exception("Symbol {symbol} not supported".format(symbol=self.symbol)))

    self.url = "https://bitcoin-central.net/api/v1/depth/{cur2}".format(cur2=self.cur2)

  def convert_to_DataFrame(self):
    cur1_amount = "{cur1}_amount".format(cur1=self.cur1.lower())
    columns = ['price', 'currency', cur1_amount, 'timestamp']
            
    self.orders['asks'] = pd.DataFrame(self.data['asks'])
    self.orders['bids'] = pd.DataFrame(self.data['bids'])

    # Rename columns (at least ['price', cur1_amount])
    self.orders['asks'] = self.orders['asks'].rename(columns={'amount': "{cur1}_amount".format(cur1=self.cur1.lower())})
    self.orders['bids'] = self.orders['bids'].rename(columns={'amount': "{cur1}_amount".format(cur1=self.cur1.lower())})

    # Cast
    self.convert_data() # convert unicode to float
    try:
      self.orders['asks']['timestamp'] = self.orders['asks']['timestamp'].map(datetime.utcfromtimestamp) # cast unixtime to python datetime
    except:
      print("Can't convert timestamp for asks")
    
    try:
      self.orders['bids']['timestamp'] = self.orders['bids']['timestamp'].map(datetime.utcfromtimestamp) # cast unixtime to python datetime
    except:
      print("Can't convert timestamp for bids")