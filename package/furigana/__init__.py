#!/usr/bin/env python3

__version__ = '1.0.0 # 20161014'

import types

from furigana.duplex import Duplex
from furigana.ruby import Ruby
from furigana.mecab import Mecab

def test(func, pool) :
	for pos, nam, ref in pool :
		h = '--- {0}({1})'.format(
			func.__name__, ', '.join(
				[repr(i) for i in pos] +
				['{0}={1!r}'.format(* p) for p in nam.items()]
			)
		)
		tst = func(* pos, ** nam)
		if isinstance(tst, types.GeneratorType) :
			tst = list(tst)
		if tst != ref :
			print("\x1b[31mKO\x1b[0m", h)
			print('expected: {0}'.format(ref))
			print('obtained: {0}'.format(tst))
		else :
			print("\x1b[32mOK\x1b[0m", h)
			if isinstance(tst, types.GeneratorType) :
				print('\n'.join(repr(i) for i in tst))
			else :
				print(tst)
