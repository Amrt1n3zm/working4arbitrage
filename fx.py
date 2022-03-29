#!/usr/bin/env python

"""
python fx.py --send EUR --req USD --send_amount 10

http://currency-api.appspot.com/api/EUR/USD.json?key=c76e9cefb2d4958b8b826806f80e8c9a4667509e&amount=1000
"""

import os
import argparse
from src.fx_currency_api import ForeignExchancheCurrencyApi

class ForeignExchancheCommandLineInterface:
  def __init__(self, args):
    self.args = args
    
    fx_api = ForeignExchancheCurrencyApi()
    fx_api.cur1 = args.send.upper()
    fx_api.cur2 = args.requ.upper()
    fx_api.data_path = os.path.dirname(__file__) # args.basepath

    if args.send_amount==None:
      fx_api.send_amount = 1.0
    else:
      fx_api.send_amount = float(args.send_amount)
    
    if not args.nodownload:
      fx_api.download()
      fx_api.write_json()
    else:
      fx_api.read_json()
    
    if args.printjson:
      fx_api.pretty_print_json()
      
    requ_amount = fx_api.requ_amount()
    print("You will get {requ_amount}{cur2} for {send_amount}{cur1} - {cur1}{cur2}@{rate}".format(
      requ_amount=requ_amount, send_amount=fx_api.send_amount,
      cur1=fx_api.cur1, cur2=fx_api.cur2, rate=fx_api.rate())) #requ_amount/fx_api.send_amount


if __name__ == "__main__":
  #locale.setlocale(locale.LC_ALL, 'en_US') # to print number with commas as thousands separators
  #locale.setlocale(locale.LC_ALL, 'fr_FR') # to print number with commas as thousands separators

  parser = argparse.ArgumentParser(description='Use the following parameters')
  parser.add_argument('--nodownload', action="store_true", help="use this flag to avoid downloading data (will use a previously downloaded file)")
  parser.add_argument('--send', action="store", help="use this flag to set what currency was sent")
  parser.add_argument('--requ', action="store", help="use this flag to set what currency is requested")
  parser.add_argument('--send_amount', action="store", help="use this flag to set how much currency is send")

  parser.add_argument('--printjson', action="store_true", help="use this flag to pretty print JSON")
  parser.add_argument('--nocalculate', action="store_true", help="use this flag to disable calculus with DataFrame")
  
  args = parser.parse_args()
  
  #args.basepath = os.path.dirname(__file__)
 
  fxcli = ForeignExchancheCommandLineInterface(args)
