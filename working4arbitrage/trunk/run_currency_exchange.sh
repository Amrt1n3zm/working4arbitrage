#!/usr/bin/env bash
python currency_exchange.py --send EUR --req USD --send_amount 100
neato -T png path.dot > path.png # Graphviz
open path.png