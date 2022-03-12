#!/usr/bin/env python

"""
https://www.aurumxchange.com/data/rates.json
"""

import os
import argparse
#from src.exchanger_aurumxchange_api import ExchangerAurumXchangeAPI

#import os
import json
import datetime

import urllib
import urllib2
import urlparse

import pandas as pd


class ExchangerAurumXchangeAPI:
  def __init__(self):
    self.url_api = 'https://www.aurumxchange.com/data/'
    self.data_path = ''
        
  def update(self):
    #self.last_update = datetime.datetime.fromtimestamp(int(self.data['timestamp']))
    # 2013-03-16T21:44:05+00:00 # ToFix: parse -> datetime
    
    self.convert_to_DataFrame()
    
  def download(self):
    url = urlparse.urljoin(self.url_api, "rates.json")
    print("Downloading exchanger data from {url}".format(url=url))
    response = urllib2.urlopen(url)
    self.json_data = response.read()
    self.data = json.loads(self.json_data)
    
  def write_json(self):
    filename = os.path.join(self.data_path, "data_in/exchanger_aurumxchange.json")
    print(" Writing exchanger data to file \"{filename}\"".format(filename=filename))
    myFile = open(filename, 'w')
    myFile.write(self.json_data)
    myFile.close()

  def read_json(self):
    filename = os.path.join(self.data_path, "data_in/exchanger_aurumxchange.json")
    print("Reading exchanger data from file \"{filename}\"".format(filename=filename))
    myFile = open(filename, 'r')
    self.json_data = myFile.read()
    self.data = json.loads(self.json_data)
    myFile.close()

  def pretty_print_json(self):
    #print(self.data)
    print(json.dumps(self.data, sort_keys=True, indent=2))


  def convert_to_DataFrame(self):
    #print(self.data['rates'])

    #self.df = pd.DataFrame(index=currencies, columns=currencies)
    
    #self.df = pd.DataFrame(self.data['rates'])
    d = self.data['rates']
    #panel =  pd.Panel.from_dict(d)
    #print(panel)
    # swap major and minor axis
    #self.df = panel.to_frame()
    
    self.df = pd.concat(map(pd.DataFrame, d.itervalues()), keys=d.keys()).stack().unstack(0)
    self.df = self.df.T
    
    #print(self.df['rate']['BCBTC']['LRUSD'])
    
    filename = os.path.join(self.data_path, "data_out_markets/_exchanger_aurum.csv")
    self.df.to_csv(filename)
    
    self.df_rate = self.df['rate'].sort_index(0)
    self.df_available = self.df['available'].sort_index(0)
    
    filename = os.path.join(self.data_path, "data_out_markets/_exchanger_aurum_rate.csv")
    self.df_rate.to_csv(filename)

    filename = os.path.join(self.data_path, "data_out_markets/_exchanger_aurum_available.csv")
    self.df_available.to_csv(filename)


class ExchangerAurumXchangeCLI:
  def __init__(self, args):
    exchange = ExchangerAurumXchangeAPI()
    exchange.data_path = os.path.dirname(__file__) # args.path
    
    if not args.nodownload:
      exchange.download()
      exchange.write_json()
    else:
      exchange.read_json()
    
    if args.printjson:
      exchange.pretty_print_json()
      
    exchange.update()
    

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Use the following parameters')
  parser.add_argument('--nodownload', action="store_true", help="use this flag to avoid downloading data (will use a previously downloaded file)")  
  parser.add_argument('--printjson', action="store_true", help="use this flag to pretty print JSON")

  #parser.add_argument('--send', action="store", help="use this flag to set what currency was sent")
  #parser.add_argument('--requ', action="store", help="use this flag to set what currency is requested")
  
  #parser.add_argument('--send_amount', action="store", help="use this flag to set how much currency is send")
  #parser.add_argument('--requ_amount', action="store", help="use this flag to set how much currency is requested")

  args = parser.parse_args()

  exchange_cli = ExchangerAurumXchangeCLI(args)