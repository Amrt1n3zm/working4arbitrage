#!/usr/bin/env python

"""
http://openexchangerates.org/api/latest.json?app_id=d9f19436487f4b73abed6fb0079f97d0

python fx_openexchangerates.py --nodownload --send EUR --requ USD --send_amount 2000
"""

import os
import argparse
from src.fx_openexchangerates_api import ForeignExchancheOpenExchangeRatesAPI

class ForeignExchancheOpenExchangeRatesCLI:
  def __init__(self, args):
    fxoer = ForeignExchancheOpenExchangeRatesAPI()
    fxoer.data_path = os.path.dirname(__file__) # args.path
    
    if not args.nodownload:
      fxoer.download()
      fxoer.write_json()
    else:
      fxoer.read_json()
    
    if args.printjson:
      fxoer.pretty_print_json()
      
    fxoer.update()
    
    print("Last update: {dt}".format(dt=fxoer.last_update))

    if args.send_amount==None and args.requ_amount==None:
      args.send_amount = 1.0
    
    if args.send_amount!=None:
      amount = fxoer.convert(args.send, args.requ, args.send_amount, None)
      print("{amount} {cur1}".format(amount=amount, cur1=args.requ))

    if args.requ_amount!=None:
      amount = fxoer.convert(args.send, args.requ, None, args.requ_amount)
      print("{amount} {cur2}".format(amount=amount, cur2=args.send))

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Use the following parameters')
  parser.add_argument('--nodownload', action="store_true", help="use this flag to avoid downloading data (will use a previously downloaded file)")  
  parser.add_argument('--printjson', action="store_true", help="use this flag to pretty print JSON")

  parser.add_argument('--send', action="store", help="use this flag to set what currency was sent")
  parser.add_argument('--requ', action="store", help="use this flag to set what currency is requested")
  
  parser.add_argument('--send_amount', action="store", help="use this flag to set how much currency is send")
  parser.add_argument('--requ_amount', action="store", help="use this flag to set how much currency is requested")

  args = parser.parse_args()

  fxoer_cli = ForeignExchancheOpenExchangeRatesCLI(args)