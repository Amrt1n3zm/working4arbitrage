from smtplib import SMTP
from datetime import datetime, timedelta

class Email_Notifier:
  def __init__(self, args):    
    self.args = args

    self.smtp_server = 'smtp.domain.com'
    self.smtp_port = 25
    self.debuglevel = 0

    self.servername = 'Mining 1'
    self.from_addr = "me <me@domain.com>"
    self.to_addr = "me <me@domain.com>"

    self.subj = "Arbitrage opportunities found"

    self.message_text = """Hello,

This is a mail from your arbitrage server.

Bye
"""
    self.email_delay = timedelta(minutes=30)

    self.smtp = SMTP()
    self.smtp.set_debuglevel(self.debuglevel)

    self.dt_last_send = datetime.now() - self.email_delay
        

  def sendEmail(self, subj=None, message_text=None, to_addr=None):
    if subj==None:
      subj = self.subj
    
    if message_text==None:
      message_text = self.message_text

    if to_addr == None:
      to_addr = self.to_addr

    self.dt_now = datetime.now()

    msg = """From: {from_addr}
To: {to_addr}
Subject: [BTC arbitrage mail][w4arbitrage] - {servername} - {subj}
Date: {date}

{message_text}""".format(from_addr=self.from_addr, to_addr=self.to_addr,
        servername=self.servername, subj=subj, date=self.dt_now.strftime("%d/%m/%Y %H:%M"), message_text=message_text)
    
    if self.args.debug:
      print(msg) # Show for test

    print("Sending email...")
    
    dt_next = self.dt_last_send + self.email_delay
    
    if self.dt_now >= dt_next:
      self.smtp.connect(self.smtp_server, self.smtp_port)
      self.smtp.sendmail(self.from_addr, self.to_addr, msg)
      self.smtp.quit()
      self.dt_last_send = self.dt_now
    else:
      print("Too many emails (next mail can be delivered after {dt}) !!!".format(dt=dt_next.strftime("%Y-%m-%d %H:%M")))


"""

import subprocess
def send_email(title, msg, raw_data):
    if send_email.old_raw_data == raw_data:
        print "already sent"
        return
    send_email.old_raw_data = raw_data
    print "sending email"
    subprocess.call('echo "%s" | mutt -s "%s" "%s"' % (msg, title, email_address),
                    shell=True)

    subprocess.call("echo {msg} | mutt -s '{title}' '{to_addr}'".format(msg=msg, title=title, to_addr=to_addr), shell=True)
send_email.old_raw_data = ""

"""