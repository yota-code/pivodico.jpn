#!/usr/bin/env python3

import reccipe

def dump(db, pth) :
	stack = list()
	for k in sorted(db) :
		if not db[k] :
			continue
		stack.append([k, * [
			(a if db[k][a] is None else "{0}/{1}".format(a, db[k][a]))
			for a in sorted(db[k])
		]])
	reccipe.data.tsv_dump(stack, pth)
