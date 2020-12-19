#!/usr/bin/env python3

import os

from pathlib import Path

import pivo
import reccipe

import furigana.database

import pivo.lang.ja

pivo_dir = Path(os.environ['PIVODIR'])

# def load_tsv(pth, yomi, mode='insert') :
# 	for k, * y_lst in reccipe.data.tsv_load(pth) :
# 		for y in y_lst :
# 			if mode == 'insert' :
# 				if k not in yomi :
# 					yomi[k] = dict()
# 				y = pivo.lang.ja.to_hiragana(y.strip('-').partition('.')[0])
# 				yomi[k][y] = 0
# 			elif mode == 'irregular' :
# 				a, b = y.split('/')
# 				yomi[k][a] = b
# 			elif mode == 'remove' :
# 				if k in yomi :
# 					if y in yomi[k] :
# 						del yomi[k][y]
# 			elif mode == 'jukujikun' :
# 				m = yomi
# 				for c in reversed(k) :
# 					if c not in m :
# 						m[c] = dict()
# 					m = m[c]
# 				m[y] = None

if __name__ == '__main__' :
	f = furigana.database.Furigana_map(
		* list(pivo.pth('repo/local/joyodb').glob('*.tsv')),
		* list(pivo.pth('repo/local/kanjidic').glob('*.tsv')),
		* list(pivo.pth('repo/local/mecab').glob('*.tsv'))
	)

	reccipe.data.debug(f, pivo.pth('source/furigana/data/furigana.py'))
	reccipe.data.json_dump(f, pivo.pth('source/furigana/data/furigana.dbg.json'), debug=True)
	reccipe.data.json_dump(f, pivo.pth('source/furigana/data/furigana.json'))

	f.dump(pivo.pth('source/furigana/data/furigana.tsv'))

	j = furigana.database.Jukujikun_map(
		pivo.pth('repo/local/lang/ja/furigana/jukujikun.tsv')
	)

	reccipe.data.debug(j, pivo.pth('source/furigana/data/jukujikun.py'))
	reccipe.data.json_dump(j, pivo.pth('source/furigana/data/jukujikun.dbg.json'), debug=True)
	reccipe.data.json_dump(j, pivo.pth('source/furigana/data/jukujikun.json'))

	pivo.pth('source/furigana/data/jukujikun.tsv').write_text(
		pivo.pth('repo/local/lang/ja/furigana/jukujikun.tsv').read_text()
	)
