#!/usr/bin/env bash

if [[ $2 != 1 ]]
  then DIR=/home/pi/bitcoin/arbitrage/working4arbitrage/
fi;

function main(){
	python ${DIR}w4arbitrage.py --markets "bc|BTC/EUR mtgox|BTC/EUR" --action arbitrage --currency1 10 --plot --reldiff -6 --loop 300 --sendpush --sendemail --nodownload
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
