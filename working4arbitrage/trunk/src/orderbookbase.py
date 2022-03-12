import os
import json

import urllib2
import pandas as pd
import numpy as np

import matplotlib as mpl
mpl.use('Agg') # uncomment if no X server
import matplotlib.pylab as plt

import locale

from ticker import Ticker

import json

class OrderBookBase:
  def __init__(self, args, symbol):  
    self.symbol = symbol
    self.args = args

    (self.cur1, self.cur2) = self.symbol.split('/')
    #self.cur1 = "BTC"
    #self.cur2 = "USD"
    #self.pair = "{cur1}{cur2}".format(cur1=self.cur1, cur2=self.cur2)

    self.config()
    self.fullmarketname = "{shortmarketname}{cur1}{cur2}".format(shortmarketname=self.shortmarketname, cur1=self.cur1, cur2=self.cur2)

    if not args.nodownload:
      self.download()
      self.write_json()
    else:
      self.read_json()
    
    if args.printjson:
      self.pretty_print_json()
        
    self.orders = dict()
    self.convert_to_DataFrame()
    self.sort_order_book()

    if args.printmk and args.nocalculate:
      self.print_mk()
        
    if not args.nocalculate:
      self.insert_zero()
      self.calculate()
      if args.printmk:
        self.print_mk()
      if args.showstats:
        self.print_stats()
      if args.plot:
        self.plot()
        
      #if not args.nocalculate:
      #  self.plot()
      #else:
      #  print("Can't plot if you don't calculate")


    self.save_to_csv()
    
  def calculate(self):
    cur1_amount = "{cur1}_amount".format(cur1=self.cur1.lower())
    cur2_amount = "{cur2}_amount".format(cur2=self.cur2.lower())
    cur1_amount_cum = "{cur1_amount}_cum".format(cur1_amount=cur1_amount)
    cur2_amount_cum = "{cur2_amount}_cum".format(cur2_amount=cur2_amount)

    self.orders['asks'][cur1_amount_cum] = self.orders['asks'][cur1_amount].cumsum()
    self.orders['bids'][cur1_amount_cum] = self.orders['bids'][cur1_amount].cumsum()

    self.orders['asks'][cur2_amount] = self.orders['asks'][cur1_amount] * self.orders['asks']['price']
    self.orders['bids'][cur2_amount] = self.orders['bids'][cur1_amount] * self.orders['bids']['price']
    
    self.orders['asks'][cur2_amount_cum] = self.orders['asks'][cur2_amount].cumsum()
    self.orders['bids'][cur2_amount_cum] = self.orders['bids'][cur2_amount].cumsum()

  def print_mk(self):
    print("="*10+" Asks (ascending)"+"="*10)
    print(self.orders['asks'])
    print("="*10+" Bids (descending)"+"="*10)
    print(self.orders['bids'])

  def get_stats(self):
    cur1_amount = "{cur1}_amount".format(cur1=self.cur1.lower())
    cur2_amount = "{cur2}_amount".format(cur2=self.cur2.lower())
    cur1_amount_cum = "{cur1_amount}_cum".format(cur1_amount=cur1_amount)
    cur2_amount_cum = "{cur2_amount}_cum".format(cur2_amount=cur2_amount)
    
    stats = dict()
    stats['nb_bids'] = len(self.orders['bids'])
    stats['nb_asks'] = len(self.orders['asks'])
    
    try:
      stats['bids_cur1_amount_cum_max'] = self.orders['bids'][cur1_amount_cum].max()
    except:
      stats['bids_cur1_amount_cum_max'] = 0
    
    try:
      stats['bids_cur2_amount_cum_max'] = self.orders['bids'][cur2_amount_cum].max()
    except:
      stats['bids_cur2_amount_cum_max'] = 0
    
    try:
      stats['asks_cur1_amount_cum_max'] = self.orders['asks'][cur1_amount_cum].max()
    except:
      stats['asks_cur1_amount_cum_max'] = 0
    
    try:
      stats['asks_cur2_amount_cum_max'] = self.orders['asks'][cur2_amount_cum].max()
    except:
      stats['asks_cur2_amount_cum_max'] = 0
    
    return(stats)
  
  def print_stats(self):    
    stats = self.get_stats()
    
    print("""Total bids ({nb_bids}) :
  {bids_cur2_amount_cum_max} {cur2}
  {bids_cur1_amount_cum_max} {cur1}

Total asks ({nb_asks}):
  {asks_cur1_amount_cum_max} {cur1}
  {asks_cur2_amount_cum_max} {cur2}
""".format(cur1=self.cur1, cur2=self.cur2,
  nb_bids=locale.format("%d", len(self.orders['bids']), grouping=True),
  bids_cur1_amount_cum_max=locale.format("%.2f", stats['bids_cur1_amount_cum_max'], grouping=True),
  bids_cur2_amount_cum_max=locale.format("%.2f", stats['bids_cur2_amount_cum_max'], grouping=True),
  nb_asks=locale.format("%d", len(self.orders['asks']), grouping=True),
  asks_cur1_amount_cum_max=locale.format("%.2f", stats['asks_cur1_amount_cum_max'], grouping=True),
  asks_cur2_amount_cum_max=locale.format("%.2f", stats['asks_cur2_amount_cum_max'], grouping=True)
  ))

  def config(self):
    pass

  def download(self):
    print("Downloading order book (full depth) for {symbol} at {fullmarketname} {url} (please wait)".format(symbol=self.symbol, fullmarketname=self.fullmarketname, url=self.url))
    response = urllib2.urlopen(self.url)
    self.json_data = response.read()
    self.data = json.loads(self.json_data)
    
  def write_json(self):
    filename = os.path.join(self.args.basepath, "data_in/{fullmarketname}.json".format(fullmarketname=self.fullmarketname))
    print(" Writing market data to file \"{filename}\"".format(filename=filename))
    myFile = open(filename, 'w')
    myFile.write(self.json_data)
    myFile.close()

  def read_json(self):
    filename = os.path.join(self.args.basepath, "data_in/{fullmarketname}.json".format(fullmarketname=self.fullmarketname))
    print("Reading order book (full depth) for {symbol} at {fullmarketname} from file \"{filename}\"".format(symbol=self.symbol, fullmarketname=self.fullmarketname, filename=filename))
    myFile = open(filename, 'r')
    self.json_data = myFile.read()
    self.data = json.loads(self.json_data)
    myFile.close()

  def pretty_print_json(self):
    #print(self.data)
    print(json.dumps(self.data, sort_keys=True, indent=2))

  def convert_to_DataFrame(self):
    pass
    
    #print(self.orders)

  def convert_data(self):
    cur1_amount = "{cur1}_amount".format(cur1=self.cur1.lower())
    columns = ['price', cur1_amount]
    
    if len(self.orders['asks'])==0:
      self.orders['asks'] = pd.DataFrame(columns=columns)
    if len(self.orders['bids'])==0:
      self.orders['bids']  = pd.DataFrame(columns=columns)

    #print(self.orders['asks'])
    #print(self.orders['bids'])
    
    # convert unicode to float
    self.orders['asks']['price'] = self.orders['asks']['price'].map(float)
    self.orders['asks'][cur1_amount] = self.orders['asks'][cur1_amount].map(float)
    self.orders['bids']['price'] = self.orders['bids']['price'].map(float)
    self.orders['bids'][cur1_amount] = self.orders['bids'][cur1_amount].map(float)
    
  def sort_order_book(self):
    # sort ask ascending / bid descending
    self.orders['asks'] = self.orders['asks'].sort('price', ascending=True)
    self.orders['asks'].index = np.arange(len(self.orders['asks']))
    self.orders['bids'] = self.orders['bids'].sort('price', ascending=False)
    self.orders['bids'].index = np.arange(len(self.orders['bids']))

  def insert_zero(self):
    pass
    """
    cur1_amount = "{cur1}_amount".format(cur1=self.cur1.lower())
    for dir in ['asks', 'bids']:
      self.orders[dir] = self.orders[dir].shift(1)
      self.orders[dir].ix[0][cur1_amount] = 0.0
      self.orders[dir].ix[0]['price'] = self.orders[dir].ix[1]['price']
    """

    #pass
    """

    #self.orders['asks'] = pd.concat([self.orders['asks'][:1], self.orders['asks']])
    
    #self.orders['asks'] = self.orders['asks'][:1].append(self.orders['asks'])
    """
  
    """
    """
  
  def save_to_csv(self):    
    self.orders['asks'].to_csv(os.path.join(self.args.basepath, "data_out_markets/{fullmarketname}_asks.csv".format(fullmarketname=self.fullmarketname)))
    self.orders['bids'].to_csv(os.path.join(self.args.basepath, "data_out_markets/{fullmarketname}_bids.csv".format(fullmarketname=self.fullmarketname)))

  def plot(self):
    cur1_amount = "{cur1}_amount".format(cur1=self.cur1.lower())
    cur2_amount = "{cur2}_amount".format(cur2=self.cur2.lower())
    cur1_amount_cum = "{cur1_amount}_cum".format(cur1_amount=cur1_amount)
    cur2_amount_cum = "{cur2_amount}_cum".format(cur2_amount=cur2_amount)

    # filter using price
    orders_tmp_lim_price = dict()
    
    #orders_tmp_lim_price['asks'] = self.orders['asks']
    #orders_tmp_lim_price['bids'] = self.orders['bids']
    
    try:
      pmax = float(self.args.pmax)
      pmin = float(self.args.pmin)
    except:
      if len(self.orders['asks'])>0:
        ask_min = self.orders['asks']['price'].min()
      else:
        if len(self.orders['bids'])>0:
          ask_min = self.orders['bids']['price'].min()
        else:
          print("Can't plot")
          return()
      
      if len(self.orders['bids'])>0:
        bid_max = self.orders['bids']['price'].max()
      else:
        if len(self.orders['asks'])>0:
          bid_max = self.orders['asks']['price'].min()
        else:
          print("Can't plot")
          return()
      
      moy = (ask_min + bid_max)/2.0
      pmax = moy + moy * 0.3
      pmin = moy - moy * 0.3
    
    orders_tmp_lim_price['asks'] = self.orders['asks'][self.orders['asks']['price']<=pmax]
    orders_tmp_lim_price['bids'] = self.orders['bids'][self.orders['bids']['price']>=pmin]

    #orders_tmp_lim_price['asks'] = self.orders['asks'][self.orders['asks'][cur1_amount_cum]<=float(self.args.currency1)]
    #orders_tmp_lim_price['bids'] = self.orders['bids'][self.orders['bids'][cur1_amount_cum]<=float(self.args.currency1)]


    # filter using cur2_amount_cum
    #orders_tmp_lim2 = dict()
    #orders_tmp_lim2['asks'] = self.orders['asks'][self.orders['asks'][cur2_amount_cum]<=10000]
    #orders_tmp_lim2['bids'] = self.orders['bids'][self.orders['bids'][cur2_amount_cum]<=10000]

    
    #btc_amount_cum_max = max(orders_tmp['bids']['btc_amount_cum'].max(), orders_tmp['asks']['btc_amount_cum'].max())
    #print(btc_amount_cum_max)
    
    #print(orders_tmp['bids'])
    #print(orders_tmp['asks'])
    
    fig = plt.figure()

    fig.subplots_adjust(bottom=0.1)
    #ax = fig.add_subplot(311)
    ax = fig.add_subplot(211)

    plt.title("{y} = f({x})".format(x='price', y=cur1_amount_cum))
    try:
      pBids, = plt.plot(orders_tmp_lim_price['bids']['price'], orders_tmp_lim_price['bids'][cur1_amount_cum], color='b', marker='.')
    except:
      pBids = None
    
    try:
      pAsks, = plt.plot(orders_tmp_lim_price['asks']['price'], orders_tmp_lim_price['asks'][cur1_amount_cum], color='r', marker='.')
    except:
      pAsks = None
    
    plt.legend([pAsks, pBids], ["Asks", "Bids"]) 

    
    #ax = fig.add_subplot(312)
    ax = fig.add_subplot(212)

    plt.title("{y} = f({x})".format(x='price', y=cur1_amount))
    try:
      pBids, = plt.plot(orders_tmp_lim_price['bids']['price'], orders_tmp_lim_price['bids'][cur1_amount], color='b', marker='.', linestyle='None')
    except:
      pass
    
    try:
      pAsks, = plt.plot(orders_tmp_lim_price['asks']['price'], orders_tmp_lim_price['asks'][cur1_amount], color='r', marker='.', linestyle='None')
    except:
      pass
    # ToDo: histogram instead of dot (see numpy.histogram or pandas.DataFrame.hist)
    plt.legend([pAsks, pBids], ["Asks", "Bids"])
    
    #ax = fig.add_subplot(313)
    #plt.title("{y} = f({x})".format(x=cur1_amount_cum,y=cur2_amount_cum))
    #plt.plot(orders_tmp_lim2['bids'][cur1_amount_cum], orders_tmp_lim2['bids'][cur2_amount_cum], color='b')
    #plt.plot(orders_tmp_lim2['asks'][cur1_amount_cum], orders_tmp_lim2['asks'][cur2_amount_cum], color='r')

    plt.savefig(os.path.join(self.args.basepath, "data_out_markets/{fullmarketname}_order_depth.png".format(fullmarketname=self.fullmarketname)))
    plt.show()

  def bid(self, requested_cur1_amount):
    return(self.how_much('sell', requested_cur1_amount, None)/float(requested_cur1_amount))
    
  def ask(self, requested_cur1_amount):
    return(self.how_much('buy', requested_cur1_amount, None)/float(requested_cur1_amount))

  """
  def ticker(self, requested_cur1_amount):
    ask = self.how_much('buy', requested_cur1_amount, None)/float(requested_cur1_amount)
    bid = self.how_much('sell', requested_cur1_amount, None)/float(requested_cur1_amount)
    #return({'ask': ask, 'bid': bid, 'spread': ask-bid})
    return(Ticker(ask, bid))
  """

  def how_much(self, direction='buy', requested_cur1_amount=None, requested_cur2_amount=None):
    # cur1=btc
    # cur2=eur|usd ...
    cur1 = self.cur1.lower()
    cur2 = self.cur2.lower()
    cur1_amount = "{cur1}_amount".format(cur1=cur1)
    cur2_amount = "{cur2}_amount".format(cur2=cur2)
    cur1_amount_cum = "{cur1_amount}_cum".format(cur1_amount=cur1_amount)
    cur2_amount_cum = "{cur2_amount}_cum".format(cur2_amount=cur2_amount)
    cur1_amount_req = "{cur1_amount}_req".format(cur1_amount=cur1_amount)
    cur2_amount_req = "{cur2_amount}_req".format(cur2_amount=cur2_amount)
    cur1_amount_req_cum = "{cur1_amount}_req_cum".format(cur1_amount=cur1_amount)
    cur2_amount_req_cum = "{cur2_amount}_req_cum".format(cur2_amount=cur2_amount)

    if requested_cur1_amount==None and requested_cur2_amount==None:
      raise Exception("how_much function error 'requested_cur1_amount' and 'requested_cur2_amount' can't be (both) 'None'")
    else:
      if direction=='buy':
        direction_inv = 'sell'
        dir = 1
        price_dir = 'asks'
      elif direction=='sell':
        direction_inv = 'buy'
        dir = -1
        price_dir = 'bids'
      else:
        raise Exception("how_much function error 'direction' should be 'buy' or 'sell'")
    
      orders_tmp = self.orders[price_dir]
    
      if requested_cur1_amount==None: # requested_cur2_amount is given

        #print("""How much {cur1} to {action} {val} {cur2} ?""".format(cur1=self.cur1, cur2=self.cur2, action=direction, val=requested_cur1_amount))

        cur2_amount_max = orders_tmp[cur2_amount].sum()
        if requested_cur2_amount<cur2_amount_max:
          pass
          #print("market is big enough to {direction} {requested_cur2_amount} {cur2} - market size ({direction_inv} offer) is {cur2_amount_max} {cur2}".format(direction=direction, direction_inv=direction_inv, requested_cur2_amount=requested_cur2_amount, cur2_amount_max=cur2_amount_max, cur2=self.cur2))
        else:
          raise Exception("market {market} is not big enough to {direction} {requested_cur2_amount} {cur2} - market size ({direction_inv} offer) is {cur2_amount_max} {cur2}".format(market=self.fullmarketname, direction=direction, direction_inv=direction_inv, requested_cur2_amount=requested_cur2_amount, cur2_amount_max=cur2_amount_max, cur2=self.cur2))
        
        orders_tmp = orders_tmp[(orders_tmp[cur2_amount_cum]<requested_cur2_amount).shift(1).fillna(True)]
        orders_tmp[cur2_amount_req] = orders_tmp[cur2_amount]
        
        currency_overflow = orders_tmp[cur2_amount].sum()-requested_cur2_amount
        orders_tmp[cur2_amount_req][len(orders_tmp)-1] = orders_tmp[cur2_amount_req][len(orders_tmp)-1] - currency_overflow
        orders_tmp[cur2_amount_req_cum] = orders_tmp[cur2_amount_req].cumsum()

        orders_tmp[cur1_amount_req] = orders_tmp[cur2_amount_req] / orders_tmp['price']
        orders_tmp[cur1_amount_req_cum] = orders_tmp[cur1_amount_req].cumsum()

        #print(orders_tmp)

        need_cur1_amount = orders_tmp[cur1_amount_req].sum()
        #print("price (avg): {price_avg}".format(price_avg = requested_cur2_amount/need_cur1_amount))
        
        orders_tmp.to_csv(os.path.join(self.args.basepath, "data_out_markets/{fullmarketname}_{dir}_request.csv".format(fullmarketname=self.fullmarketname, dir=direction)))
        
        return(need_cur1_amount) # btc_amount

      elif requested_cur2_amount==None: # requested_cur1_amount is given

        #print("""How much {cur2} to {action} {val} {cur1} ?""".format(cur1=self.cur1, cur2=self.cur2, action=direction, val=requested_cur1_amount))

        cur1_amount_max = orders_tmp[cur1_amount].sum()
        
        if requested_cur1_amount<cur1_amount_max:
          pass
          #print("market is big enough to {direction} {requested_cur1_amount} {cur1} - market size ({direction_inv} offer) is {cur1_amount_max} {cur1}".format(direction=direction, direction_inv=direction_inv, requested_cur1_amount=requested_cur1_amount, cur1_amount_max=cur1_amount_max, cur1=self.cur1))
        else:
          raise Exception("market {market} is not big enough to {direction} {requested_cur1_amount} {cur1} - market size ({direction_inv} offer) is {cur1_amount_max} {cur1}".format(market=self.fullmarketname, direction=direction, direction_inv=direction_inv, requested_cur1_amount=requested_cur1_amount, cur1_amount_max=cur1_amount_max, cur1=self.cur1))
        
        orders_tmp = orders_tmp[(orders_tmp[cur1_amount_cum]<requested_cur1_amount).shift(1).fillna(True)]
        orders_tmp[cur1_amount_req] = orders_tmp[cur1_amount]

        btc_overflow = orders_tmp[cur1_amount].sum()-requested_cur1_amount
        #print(btc_overflow)
        
        #print(orders_tmp)
        
        orders_tmp[cur1_amount_req][len(orders_tmp)-1] = orders_tmp[cur1_amount_req][len(orders_tmp)-1] - btc_overflow
        
        orders_tmp[cur1_amount_req_cum] = orders_tmp[cur1_amount_req].cumsum()

        orders_tmp[cur2_amount_req] = orders_tmp[cur1_amount_req] * orders_tmp['price']
        orders_tmp[cur2_amount_req_cum] = orders_tmp[cur2_amount_req].cumsum()
        
        need_cur2_amount = orders_tmp[cur2_amount_req].sum()
        #print("price (avg): {price_avg}".format(price_avg = need_cur2_amount/requested_cur1_amount))
        
        orders_tmp.to_csv(os.path.join(self.args.basepath, "data_out_markets/{fullmarketname}_request_{dir}.csv".format(fullmarketname=self.fullmarketname, dir=direction)))
        
        return(need_cur2_amount) # currency_amount (currency=EUR, USD, ...)

