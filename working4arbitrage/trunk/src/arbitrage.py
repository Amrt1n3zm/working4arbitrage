import os
import pandas as pd
import numpy as np
from datetime import datetime
from src.markets import *
from src.arbitrage_callback import *

class Arbitrage:
  def __init__(self, args):
    self.args = args
    self.markets = args.markets.split(' ')

    if self.args.sendemail:
      self.email_notifier = Email_Notifier(self.args)
    if self.args.sendpush:
      self.push_notifier = Pushover_Notifier(self.args)


  def howmuch(self):
    args = self.args
    print("Howmuch ?")
    for market_symbol in self.markets:
      market_symbol = market_symbol.split('|')
      market = market_symbol[0]
      symbol = market_symbol[1]
      market_class = "OrderBook_{market}".format(market=market)
      ob = eval(market_class)(args, symbol)

      try:
        val1 = float(args.requested_cur1_amount)
      except:
        val1 = None
      
      try:
        val2 = float(args.requested_cur2_amount)
      except:
        val2 = None

      dir = args.direction
      
      ret = ob.how_much(dir, val1, val2)
            
      print("{total_price} {cur2} @ {avg_price} {cur2} per {cur1} to {dir}".format(
        total_price=ret, avg_price=ret/val1, cur1=ob.cur1, cur2=ob.cur2,
        dir=args.direction
        )
      )
  
  def printmk(self):
    for market_symbol in self.markets:
      market_symbol = market_symbol.split('|')
      market = market_symbol[0]
      symbol = market_symbol[1]
      market_class = "OrderBook_{market}".format(market=market)
      ob = eval(market_class)(self.args, symbol)

  def arbitrage(self):
    self.df = pd.DataFrame(index=self.markets, columns=['bid', 'ask'])

    self.size = float(self.args.currency1)

    i = 0
    self.ob_dict = dict() # dictionary of order books
    for market_symbol in self.markets:
      try:
        lst_market_symbol = market_symbol.split('|')
        market = lst_market_symbol[0]
        symbol = lst_market_symbol[1]
        if i>0:
          if symbol!=symbol_prev:
            raise(Exception("Symbols must be similar {symbol}!={symbol_prev} (market symbols were {market1} {market2})".format(
              symbol=symbol, symbol_prev=symbol_prev,
              market1=market_symbol, market2=market_symbol_prev,
              ))
            )
        symbol_prev = symbol
        market_symbol_prev = market_symbol
        
        market_class = "OrderBook_{market}".format(market=market)
        ob = eval(market_class)(self.args, symbol)
        self.ob_dict[market_symbol] = ob
      
        try:
          self.df['bid'][market_symbol] = ob.bid(self.size)
        except:
          print("  Can't get bid price for {market_symbol} (market is probably not big enough)".format(market_symbol=market_symbol)) # NaN instead of bid/ask

        try:
          self.df['ask'][market_symbol] = ob.ask(self.size)
        except:
          print("  Can't get ask for price {market_symbol} (market is probably not big enough)".format(market_symbol=market_symbol)) # NaN instead of bid/ask
            
        stats = ob.get_stats()
      
        for key, value in stats.items():
          if i==0:
            self.df[key] = None
          self.df[key][market_symbol] = value

        i = i + 1
    
      except:
        print("Error with {market_symbol}".format(market_symbol=market_symbol))
        del self.markets[i]
    
    self.df['spread'] = self.df['ask'] - self.df['bid']
    self.symbol = symbol
    (self.cur1, self.cur2) = self.symbol.split('/')
    self.pair = "{cur1}{cur2}".format(cur1=self.cur1, cur2=self.cur2) # no /
    
    #self.cur1 = symbol[0:3] #"BTC"
    #self.cur2 = symbol[3:7] ##"USD"
    
    #mask = ~ ((self.df['bid'].apply(np.isnan)) & (self.df['ask'].apply(np.isnan)))
    #mask =  ~ (self.df['bid'].isnull() & self.df['ask'].isnull())
    #self.df['mask'] = mask

    print("="*10+" Tickers for {size:.8f}{cur1} ".format(size=self.size, cur1=self.cur1)+"="*10)
    dt_now = datetime.now()

    self.df = self.df.sort('bids_cur1_amount_cum_max', ascending=False)

    print(self.df)
    self.df.to_csv(os.path.join(self.args.basepath, "data_out_arbitrage/arbitrage_markets_{symbol}.csv".format(symbol=self.pair)))

    self.df.sort('ask', ascending=True).to_csv(os.path.join(self.args.basepath, "data_out_arbitrage/arbitrage_markets_{symbol}_asks_asc.csv".format(symbol=self.pair)))
    self.df.sort('bid', ascending=False).to_csv(os.path.join(self.args.basepath, "data_out_arbitrage/arbitrage_markets_{symbol}_bids_desc.csv".format(symbol=self.pair)))


    print("="*10+" Tickers stats "+"="*10)
    print("""Total asks: {asks_total}
Total bid: {bids_total}
""".format(
  asks_total=self.df['nb_asks'].sum(), bids_total=self.df['nb_bids'].sum()))


    # Remove lines bid/ask = NaN/NaN
    #mask = (self.df['bid'].apply(np.isfinite)) | (self.df['ask'].apply(np.isfinite))
    #mask = ~ ((self.df['bid'].apply(np.isnan)) & (self.df['ask'].apply(np.isnan)))
    mask =  ~ (self.df['bid'].isnull() & self.df['ask'].isnull())
    # see also np.isnan (with ~ for not)
    # see isnan http://docs.scipy.org/doc/numpy/reference/generated/numpy.isnan.html
    # see ~ http://docs.python.org/2/library/operator.html
    #print(mask)
    self.df = self.df[mask]    
    self.markets = self.df.index
    
    self.df_ask = pd.DataFrame(index=self.markets, columns=self.markets)
    self.df_bid = pd.DataFrame(index=self.markets, columns=self.markets)

    
    
    if self.args.reldiff==None:
      self.arbitrage_rel_min = 0.0 # filter (%)
    else:
      self.arbitrage_rel_min = float(self.args.reldiff)
    

    #print("="*10+" Ticker "+"="*10)
    #dt_now = datetime.now()
    #str = "Ticker bid/ask for {size:.8f} {cur2} @ {dt}".format(size=self.size, cur2=self.cur2, dt=dt_now.strftime("%Y-%m-%d %H:%M"))
    #print(str)
    
    for mk in self.markets:
      #str = str + " - {market}: {bid:.5f}/{ask:.5f}".format(market=mk, bid=self.df.ix[mk]['bid'], ask=self.df.ix[mk]['ask'])
      self.df_ask.ix[mk] = self.df.ix[mk]['ask'] # ToImprove: this can probably be done outside this for loop
      self.df_bid[mk] = self.df.ix[mk]['bid'] # ToImprove: this can probably be done outside this for loop
    #print(str)

    #print(self.df)
    #print(self.df_bid)
    #print(self.df_ask)

    self.df_arbitrage_abs = (self.df_bid - self.df_ask)*self.size
    self.df_arbitrage_rel = (self.df_bid - self.df_ask)/self.df_ask*100.0

    self.df_arbitrage_abs.to_csv(os.path.join(self.args.basepath, "data_out_arbitrage/arbitrage_abs_{symbol}.csv".format(symbol=self.pair)))
    self.df_arbitrage_rel.to_csv(os.path.join(self.args.basepath, "data_out_arbitrage/arbitrage_rel_{symbol}.csv".format(symbol=self.pair)))

    print("="*10+" Relative difference (%) "+"="*10)
    print(self.df_arbitrage_rel)

    print("="*40)
    #df_arbitrage_opportunities df_arbitrage_opportunities
    
    #self.df_arbitrage_opportunities_all = pd.DataFrame(self.df_arbitrage_rel.unstack(), columns=['rel diff'])
    self.df_arbitrage_opportunities_all = pd.DataFrame(self.df_ask.unstack(), columns=['ask'])
    #self.df_arbitrage_opportunities_all['ask'] = self.df_ask.unstack()
    self.df_arbitrage_opportunities_all['bid'] = self.df_bid.unstack()
    self.df_arbitrage_opportunities_all['abs diff'] = self.df_arbitrage_abs.unstack()
    self.df_arbitrage_opportunities_all['rel diff'] = self.df_arbitrage_rel.unstack()
    self.df_arbitrage_opportunities_all = self.df_arbitrage_opportunities_all[self.df_arbitrage_opportunities_all['rel diff']>-100]
    self.df_arbitrage_opportunities_all = self.df_arbitrage_opportunities_all.sort('rel diff', ascending=False)
    self.df_arbitrage_opportunities_all.index.names = ['market_sell', 'market_buy']
    self.df_arbitrage_opportunities_all = self.df_arbitrage_opportunities_all.swaplevel(0, 1, axis=0) # swap to have market_buy as first hierarchical index
    print(self.df_arbitrage_opportunities_all.sort('rel diff', ascending=True)[-50:])
    
    print("="*10+" Arbitrage opportunities (better than {arbitrage_rel_min}%)".format(arbitrage_rel_min=self.arbitrage_rel_min)+"="*10)
    self.df_arbitrage_opportunities = self.df_arbitrage_opportunities_all[self.df_arbitrage_opportunities_all['rel diff']>self.arbitrage_rel_min]
    
    if len(self.df_arbitrage_opportunities)>0:
      arbitrage_callback(print_arbitrage, self)
      arbitrage_callback(plot_arbitrage, self)
      if self.args.sendemail:
        arbitrage_callback(send_email_arbitrage, self)
      if self.args.sendpush:
        arbitrage_callback(send_push_arbitrage, self)
      
    else:
      print(";-( no arbitrage opportunities ;-(")
