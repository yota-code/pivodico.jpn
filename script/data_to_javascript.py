#!/usr/bin/env python3

import furigana.database

from pathlib import Path

import pivo
import reccipe

if __name__ = '__main__' :
	f = furigana.database.Furigana_map(
		pivo.pth('source/furigana/data/furigana.tsv')
	)
	j = furigana.database.Jukujikun_map(
		pivo.pth('source/furigana/data/jukujikun.tsv')
	)

	f_json =
