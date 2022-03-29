#!/usr/bin/env bash

MARKET=$1 #"intrsng|BTC/EUR"
LEVEL=$2 #0

echo "Testing MARKET=$MARKET with debug=$LEVEL"

if [[ $LEVEL == 0 ]]
  then python w4arbitrage.py --action printmk --markets "$MARKET" --printjson --printmk --nocalculate
elif [[ $LEVEL == 1 ]]
  then python w4arbitrage.py --action printmk --markets "$MARKET" --nodownload --printjson --printmk --nocalculate
elif [[ $LEVEL == 2 ]]
  then python w4arbitrage.py --action printmk --markets "$MARKET" --nodownload --printmk
elif [[ $LEVEL == 3 ]]
  then python w4arbitrage.py --action printmk --markets "$MARKET" --nodownload --printjson --printmk --showstats
elif [[ $LEVEL == 4 ]]
  then python w4arbitrage.py --action printmk --markets "$MARKET" --nodownload --printjson --printmk --showstats --plot
else
  echo "$0 mtgox|BTC/USD 0"
  python w4arbitrage.py --action printmk --markets "$MARKET" --printjson --printmk --showstats --plot
fi;
