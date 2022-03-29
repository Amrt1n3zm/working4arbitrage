#!/usr/bin/env python

"""
A little script to see how profitable it can be to use BTC to exchange currencies

python currency_exchange_via_btc.py --cur1 EUR --cur2 USD --size 100 --nodownload 
"""

import os
import argparse
import pandas as pd
import numpy as np
from src.markets import *
from src.fx_currency_api import ForeignExchancheCurrencyApi
from time import sleep
from datetime import datetime, timedelta

class ConvertCurrenciesViaBTC:
  def __init__(self, args):
    self.args = args
    
    self.cur1 = args.cur1.upper() #'EUR' # sent cur
    self.cur2 = args.cur2.upper() #'USD' # requ cur

  def update(self):
    if args.size==None:
      self.size = 1
    else:
      self.size = float(args.size)

    self.load_fx_market()
    self.load_btc_market()

  def load_fx_market(self):
    print("Loading FX market")
    self.fx_api = ForeignExchancheCurrencyApi()
    self.fx_api.cur1 = self.cur1
    self.fx_api.cur2 = self.cur2
    self.fx_api.send_amount = self.size
    self.fx_api.data_path = os.path.dirname(__file__) # args.basepath

    if not (args.nodownload or args.nodownloadFX):
      self.fx_api.download()
      self.fx_api.write_json()
    else:
      self.fx_api.read_json()
    
    if args.printjson:
      self.fx_api.pretty_print_json()
      
    #requ_amount = self.fx_api.requ_amount()
    #print("You will get {requ_amount}{cur2} for {send_amount}{cur1} - {cur1}{cur2}@{rate}".format(
    #  requ_amount=requ_amount, send_amount=self.fx_api.send_amount,
    #  cur1=self.fx_api.cur1, cur2=self.fx_api.cur2, rate=requ_amount/self.fx_api.send_amount))
    
    self.fx_rate = self.fx_api.rate()
    
    #print(self.fx_rate)


    
  def load_btc_market(self):
    print("Loading BTC market")
    self.df_markets_btc = pd.read_csv(os.path.join(self.args.basepath, 'markets_btc.csv'), sep=';')
    #self.df_markets_exchangers = pd.read_csv('markets_exchangers.csv', sep=';')
    #  raise TypeError('unhashable type')
    self.df_markets = self.df_markets_btc
    #self.df_markets = pd.concat([self.df_markets_btc, self.df_markets_exchangers])
    # see https://www.aurumxchange.com/data/rates.json
    
    #self.df_markets.index = range(len(self.df_markets))
    #self.df_markets.
    
    
    #print(self.df_markets)

    self.df_markets['active'] = self.df_markets['active'].map(bool)
    self.df_markets['symbol'] = self.df_markets['cur1'] + '/' + self.df_markets['cur2']
    self.df_markets['fullmarketname'] = self.df_markets['market'] + '|' + self.df_markets['symbol']
    
    self.df_markets = self.df_markets[self.df_markets['active']==True] # select only active market

    
    self.df_markets['bid'] = None # NaN
    self.df_markets['ask'] = None

    #self.ob_dict = dict() # dictionary of order books
    for i in self.df_markets.index:
      market = self.df_markets['market'][i]
      fullmarketname = self.df_markets['fullmarketname'][i]
      #print(market)
      symbol = self.df_markets['symbol'][i]

      market_class = "OrderBook_{market}".format(market=market)
      ob = eval(market_class)(self.args, symbol)
      

      try:
        self.df_markets['bid'][i] = ob.bid(self.size)
      except:
        print("  Can't get bid price for {symbol} (market is probably not big enough)".format(symbol=symbol)) # NaN instead of bid/ask
        self.df_markets['bid'][i] = np.nan

      try:
        self.df_markets['ask'][i] = ob.ask(self.size)
      except:
        print("  Can't get ask for price {symbol} (market is probably not big enough)".format(symbol=symbol)) # NaN instead of bid/ask
        self.df_markets['ask'][i] = np.nan
        
      """
      stats = ob.get_stats()
      for key, value in stats.items():
        if i==0:
          self.df_markets[key] = None
        self.df_markets[key][i] = value
      """

    self.df_markets['spread'] = self.df_markets['ask'] - self.df_markets['bid']

    #self.df_markets = self.df_markets.reindex(self.df_markets['fullmarketname'])
    self.df_markets.index = self.df_markets['fullmarketname']

    print(self.df_markets)
    
    filename = os.path.join(self.args.basepath, "data_out_markets/_markets.csv")
    self.df_markets.to_csv(filename)
    
    markets_buy = self.df_markets[self.df_markets['cur2']==self.cur1]
    markets_sell = self.df_markets[self.df_markets['cur2']==self.cur2]
        
    self.df_matrix = pd.DataFrame(index=markets_buy['fullmarketname'], columns=markets_sell['fullmarketname'])
    self.df_ask = self.df_matrix.copy() # pd.DataFrame(index=markets_buy['fullmarketname'], columns=markets_sell['fullmarketname']) #self.df_matrix
    self.df_bid = self.df_matrix.copy() # pd.DataFrame(index=markets_buy['fullmarketname'], columns=markets_sell['fullmarketname']) #self.df_matrix
    
    for mk_buy in markets_buy.index:
      self.df_ask.ix[mk_buy] = self.df_markets.ix[mk_buy]['ask']

    for mk_sell in markets_sell.index:
      self.df_bid[mk_sell] = self.df_markets.ix[mk_sell]['bid'] # ToImprove: this can probably be done outside this for loop

    filename = os.path.join(self.args.basepath, "data_out_markets/_markets_matrix_ask.csv")
    self.df_ask.to_csv(filename)

    filename = os.path.join(self.args.basepath, "data_out_markets/_markets_matrix_bid.csv")
    self.df_bid.to_csv(filename)
    
    self.df_matrix = self.df_bid/self.df_ask
    
    print(self.df_matrix)

    filename = os.path.join(self.args.basepath, "data_out_markets/_markets_matrix.csv")
    self.df_matrix.to_csv(filename)

    self.df_convert_opportunities_all = pd.DataFrame(self.df_matrix.unstack(), columns=['rate'])
    self.df_convert_opportunities_all = self.df_convert_opportunities_all[self.df_convert_opportunities_all['rate']>-100]
    self.df_convert_opportunities_all = self.df_convert_opportunities_all.sort('rate', ascending=False)
    self.df_convert_opportunities_all.index.names = ['market_sell', 'market_buy']
    self.df_convert_opportunities_all = self.df_convert_opportunities_all.swaplevel(0, 1, axis=0) # swap to have market_buy as first hierarchical index
    #print(self.df_convert_opportunities_all)    
    
    self.df_convert_opportunities_all['rateFX'] = self.fx_rate

    self.df_convert_opportunities_all['rel diff (fx-btc)'] = (self.df_convert_opportunities_all['rate'] - self.fx_rate) / self.fx_rate * 100.0

    #self.df_convert_opportunities_all[self.cur1] = 'ToDo'
    #self.df_convert_opportunities_all[self.cur2] = 'ToDo'



    #print("{cur1}/{cur2} = {fx_rate}".format(cur1=self.cur1, cur2=self.cur2, fx_rate=self.fx_rate))
    
    self.df_convert_opportunities_all = self.df_convert_opportunities_all.sort('rate', ascending=False)
    filename = os.path.join(self.args.basepath, "data_out_markets/_currency_exch_via_btc.csv")
    self.df_convert_opportunities_all.to_csv(filename)

    self.df_convert_opportunities_all = self.df_convert_opportunities_all.sort('rate', ascending=True)
    print(self.df_convert_opportunities_all)

    
    #print(market_buy)
    #print(market_sell)


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Use the following parameters')
  parser.add_argument('--send_amount', action="store", help="use this flag to set how much currency is send")
  parser.add_argument('--nodownload', action="store_true", help="use this flag to avoid downloading data (will use a previously downloaded file)")
  parser.add_argument('--nodownloadFX', action="store_true", help="use this flag to avoid downloading FX data (will use a previously downloaded file)")
#  parser.add_argument('--nodownloadBTC', action="store_true", help="use this flag to avoid downloading BTC orderbooks (will use a previously downloaded file)")
  parser.add_argument('--printjson', action="store_true", help="use this flag to pretty print JSON")
  parser.add_argument('--printmk', action="store_true", help="use this flag to print market")
  parser.add_argument('--nocalculate', action="store_true", help="use this flag to disable calculus with DataFrame")
  parser.add_argument('--showstats', action="store_true", help="use this flag to show market stats")
  parser.add_argument('--plot', action="store_true", help="use this flag to display order book depth graph")
  parser.add_argument('--size', action="store", help="use this flag to set arbitrage size (in BTC)")
  parser.add_argument('--cur1', action="store", help="use this flag to set currency code you send")
  parser.add_argument('--cur2', action="store", help="use this flag to set currency code you request")
  parser.add_argument('--loop', action="store", help="use this flag to run program in an infinite loop (LOOP parameters is pause in seconds)")

  args = parser.parse_args()

  args.basepath = os.path.dirname(__file__)

  conv = ConvertCurrenciesViaBTC(args)
  

  if args.loop==None:
    conv.update()
  else:
    delay_s = float(args.loop)
    while True:
      conv.update()
      dt_next = datetime.now() + timedelta(seconds=delay_s)
      print("="*10)
      print("Waiting... next update @ {dt_next}".format(dt_next=dt_next.strftime("%Y-%m-%d %H:%M")))
      sleep(delay_s)
