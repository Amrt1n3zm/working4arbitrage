#!/usr/bin/env bash

DIR=/home/pi/bitcoin/arbitrage/working4arbitrage/

rm ${DIR}data_in # ToFix ?
#touch ${DIR}lock/downloading.lock
touch /tmp/w4a_downloading.lock
python ${DIR}download_btc_orderbooks.py >> /tmp/w4a_download.log
#rm ${DIR}lock/downloading.lock
rm /tmp/w4a_downloading.lock
