import os
import json
import datetime

import urllib
import urllib2
import urlparse

#import pandas as pd

"""
https://openexchangerates.org/quick-start
http://openexchangerates.org/api/latest.json?app_id=d9f19436487f4b73abed6fb0079f97d0

{
    "disclaimer": "Exchange rates are provided for informational purposes only, and do not constitute financial advice of any kind. Although every attempt is made to ensure quality, NO guarantees are given whatsoever of accuracy, validity, availability, or fitness for any purpose - please use at your own risk. All usage is subject to your acceptance of the Terms and Conditions of Service, available at: http://openexchangerates.org/terms/",
    "license": "Data sourced from various providers with public-facing APIs; copyright may apply; resale is prohibited; no warranties given of any kind. All usage is subject to your acceptance of the License Agreement available at: http://openexchangerates.org/license/",
    "timestamp": 1363449609,
    "base": "USD",
    "rates": {
        "AED": 3.67312,
        ...
        "EUR": 0.765017,
        "GBP": 0.662014,
        ...
        "ZWL": 322.387247
    }
}

"""

class ForeignExchancheOpenExchangeRatesAPI:
  def __init__(self):
    self.api_key = 'GetYourOwn'
    self.url_api = 'http://openexchangerates.org/api/'

    self.data_path = ''
    
    self.cur1 = ''
    
  def update(self):
    self.cur1 = self.data['base']
    self.last_update = datetime.datetime.fromtimestamp(int(self.data['timestamp']))
    self.data['rates'][self.cur1] = 1

    #self.convert_to_DataFrame()
    
  def download(self):
    url = urlparse.urljoin(self.url_api, "latest.json?app_id={key}".format(key=self.api_key))
    print("Downloading FX data from {url}".format(url=url))
    response = urllib2.urlopen(url)
    self.json_data = response.read()
    self.data = json.loads(self.json_data)
    
  def write_json(self):
    filename = os.path.join(self.data_path, "data_in/FX_oer.json")
    print(" Writing FX market data to file \"{filename}\"".format(filename=filename))
    myFile = open(filename, 'w')
    myFile.write(self.json_data)
    myFile.close()

  def read_json(self):
    filename = os.path.join(self.data_path, "data_in/FX_oer.json")
    print("Reading FX market data from file \"{filename}\"".format(filename=filename))
    myFile = open(filename, 'r')
    self.json_data = myFile.read()
    self.data = json.loads(self.json_data)
    myFile.close()

  def pretty_print_json(self):
    #print(self.data)
    print(json.dumps(self.data, sort_keys=True, indent=2))

  def convert(self, send, requ, send_amount=None, requ_amount=None):
    if send_amount==None and requ_amount==None:
      raise(Exception("send_amount and requ_amount can't be simultaneously equal to None"))

    if send_amount!=None:
      return(self.data['rates'][requ]/self.data['rates'][send]*float(send_amount))

    if requ_amount!=None:
      return(self.data['rates'][send]/self.data['rates'][requ]*float(requ_amount))

"""
  # with Pandas DataFrame to output a conversion "matrix"

  def convert_to_DataFrame(self):
    d = self.data['rates']
    currencies = list(d.viewkeys())
    currencies.sort()
    #self.df = pd.DataFrame(d, index=['USD'])
    #self.df.index = self.df.columns
    self.df = pd.DataFrame(index=currencies, columns=currencies)
    #self.df[self.cur1] = d
    filename = os.path.join(self.data_path, "data_out_markets/_FX_oer.csv")
    
    for key, value in d.items():
      self.df[key][self.cur1] = value
      self.df[self.cur1][key] = value
      self.df[key][key] = 1
    
    for key, value in d.items():
      self.df[key] = self.df[self.cur1]/self.df[self.cur1][key]
      self.df.ix[key] = 1/(self.df[self.cur1]/self.df[self.cur1][key])
    
    self.df.to_csv(filename)

  def convert(self, send, requ, send_amount=None, requ_amount=None):
    if send_amount==None and requ_amount==None:
      raise(Exception("send_amount and requ_amount can't be simultaneously equal to None"))

    if send_amount!=None:
      return(self.df[send][requ]*float(send_amount))

    if requ_amount!=None:
      return(self.df[requ][send]*float(requ_amount))
"""