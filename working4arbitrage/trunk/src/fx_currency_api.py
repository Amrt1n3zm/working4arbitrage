import os
import json

import urllib
import urllib2
import urlparse

class ForeignExchancheCurrencyApi:
  def __init__(self):
    self.api_key = 'GetYourOwn'
    self.url_api = 'http://currency-api.appspot.com/api/'

    self.cur1 = 'EUR'
    self.cur2 = 'USD'
    self.send_amount = 1
    
    self.data_path = ''
    
  def pair(self):
    return("{cur1}{cur2}".format(cur1=self.cur1, cur2=self.cur2))
        
  def requ_amount(self):
    if self.data['success']==True:
      return(self.send_amount*float(self.data['rate']))
    else:
      raise(Exception(self.data))
  
  def rate(self):
    return(self.requ_amount()/self.send_amount)
      
  def download(self):
    url = urlparse.urljoin(self.url_api, "{cur1}/{cur2}.json?key={key}".format(cur1=self.cur1, cur2=self.cur2, key=self.api_key))
    print("Downloading FX data from {url}".format(url=url))
    response = urllib2.urlopen(url)
    self.json_data = response.read()
    self.data = json.loads(self.json_data)
    
  def write_json(self):
    filename = os.path.join(self.data_path, "data_in/FX_{pair}.json".format(pair=self.pair()))
    print(" Writing FX market data for {pair} to file \"{filename}\"".format(pair=self.pair(), filename=filename))
    myFile = open(filename, 'w')
    myFile.write(self.json_data)
    myFile.close()

  def read_json(self):
    filename = os.path.join(self.data_path, "data_in/FX_{pair}.json".format(pair=self.pair()))
    print("Reading FX market data for {pair} at \"{filename}\"".format(pair=self.pair(), filename=filename))
    myFile = open(filename, 'r')
    self.json_data = myFile.read()
    self.data = json.loads(self.json_data)
    myFile.close()

  def pretty_print_json(self):
    #print(self.data)
    print(json.dumps(self.data, sort_keys=True, indent=2))
