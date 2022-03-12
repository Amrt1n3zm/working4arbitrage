#!/usr/bin/env bash

if [[ $2 != 1 ]]
  then DIR=/home/pi/bitcoin/arbitrage/working4arbitrage/
fi;

function main(){
	python ${DIR}currency_exchange_via_btc.py --cur1 EUR --cur2 USD --size 10 --loop 900
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