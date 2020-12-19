#!/usr/bin/env python3

import json, pickle

with open("/mnt/storage/pivodico/data/furigana/yomi_tree.json", 'rt') as fid :
	u = json.load(fid)
	
print('命' in u['い']['め'][''])

