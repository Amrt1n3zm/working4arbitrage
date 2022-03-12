import urllib
import urllib2
import urlparse
import json

from datetime import datetime, timedelta
#import time

"""
https://pushover.net/
https://api.pushover.net/1/messages.json

https://pushover.net/api
"""

class Pushover_Notifier:
  def __init__(self, args):
    self.args = args

    self.user_key = "GetYourOwn"
    self.api_token = "GetYourOwn"    
    self.url_api = "https://api.pushover.net/1/"
    self.title = 'pushover_cli'
    self.priority = -1

    self.notifier_delay = timedelta(minutes=30)
    self.dt_last_send = datetime.now() - self.notifier_delay
    
  def __sendNotification_release(self, message_text, title):
    if self.args.debug:
      print("="*10)
      print(message_text) # Show for test
      print("="*10)

    url = urlparse.urljoin(self.url_api, "messages.json")

    params = urllib.urlencode({
      'user' : self.user_key,
      'token' : self.api_token,
      'message' : message_text,
      'title': title,
      'priority': self.priority
    })
    
    req = urllib2.Request(url, params)
    response = urllib2.urlopen(req)
    output = response.read()
    data = json.loads(output)
    
    if self.args.debug:
      print(data)

    if data['status'] != 1:
        raise PushoverError(output)

    response.close()

  def __sendNotification_test(self, message_text, title):
    print("Sending notification to {user_key}".format(user_key=self.user_key))
    print("="*30)
    print(message_text)

  def __sendNotification(self, message_text, title):
    if self.args.test:
      self.__sendNotification_test(message_text, title)
    else:
      self.__sendNotification_release(message_text, title)

  def sendNotification(self, message_text=None, title=None):
    if message_text==None:
      raise(Exception("No notification send because no message was given"))
      #message_text = self.message_text

    if title == None:
      title = self.title

    #self.date = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    print("Sending notification...")

    self.dt_now = datetime.now()
    dt_next = self.dt_last_send + self.notifier_delay
    
    if self.dt_now >= dt_next:
      self.__sendNotification(message_text, title)
      self.dt_last_send = self.dt_now
    else:
      print("Too many notifications (next notification can be delivered after {dt}) !!!".format(dt=dt_next.strftime("%Y-%m-%d %H:%M")))
    
