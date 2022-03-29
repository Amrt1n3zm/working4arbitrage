#!/usr/bin/env python

import os
#import locale
import argparse
from time import sleep
from datetime import datetime, timedelta

from src.markets import *
from src.arbitrage import Arbitrage

def main(args):
  print("="*5+" Running {dt} ".format(dt=datetime.now().strftime("%Y-%m-%d %H:%M"))+"="*5)
  
  if args.action!=None:
    args.action = args.action.lower()

  if args.action=='arbitrage':
    if args.currency1==None:
      raise Exception("--action arbitrage --currency1 size")
    arb.arbitrage()
    
  elif args.action=='howmuch':
    arb.howmuch()

  elif args.action=='printmk':
    arb.printmk()
    
  else:
    raise Exception("--action arbitrage|howmuch|printmk")


if __name__ == "__main__":
  #locale.setlocale(locale.LC_ALL, 'en_US') # to print number with commas as thousands separators
  #locale.setlocale(locale.LC_ALL, 'fr_FR') # to print number with commas as thousands separators

  parser = argparse.ArgumentParser(description='Use the following parameters')
  parser.add_argument('--nodownload', action="store_true", help="use this flag to avoid downloading orderbook (will use a previously downloaded file)")
  parser.add_argument('--printjson', action="store_true", help="use this flag to pretty print JSON")
  parser.add_argument('--printmk', action="store_true", help="use this flag to print market")
  parser.add_argument('--nocalculate', action="store_true", help="use this flag to disable calculus with DataFrame")
  parser.add_argument('--plot', action="store_true", help="use this flag to display order book depth graph")
  parser.add_argument('--pmin', action="store", help="use this flag to define price min to plot")
  parser.add_argument('--pmax', action="store", help="use this flag to define price max to plot")
  parser.add_argument('--showstats', action="store_true", help="use this flag to show market stats")
  parser.add_argument('--markets', action="store", help="use this flag to define markets")
  parser.add_argument('--loop', action="store", help="use this flag to run program in an infinite loop (LOOP parameters is pause in seconds)")
  parser.add_argument('--action', action="store", help="use this flag to set 'arbitrage' mode or to reply to 'howmuch' question or just 'printmk' to print market order book")
  parser.add_argument('--reldiff', action='store', help='use this flag to show only arbitrage opportunities >= reldiff (%%)')
  parser.add_argument('--currency1', action="store", help="use this flag to set arbitrage size (in currency 1 = BTC)")
  parser.add_argument('--direction', action="store", help="use this flag to set how much direction")
  parser.add_argument('--requested_cur1_amount', action="store", help="use this flag to set how much cur1 is requested")
  parser.add_argument('--requested_cur2_amount', action="store", help="use this flag to set how much cur2 is requested")
  parser.add_argument('--sendemail', action="store_true", help="use this flag to send email when arbitrage opportunities are found")
  parser.add_argument('--sendpush', action="store_true", help="use this flag to send push notification")
  parser.add_argument('--debug', action="store_true", help="use this flag to switch to debug mode")
  parser.add_argument('--test', action="store_true", help="use this flag to test notifications (email, SMS, push)")
  
  args = parser.parse_args()
  
  args.basepath = os.path.dirname(__file__)
  
  #markets = args.markets
  #markets = ['bitcurexEUR', 'mtgoxEUR']

  #ob = OrderBook_bitcurexEUR(args)
  #ob = OrderBook_mtgoxEUR(args)

  arb = Arbitrage(args)

  if args.loop==None:
    main(args)
  else:
    delay_s = float(args.loop)
    while True:
      main(args)
      dt_next = datetime.now() + timedelta(seconds=delay_s)
      print("="*10)
      print("Waiting... next update @ {dt_next}".format(dt_next=dt_next.strftime("%Y-%m-%d %H:%M")))
      sleep(delay_s)
