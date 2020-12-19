#!/usr/bin/env python3

import reccipe

import pivo.lang.ja

def furigana(pth, db) :
	"""
	reading can contains:
	'-' to mark a suffix of prefix form
	'.' to mark the beginning of okurigana
	"""
	for k, * y_lst in reccipe.data.tsv_load(pth) :
		for y in y_lst :
			if k not in db :
				db[k] = dict()
			y = pivo.lang.ja.to_hiragana(y.strip('-').partition('.')[0])
			db[k][y] = 0
			
def irregular(pth, db) :
	"""
	readings are made of two values separated by a '/':
	the irregular reading
	the normal one it should refer to
	"""
	for k, * y_lst in reccipe.data.tsv_load(pth) :
		for y in y_lst :
			if k not in db :
				db[k] = dict()
			a, b = y.split('/')
			db[k][a] = b
			
def remove(pth, db) :
	"""
	readings to be removed
	"""
	for k, * y_lst in reccipe.data.tsv_load(pth) :
		for y in y_lst :
			if k in db and y in db[k] :
				del db[k][y]
			if not db[k] :
				del db[k]

def jukujikun(pth, db) :
	"""
	complex readings
	"""
	for k, * y_lst in reccipe.data.tsv_load(pth) :
		for y in y_lst :
			if k not in db :
				m = db
				for c in reversed(k) :
					if c not in m :
						m[c] = dict()
					m = m[c]
				m[y] = 0

