#!/usr/bin/env python

"""
python currency_exchange.py --send EUR --req USD --send_amount 100

see Yahoo Finance, Google, Xe.com 

"""

import os
#import locale
import argparse

import sets
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx


class CurrencyExchanche:
  def __init__(self, args):
    self.args = args

  def update(self):
    self.draw_digraph()
    
  def load_market(self):
    self.df_markets_btc = pd.read_csv(os.path.join(self.args.basepath, 'markets_btc.csv'), sep=';')
    #self.df_markets_exchangers = pd.read_csv('markets_exchangers.csv', sep=';')
    #  raise TypeError('unhashable type')
    self.df_markets = self.df_markets_btc
    #self.df_markets = pd.concat([self.df_markets_btc, self.df_markets_exchangers])
    # see https://www.aurumxchange.com/data/rates.json
    
    print(self.df_markets)

    self.df_markets['active'] = self.df_markets['active'].map(bool)
    self.df_markets['fullmarketname'] = self.df_markets['market']+'|'+self.df_markets['cur1']+'/'+self.df_markets['cur2']
    
    self.df_markets = self.df_markets[self.df_markets['active']==True] # only active market
    
    #print(self.df_markets)


  def draw_digraph(self):
    print("Draw DiGraph")
    
    self.load_market()
    
    self.df_markets['cur1_account'] = self.df_markets['market']+'_'+self.df_markets['cur1']
    self.df_markets['cur2_account'] = self.df_markets['market']+'_'+self.df_markets['cur2']
    
    print(self.df_markets)

    set_cur1 = sets.Set(self.df_markets['cur1'].unique())
    set_cur2 = sets.Set(self.df_markets['cur2'].unique())
    currencies = set_cur1.union(set_cur2)
    print(currencies)
    
    set_acc_cur1 = sets.Set(self.df_markets['cur1_account'].unique())
    set_acc_cur2 = sets.Set(self.df_markets['cur2_account'].unique())
    accounts = set_acc_cur1.union(set_acc_cur2)
    
    #print(accounts)
    
    G = nx.DiGraph()
    G.add_nodes_from(currencies)
    G.add_nodes_from(accounts)


    for i in self.df_markets.index:
      market = self.df_markets['market'][i]
      cur1 = self.df_markets['cur1'][i]
      cur2 = self.df_markets['cur2'][i]
      cur1_account = self.df_markets['cur1_account'][i]
      cur2_account = self.df_markets['cur2_account'][i]
      active = self.df_markets['active'][i]
      fullmarketname = self.df_markets['fullmarketname'][i]
      #print("{fullmarketname}".format(fullmarketname=fullmarketname))
      G.add_edge(cur1_account, cur2_account) # label=market #, label='0'
      G.add_edge(cur2_account, cur1_account)
      
      G.add_edge(cur1_account, cur1)
      G.add_edge(cur1, cur1_account)

      G.add_edge(cur2_account, cur2)
      G.add_edge(cur2, cur2_account)


    #nx.draw(G)
    #nx.draw_random(G)
    #nx.draw_circular(G)
    #nx.draw_spectral(G)
    #plt.savefig("path.png")    
    #plt.show()

    nx.draw_graphviz(G)
    nx.write_dot(G,'path.dot')

    
    
  def draw_multigraph(self):
    print("Draw MultiGraph")
    
    self.load_market()
    
    set_cur1 = sets.Set(self.df_markets['cur1'].unique())
    set_cur2 = sets.Set(self.df_markets['cur2'].unique())
    currencies = set_cur1.union(set_cur2)
    #print(currencies)
    
    G=nx.MultiGraph() # Graph (pas plusieurs aretes) MultiDiGraph (plusieurs aretes dirigees entre 2 noeuds)
    G.add_nodes_from(currencies)
        
    #
    
    #egde_labels = list()
    for i in self.df_markets.index:
      market = self.df_markets['market'][i]
      cur1 = self.df_markets['cur1'][i]
      cur2 = self.df_markets['cur2'][i]
      active = self.df_markets['active'][i]
      fullmarketname = self.df_markets['fullmarketname'][i]
      print("{fullmarketname}".format(fullmarketname=fullmarketname))
      G.add_edge(cur1, cur2, label=market)
      #egde_labels[(cur1, cur2)] = fullmarketname

    #nx.draw_networkx_labels(G,1,fontsize=2, labelloc='c')
    #nx.draw_networkx_edge_labels(G,1, egde_labels, label_pos=0.3, ax=None, rotate=False)

    print(G)
    
    #print(egde_labels)
    
    #nx.draw(G)
    #nx.draw_random(G)
    #nx.draw_circular(G)
    #nx.draw_spectral(G)
    
    nx.draw_graphviz(G)
    nx.write_dot(G, os.path.join(self.args.basepath, 'path.dot'))
    
    #try:
    #  p = nx.shortest_path(G, source=args.send, target=args.requ, weight=None)
    #  print("Shortest path is {path}".format(path=p))
    #except:
    #  raise(Exception("Can't find a path - valid nodes are {currencies}".format(currencies=currencies)))

    #paths = nx.all_shortest_paths(G, source=args.send, target=args.requ)
    #print(paths)

    
    #plt.savefig("path.png")
    
    #plt.show()
    
    


if __name__ == "__main__":
  #locale.setlocale(locale.LC_ALL, 'en_US') # to print number with commas as thousands separators
  #locale.setlocale(locale.LC_ALL, 'fr_FR') # to print number with commas as thousands separators

  parser = argparse.ArgumentParser(description='Use the following parameters')
  parser.add_argument('--nodownload', action="store_true", help="use this flag to avoid downloading orderbook (will use a previously downloaded file)")
  parser.add_argument('--send', action="store", help="use this flag to set what currency was sent")
  parser.add_argument('--requ', action="store", help="use this flag to set what currency is requested")
  parser.add_argument('--send_amount', action="store", help="use this flag to set how much currency is send")
  
  args = parser.parse_args()
  
  args.basepath = os.path.dirname(__file__)
 
  ce = CurrencyExchanche(args)
  ce.update()