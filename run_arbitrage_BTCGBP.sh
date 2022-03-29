#!/usr/bin/env bash

if [[ $2 != 1 ]]
  then DIR=/home/pi/bitcoin/arbitrage/working4arbitrage/
fi;

function main(){
	python ${DIR}w4arbitrage.py --markets "intrsng|BTC/GBP bc|BTC/GBP mtgox|BTC/GBP" --action arbitrage --currency 20 --plot --reldiff 4 --loop 900 --nodownload --sendemail # 2>&1 | tee /tmp/w4arbitrage_BTCEUR.log
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
