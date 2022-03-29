#!/usr/bin/env bash

if [[ $2 != 1 ]]
  then DIR=/home/pi/bitcoin/arbitrage/working4arbitrage/
fi;

function main(){
	python ${DIR}w4arbitrage.py --markets "vcx|BTC/USD intrsng|BTC/USD cbx|BTC/USD bc|BTC/USD rock|BTC/USD bitme|BTC/USD btc24|BTC/USD bitfloor|BTC/USD btce|BTC/USD bitstamp|BTC/USD mtgox|BTC/USD" --action arbitrage --currency1 20 --plot --reldiff 4 --loop 900 --nodownload --sendpush #--sendemail # 2>&1 | tee /tmp/w4arbitrage_BTCUSD.log
}

if [[ $1 == 1 ]]
  then main
else

	while [[ $1 != 1 ]]
	do
		main
		DELAY=120
		echo "Restart... after $DELAY s"
		sleep $DELAY
	done

fi;
