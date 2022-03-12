from email_notifier import Email_Notifier
from pushover_notifier import Pushover_Notifier
import matplotlib as mpl
mpl.use('Agg') # uncomment if no X server
import matplotlib.pylab as plt
import os
import numpy as np


def send_email_arbitrage(arb_obj):
  #print("Sending email...")
  str = arbitrage_message_email(arb_obj)
  Nopp = len(arb_obj.df_arbitrage_opportunities)
  
  body = """Hello,

I'm w4arbitrage bot. I'm working for you!
{Nopp} {symbol} arbitrage opportunities have been found by requesting several exchangers API to get market data.
We are only looking for arbitrage opportunities better than {arbitrage_rel_min}%.
Use this at your own risk !


========

{str}
""".format(Nopp=Nopp, symbol=arb_obj.symbol, str=str, arbitrage_rel_min=arb_obj.arbitrage_rel_min)

  title = "{Nopp} {symbol} arbitrage opportunities found".format(Nopp=Nopp, symbol=arb_obj.symbol)

  arb_obj.email_notifier.sendEmail(title, body) # ToFix: sending monospace HTML email


"""
def send_email_arbitrage(arb_obj):
  email_notifier = Email_Notifier(arb_obj.args)
  #print("Sending email...")
  str = arbitrage_email_message(arb_obj)
  email_notifier.sendEmail("{symbol} arbitrage opportunities found".format(symbol=arb_obj.symbol), str)
"""

def plot_arbitrage(arb_obj):
  print("Plot arbitrage opportunities")
  
  Nopp = len(arb_obj.df_arbitrage_opportunities)

  cur1=arb_obj.cur1
  cur2=arb_obj.cur2
  cur1_amount = "{cur1}_amount".format(cur1=arb_obj.cur1.lower())
  cur2_amount = "{cur2}_amount".format(cur2=arb_obj.cur2.lower())
  cur1_amount_cum = "{cur1_amount}_cum".format(cur1_amount=cur1_amount)
  cur2_amount_cum = "{cur2_amount}_cum".format(cur2_amount=cur2_amount)


  #arb = arb_obj.lst_arbitrage_opportunities[0] # best arbitrage opportunity

  for i in range(Nopp):
    market_buy = arb_obj.df_arbitrage_opportunities.index[i][0]
    market_sell = arb_obj.df_arbitrage_opportunities.index[i][1]
  
    ob_buy = arb_obj.ob_dict[market_buy].orders['asks']
    ob_sell = arb_obj.ob_dict[market_sell].orders['bids']
  
    cur1_amount_max_from_ob = min(ob_buy[cur1_amount_cum].max(), ob_sell[cur1_amount_cum].max())
    cur1_amount_max_from_cur1 = 10 * float(arb_obj.args.currency1)
    cur1_amount_max = min(cur1_amount_max_from_ob, cur1_amount_max_from_cur1)
  
    #print(cur1_amount_max)
  
    ob_sell = ob_sell[(ob_sell[cur1_amount_cum]<cur1_amount_max)] #.shift(1).fillna(True)
    ob_buy = ob_buy[(ob_buy[cur1_amount_cum]<cur1_amount_max)] #.shift(1).fillna(True)


    #cur2_amount_max = 2000
    #ob_sell = ob_sell[ob_sell[cur2_amount_cum]<cur2_amount_max]
    #ob_buy = ob_buy[ob_buy[cur2_amount_cum]<cur2_amount_max]  
    
    x_buy = ob_buy[cur1_amount_cum]
    x_sell = ob_sell[cur1_amount_cum]
    x = np.union1d(x_buy, x_sell)
    y_buy = ob_buy[cur2_amount_cum]
    y_sell = ob_sell[cur2_amount_cum]

    y_buy_i = np.interp(x, x_buy, y_buy)
    y_sell_i = np.interp(x, x_sell, y_sell)
	
    y_diff = y_sell_i - y_buy_i
    y_diff_max = y_diff.max()
    x_diff_max = x[np.argmax(y_diff)]
    #x_diff_max = y_diff.idxmax()
    #x_diff_max = 0
    print("Diff max buy@{market_buy} sell@{market_sell} = {diff_max}{cur2} for {x_diff_max}{cur1}".format(
      diff_max=y_diff_max, x_diff_max=x_diff_max, cur1=arb_obj.cur1, cur2=arb_obj.cur2,
      market_sell=market_sell, market_buy=market_buy,
    ))
    
    fig = plt.figure()

    ax = fig.add_subplot(221)
    # ToDo
    plt.title("{y} = f({x})".format(x='price', y=cur1_amount_cum))
    
    #pc=0.05
    #plt.xlim(ob_buy['price'].min()*(1-pc),ob_sell['price'].max()*pc)
    
    
    pc = 5.0
    p_min = ob_buy['price'].min()
    p_max = ob_sell['price'].max()
    
    #ob_buy['price']<
    
    plt.xlim(p_min-(p_max-p_min)*pc/100.0,p_max+(p_max-p_min)*pc/100.0)
    #plt.ylim(0,max(ob_buy[cur1_amount_cum].max(),ob_sell[cur1_amount_cum].max()))
    plt.ylim(0, float(arb_obj.args.currency1))    
    
    pBids, = plt.plot(ob_sell['price'], ob_sell[cur1_amount_cum], color='b')
    pAsks, = plt.plot(ob_buy['price'], ob_buy[cur1_amount_cum], color='r')
    
    plt.legend([pAsks, pBids], ["Asks", "Bids"]) 



    ax = fig.add_subplot(223)
    #plt.title("{y} = f({x})".format(x=cur1_amount_cum,y=cur2_amount_cum))
    plt.title("{y} = f({x})".format(x=cur1,y=cur2))
    pSell, = ax.plot(ob_sell[cur1_amount_cum], ob_sell[cur2_amount_cum], color='b', marker='*') # , linestyle='None'
    pBuy, = ax.plot(ob_buy[cur1_amount_cum], ob_buy[cur2_amount_cum], color='r', marker='*') #, linestyle='None'
    #lgd = ax.legend(loc=9, bbox_to_anchor=(0.5,0))
    #ax.legend(bbox_to_anchor=(1.1, 1.05))
    # move legend
    
    #plt.legend([pBuy, pSell], ["Buy {market_buy} @ ask".format(market_buy=market_buy), "Sell {market_sell} @ bid".format(market_sell=market_sell)]) 
    plt.legend([pBuy, pSell], ["Buy {market_buy}".format(market_buy=market_buy), "Sell {market_sell}".format(market_sell=market_sell)]) 

    # arbitrage opp when blue above red
    

    ax = fig.add_subplot(222)
    plt.title("sell-buy ({cur2}) = f({cur1})".format(cur1=cur1,cur2=cur2))
    pDiff, = ax.plot(x, y_diff, color='k', marker='.') # y_diff_max
    #plt.legend([pDiff], ["bid_{market_sell} - ask_{market_buy}".format(market_buy=market_buy, market_sell=market_sell)]) 
    plt.legend([pDiff], ["diff"]) 
    plt.ylim(0.0,y_diff_max*1.1)
    #plt.ylim(-y_diff_max,y_diff_max)

    ax = fig.add_subplot(224)
    plt.ylim(0.0,20.0)
    pDiffPercent, = ax.plot(x, y_diff/y_buy_i*100.0, color='k', marker='.') # y_diff_max
    plt.title("% = f({x})".format(x=cur1))
    plt.legend([pDiff], ["diff (%)"]) 
    
    plt.savefig(os.path.join(arb_obj.args.basepath, "data_out_arbitrage/arbitrage_{i:02d}_{market_buy}_{market_sell}.png".format(
      i=i, market_sell=market_sell.replace('|', '').replace('/', ''), market_buy=market_buy.replace('|', '').replace('/', ''))))
    plt.show()


def arbitrage_message(arb_obj):
  str = ''
  for i in range(len(arb_obj.df_arbitrage_opportunities)):
    market_buy = arb_obj.df_arbitrage_opportunities.index[i][0]
    market_sell = arb_obj.df_arbitrage_opportunities.index[i][1]
    ask = arb_obj.df_ask[market_sell][market_buy]
    bid = arb_obj.df_bid[market_sell][market_buy]
    market_sell_price = arb_obj.size*ask
    market_buy_price = arb_obj.size*bid
    arbitrage_rel = arb_obj.df_arbitrage_rel[market_sell][market_buy]
    arbitrage_abs = arb_obj.df_arbitrage_abs[market_sell][market_buy]
    str = str + "opportunity - buy {size}{cur1} at {ask:.5f}{cur2} (for {market_buy_price:.2f}{cur2} at {market_buy}) - sell at {bid:.5f}{cur2} (for {market_sell_price:.2f}{cur2} at {market_sell}) - {arbitrage_rel:.2f}% - {arbitrage_abs:.2f}{cur2}\n".format(
      size=arb_obj.size,
      cur1=arb_obj.cur1, cur2=arb_obj.cur2,
      market_buy_price=market_buy_price, market_sell_price=market_sell_price,
      market_buy=market_buy, market_sell=market_sell,
	  ask=ask, bid=bid,
  	  arbitrage_rel=arbitrage_rel,
	  arbitrage_abs=arbitrage_abs)
  return(str)


def arbitrage_message_email(arb_obj):
  str = ''
  Nopp = len(arb_obj.df_arbitrage_opportunities)
  for i in range(Nopp):
    market_buy = arb_obj.df_arbitrage_opportunities.index[i][0]
    market_sell = arb_obj.df_arbitrage_opportunities.index[i][1]
    ask = arb_obj.df_ask[market_sell][market_buy]
    bid = arb_obj.df_bid[market_sell][market_buy]
    market_sell_price = arb_obj.size*ask
    market_buy_price = arb_obj.size*bid
    arbitrage_rel = arb_obj.df_arbitrage_rel[market_sell][market_buy]
    arbitrage_abs = arb_obj.df_arbitrage_abs[market_sell][market_buy]
    str = str + "opportunity - buy {size}{cur1} at {ask:.5f}{cur2} (for {market_buy_price:.2f}{cur2} at {market_buy}) - sell at {bid:.5f}{cur2} (for {market_sell_price:.2f}{cur2} at {market_sell}) - {arbitrage_rel:.2f}% - {arbitrage_abs:.2f}{cur2}\n".format(
      size=arb_obj.size,
      cur1=arb_obj.cur1, cur2=arb_obj.cur2,
      market_buy_price=market_buy_price, market_sell_price=market_sell_price,
      market_buy=market_buy, market_sell=market_sell,
	  ask=ask, bid=bid,
  	  arbitrage_rel=arbitrage_rel,
	  arbitrage_abs=arbitrage_abs)
    str = str + " BUY  @ " + "http://bitcoincharts.com/markets/{fullmarketname}_depth.html".format(fullmarketname=arb_obj.ob_dict[market_buy].fullmarketname) + "\n"
    str = str + " SELL @ " + "http://bitcoincharts.com/markets/{fullmarketname}_depth.html".format(fullmarketname=arb_obj.ob_dict[market_sell].fullmarketname) + "\n"
    str = str + '\n'

  str = str + "\n"
  str = str + "="*50 + "\n"
  str = str + "\n"

  for i in range(Nopp):
    market_buy = arb_obj.df_arbitrage_opportunities.index[i][0]
    market_sell = arb_obj.df_arbitrage_opportunities.index[i][1]
    ask = arb_obj.df_ask[market_sell][market_buy]
    bid = arb_obj.df_bid[market_sell][market_buy]
    market_sell_price = arb_obj.size*ask
    market_buy_price = arb_obj.size*bid
    arbitrage_rel = arb_obj.df_arbitrage_rel[market_sell][market_buy]
    arbitrage_abs = arb_obj.df_arbitrage_abs[market_sell][market_buy]
    str = str + "opportunity - buy {size}{cur1} at {ask:.5f}{cur2} (for {market_buy_price:.2f}{cur2} at {market_buy}) - sell at {bid:.5f}{cur2} (for {market_sell_price:.2f}{cur2} at {market_sell}) - {arbitrage_rel:.2f}% - {arbitrage_abs:.2f}{cur2}\n".format(
      size=arb_obj.size,
      cur1=arb_obj.cur1, cur2=arb_obj.cur2,
      market_buy_price=market_buy_price, market_sell_price=market_sell_price,
      market_buy=market_buy, market_sell=market_sell,
	  ask=ask, bid=bid,
  	  arbitrage_rel=arbitrage_rel,
	  arbitrage_abs=arbitrage_abs)
    str = str + "="*30 + "\n"
    str = str + arb_obj.df.ix[market_buy].to_string() + "\n"
    str = str + "="*40 + "\n"
    str = str + arb_obj.df.ix[market_sell].to_string() + "\n"
    str = str + "="*100 + "\n"

  str = str + "Markets" + "\n"
  str = str + "="*20 + "\n"
  str = str + arb_obj.df.to_string() + "\n"
  str = str + "="*100 + "\n"

  str = str + "Arbitrage matrix absolute ({cur2})".format(cur2=arb_obj.cur2) + "\n"
  str = str + "="*20 + "\n"
  str = str + arb_obj.df_arbitrage_abs.to_string() + "\n"
  str = str + "="*100 + "\n"

  str = str + "Arbitrage matrix relative (%)" + "\n"
  str = str + "="*20 + "\n"
  str = str + arb_obj.df_arbitrage_rel.to_string() + "\n"
  str = str + "="*100 + "\n"

  str = str + "Arbitrage list" + "\n"
  str = str + "="*20 + "\n"
  #str = str + arb_obj.df_arbitrage_opportunities.sort('rel diff', ascending=True).to_string() + "\n"
  str = str + arb_obj.df_arbitrage_opportunities_all.sort('rel diff', ascending=True).to_string() + "\n"
  #str = str + "="*100 + "\n"


  return(str)


def print_arbitrage(arb_obj):
  #print(arb_obj.df_arbitrage_opportunities)
  str = arbitrage_message(arb_obj)
  print(str)  


def arbitrage_callback(func, arb_obj):
  func(arb_obj)

def send_push_arbitrage(arb_obj):
  Nopp = len(arb_obj.df_arbitrage_opportunities)
  title = "[w4arbitrage] {Nopp} {symbol} >= {arbitrage_rel_min}%".format(
    Nopp=Nopp, symbol=arb_obj.symbol, arbitrage_rel_min=arb_obj.arbitrage_rel_min)
  str = ''
  Nopp = len(arb_obj.df_arbitrage_opportunities)
  for i in range(Nopp):
    market_buy = arb_obj.df_arbitrage_opportunities.index[i][0]
    market_sell = arb_obj.df_arbitrage_opportunities.index[i][1]
    ask = arb_obj.df_ask[market_sell][market_buy]
    bid = arb_obj.df_bid[market_sell][market_buy]
    market_sell_price = arb_obj.size*ask
    market_buy_price = arb_obj.size*bid
    arbitrage_rel = arb_obj.df_arbitrage_rel[market_sell][market_buy]
    arbitrage_abs = arb_obj.df_arbitrage_abs[market_sell][market_buy]	

    if i!=0:
      str = str + "="*10 + '\n'

    str = str + "{id:02d}/{Nopp:02d} - BUY {size}{cur1} at {ask:.5f}{cur2} (for {market_buy_price:.2f}{cur2} at {market_buy})".format(
      Nopp=Nopp, id=i+1, size=arb_obj.size, 
      cur1=arb_obj.cur1, cur2=arb_obj.cur2, 
      market_buy=market_buy,
      market_buy_price=market_buy_price,
      ask=ask
    )
    str = str + '\n' + "SELL at {bid:.5f}{cur2} (for {market_sell_price:.2f}{cur2} at {market_sell})".format(
      cur1=arb_obj.cur1, cur2=arb_obj.cur2,
      market_sell=market_sell, 
      market_sell_price=market_sell_price,
	  bid=bid
	)
    str = str + '\n' + "{arbitrage_rel:.2f}% - {arbitrage_abs:.2f}{cur2}\n".format(
      cur2=arb_obj.cur2,
  	  arbitrage_rel=arbitrage_rel,
	  arbitrage_abs=arbitrage_abs	
	)
	  
  str = str + "="*20 + '\n'
  for i in range(Nopp):
    market_buy = arb_obj.df_arbitrage_opportunities.index[i][0]
    market_sell = arb_obj.df_arbitrage_opportunities.index[i][1]

    str = str + "{id:02d}/{Nopp:02d} BUY @ http://bitcoincharts.com/markets/{fullmarketname}_depth.html".format(fullmarketname=arb_obj.ob_dict[market_buy].fullmarketname, Nopp=Nopp, id=i+1) + "\n"
    str = str + "SELL @ http://bitcoincharts.com/markets/{fullmarketname}_depth.html".format(fullmarketname=arb_obj.ob_dict[market_sell].fullmarketname) + "\n"
    str = str + '\n'
  
  arb_obj.push_notifier.sendNotification(str, title)