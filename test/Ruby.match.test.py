#!/usr/bin/env python3

import pivo

import furigana
import furigana.load
import furigana.dump

furigana_db = dict()

furigana.load.furigana(pivo.pth('repo/local/lang/ja/furigana/joyodb.tsv'), furigana_db)
furigana.load.furigana(pivo.pth('repo/local/lang/ja/furigana/kanjidic.tsv'), furigana_db)

jukujikun_db = dict()

furigana.load.jukujikun(pivo.pth('repo/local/lang/ja/furigana/jukujikun.tsv'), jukujikun_db)	

u = furigana.Ruby(furigana_db, jukujikun_db, debug=False)

match_regression_map = {
	('さくらんぼ', 'さくらんぼ', None, None) : [(['さくらんぼ', 'さくらんぼ'], 0, 0),],
	('くさらんぼ', 'さくらんぼ', None, None) : [(['らんぼ', 'らんぼ'], 2, 2),],
	('さくらんぼ', 'さくらんぼ', 2, 2) : [(['さく', 'さく'], 0, 0),],
	('止', 'とど', None, None) : [(['止', 'ど'], 0, 1), (['止', 'とど'], 0, 0)],
	('昨日', 'きのう', None, None) : [(['昨日', 'きのう'], 0, 0),],
}

for k, v in match_regression_map.items() :
	print(">>> match({0!r}, {1!r}, {2}, {3}) ... ".format(* k), end='')
	r = list(u.match(* k))
	if r == v :
		print("\x1b[32mOK\x1b[0m")
	else :
		print("\x1b[31mKO\x1b[0m")
		print("exected:", v)
		print("obtained", r)

