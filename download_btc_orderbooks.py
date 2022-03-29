#!/usr/bin/env python

"""
Download BTC orderbooks
"""

import os
import argparse
from src.markets import *
from time import sleep
from datetime import datetime, timedelta
import pandas as pd

class DownloadBTCOrderbooks:
  def __init__(self, args):
    self.args = args

  def update(self):
    dt = datetime.now()
    print("="*5+" Loading BTC market @ {dt} ".format(dt=dt)+"="*5)
    filename_mk_btc = 'markets_btc.csv'
    self.df_markets = pd.read_csv(os.path.join(self.args.basepath, filename_mk_btc), sep=';')
    del self.df_markets['Unnamed: 0']
    
    self.df_markets['active'] = self.df_markets['active'].map(bool)
    self.df_markets['symbol'] = self.df_markets['cur1'] + '/' + self.df_markets['cur2']
    self.df_markets['fullmarketname'] = self.df_markets['market']+'|'+self.df_markets['cur1']+'/'+self.df_markets['cur2']
    
    self.df_markets = self.df_markets[self.df_markets['active']==True] # select only active market
    
    #print(self.df_markets)
    
    for i in self.df_markets.index:
      market = self.df_markets['market'][i]
      fullmarketname = self.df_markets['fullmarketname'][i]
      symbol = self.df_markets['symbol'][i]

      market_class = "OrderBook_{market}".format(market=market)

      try:
        dt = datetime.now()
        self.df_markets['last_update_try'][i] = dt
        ob = eval(market_class)(self.args, symbol)
        dt = datetime.now()
        self.df_markets['last_update_ok'][i] = dt
      except:
        print(" !!! Error with this market !!!")
    
    print("")
    
    self.df_markets.to_csv(os.path.join(self.args.basepath, filename_mk_btc), sep=';')


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Use the following parameters')
  parser.add_argument('--nodownload', action="store_true", help="use this flag to avoid downloading data (will use a previously downloaded file)")
  parser.add_argument('--printjson', action="store_true", help="use this flag to pretty print JSON")
  parser.add_argument('--printmk', action="store_true", help="use this flag to print market")
  parser.add_argument('--nocalculate', action="store_true", help="use this flag to disable calculus with DataFrame")
  parser.add_argument('--showstats', action="store_true", help="use this flag to show market stats")
  parser.add_argument('--plot', action="store_true", help="use this flag to display order book depth graph")
  args = parser.parse_args()

  args.basepath = os.path.dirname(__file__)

  dwl = DownloadBTCOrderbooks(args)

  dwl.update()
