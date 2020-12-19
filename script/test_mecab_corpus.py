#!/usr/bin/env python3

import collections
from pathlib import Path

import pivo, reccipe

import furigana.test

u = furigana.test.RubyTest()

for pth in pivo.pth('repo/other/joyodb').glob('*.tsv') :
	u.load_furigana(pth)

for pth in pivo.pth('repo/other/kanjidic').glob('*.tsv') :
	u.load_furigana(pth)

u.load_furigana(pivo.pth('repo/local/lang/ja/furigana/supplementary_f.tsv'))

u.load_jukujikun(pivo.pth('repo/local/lang/ja/furigana/jukujikun.tsv'))

u.load_jukujikun(pivo.pth('repo/local/lang/ja/furigana/supplementary_j.tsv'))

if __name__ == '__main__' :
	import sys

	pth = pivo.pth('tmp/mecab/corpus.tsv')

	total_missing = {
		t : collections.defaultdict(set)
		for t in u.failure
	}
	irregular_map = collections.defaultdict(set)

	n = 0

	while n < 9 :
		error_set = set()
		print("round", n, file=sys.stderr)
		round_missing = {
			t : collections.defaultdict(set)
			for t in u.failure
		}
		for kanji, furigana in reccipe.data.tsv_load(pth) :
			result = u.split(kanji, furigana)
			if result is None :
				error_set.add((kanji, furigana))
			else :
				for k, f in result :
					if '#' not in f :
						continue
					f, null, t = f.partition('#')
					round_missing[t][k].add(f)
					total_missing[t][k].add(f)


		reccipe.data.json_dump(round_missing, Path("missing.{0}.json".format(n)), debug=True)

		# les irréguliers sont traités à part pour éviter la réinjection
		if round_missing['irregular'] :
			for k in round_missing['irregular'] :
				irregular_map[k] |= round_missing['irregular'][k]
		del round_missing['irregular']


		for t in round_missing :
			if (
				(round_missing['glottized'] or round_missing["voiced"]) or
				(t == 'soliton' or not round_missing['glottized'] or not round_missing["voiced"])
			) :
				for k in round_missing[t] :
					for f in round_missing[t][k] :
						u._push_furigana(k, f)

		if not (round_missing['glottized'] or round_missing["voiced"] or round_missing['soliton']) :
			break

		n += 1

	reccipe.data.json_dump(total_missing, Path("missing.json"), debug=True)

	total_missing['irregular'] = irregular_map
	
	for t in total_missing :
		stack = list()
		for k in sorted(total_missing[t]) :
			stack.append([k, * sorted(total_missing[t][k])])
		reccipe.data.tsv_dump(
			stack,
			pivo.pth('repo/other/mecab/{0}.tsv'.format(t)),
			mkdir='shared',
			comment="$PIVODIR/{0}".format(Path(__file__).absolute().relative_to(pivo.pivo_dir))
		)

	reccipe.data.tsv_dump(
		list(error_set),
		pivo.pth('tmp/mecab/error.tsv'),
		mkdir='shared',
		comment="$PIVODIR/{0}".format(Path(__file__).absolute().relative_to(pivo.pivo_dir))
	)
