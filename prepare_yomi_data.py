#!/usr/bin/env python3

import os, sys
import json, pickle
import collections

from pathlib import Path

pivo_dir = Path(os.environ['PIVODIR'])
def pivo_pth(* k_lst) :
	return Path(pivo_dir, * k_lst)
	
with Path('./yomi_data.json').open('rt') as fid :
	txt = fid.read()
	
with Path('./yomi_data.js').open('wt') as fid :
	fid.write("yomi_data = {0};".format(txt))
	
