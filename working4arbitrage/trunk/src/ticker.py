class Ticker:
  def __init__(self, ask=None, bid=None):
    self.ask = ask
    self.bid = bid

  def spread(self):
    return(self.ask-self.bid)

  def __repr__(self):
    str = """ask: {ask}
bid: {bid}""".format(ask=self.ask, bid=self.bid)

    if self.ask!=None and self.bid!=None:
      str = str + """
spread: {spread}""".format(spread=self.spread())
  
    return(str)
    
    # buy at ask price - sell at bid price
