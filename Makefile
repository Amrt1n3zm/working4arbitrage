all:
#	python w4arbitrage.py --markets "mtgox|BTCEUR bitcurex|BTCEUR bc|BTCEUR" --action arbitrage --currency1 100 --loop 900
#	python w4arbitrage.py --markets "mtgox|BTCEUR bitcurex|BTCEUR bc|BTCEUR" --action arbitrage --currency1 100
#	python w4arbitrage.py --markets "mtgox|BTCEUR bitcurex|BTCEUR bc|BTCEUR btce|BTCEUR" --action arbitrage --currency1 10
#	python w4arbitrage.py --markets "mtgox|BTCUSD bitstamp|BTCUSD bc|BTCUSD btce|BTCUSD bitme|BTCUSD" --action arbitrage --currency1 10
#	python w4arbitrage.py --nodownload --markets "bc|BTCEUR bitcurex|BTCEUR mtgox|BTCEUR" --action howmuch --currency1 BTC --direction buy --requested_cur1_amount 10
	$(MAKE) arbEUR

arbEUR:
	./run_arbitrage_BTCEUR.sh

arbUSD:
	./run_arbitrage_BTCUSD.sh

.PHONY: clean

clean:
	$(RM) data_in/*
	$(RM) data_out_markets/*
	$(RM) data_out_arbitrage/*

#temp:
	#python w4arbitrage.py
	#python w4arbitrage.py --nodownload
	#python w4arbitrage.py --nodownload --markets "bitcurexEUR mtgoxEUR"
	#python w4arbitrage.py --nodownload --markets "bitcurexEUR mtgoxEUR" --loop 10
	#python w4arbitrage.py --nodownload --markets "bitcurexEUR mtgoxEUR" --loop 60 --action arbitrage --size 10
	#python w4arbitrage.py --nodownload --markets "bitcurexEUR mtgoxEUR" --loop 10 --action howmuch --cur1 BTC --cur2 EUR --direction buy --requested_cur1_amount 10 --requested_cur2_amount
