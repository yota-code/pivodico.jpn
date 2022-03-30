#!/usr/bin/env python3

import collections
import os
import re
import unicodedata

from cc_pathlib import Path

from pivodico.generic.tool.translate import TransMap

translate_dir = Path(os.environ["PIVODICO_jpn_DIR"]) / "data" / "translate"

# http://www.localizingjapan.com/blog/2012/01/20/regular-expressions-for-japanese-text/

jpn_map = {
	"hiragana" : r'\u3041-\u3096',
	"katakana" : r'\u30A0-\u30FF',
	"kanji" : r'\u3400-\u4DB5\u4E00-\u9FCB\uF900-\uFA6A',
}

def jpn_catch(* arg_lst, only=False) :
	range_lst = list()
	for arg in arg_lst :
		range_lst.append(jpn_map[arg])
	range_txt = r''.join(range_lst)
	if only :
		return re.compile(r'^[{0}]+$'.format(range_txt), re.UNICODE)
	else :
		return re.compile(r'[{0}]+'.format(range_txt), re.UNICODE)


# is_kanji_rec = re.compile(r'^[{0}]+$'.format(hiragana_range), re.UNICODE)
# only_hiragana_rec = re.compile(r'^[{0}]+$'.format(hiragana_range), re.UNICODE)
only_katakana_rec = jpn_catch("katakana", only=True)
only_hiragana_katakana_kanji_rec = jpn_catch("hiragana", "katakana", "kanji", only=True)

def is_only_hiragana(txt) :
	return only_hiragana_rec.match(txt) is not None

rem_dakuten_trm = TransMap(translate_dir / "dakuten.tsv")
add_dakuten_trm = ~ rem_dakuten_trm

rem_handakuten_trm = TransMap(translate_dir / "handakuten.tsv")
add_handakuten_trm = ~ rem_handakuten_trm

rem_diacritics_trm = rem_dakuten_trm | rem_handakuten_trm

to_katakana_trm = TransMap(translate_dir / "katakana.tsv")

def any_kanji(s) :
        return any(unicodedata.name(c).startswith("CJK UNIFIED IDEOGRAPH") for c in s)

def all_kanji(s) :
        return all(unicodedata.name(c).startswith("CJK UNIFIED IDEOGRAPH") for c in s)

def normalize(s) :
	s_lst = to_katakana_trm.translate(s)
	r_lst = list()
	for n, c in enumerate(s_lst) :
		if c in '々〻ゝ' :
			r_lst.append(prev_c)
		elif c == 'ー' :
			if prev_c in 'イィキギシジチヂニヒビピミヰエェケゲセゼテデヘベペメヱ' :
				r_lst.append('イ')
			elif prev_c in 'ウゥクグスズツヅヌフブプムユュオォコゴソゾトドホボポモヨョ' :
				r_lst.append('ウ')
			else :
				r_lst.append('ア')
		elif c == 'ヾ' :
			r_lst.append(add_dakuten_trm.translate(prev_c))
		else :
			r_lst.append(c)
		prev_c = c
	return ''.join(r_lst)

def find_glotized(f, * g_lst) :
	if len(f) > 1 and f[-1] == 'ッ' :
		for g in g_lst :
			if g[-1] in 'コツ' and g[:-1] == f :
				return f, g

def find_voiced(f, g_lst) :
	if len(f) > 1 and f[-1] == 'ッ' :
		for g in g_lst :
			if g != f and g[-1] in 'コツ' and g[:-1] == f[:-1] :
				return f, g




		# while kanji and furigana and kanji[-1] == furigana[-1] :
		# 	kanji = kanji[:-1]
		# 	furigana = furigana[:-1]
		# while kanji and furigana and kanji[0] == furigana[0] :
		# 	kanji = kanji[1:]
		# 	furigana = furigana[1:]

if __name__ == '__main__' :

	t_lst = [
		'人々',
		'ラーメン',
		'ニュース',
		'へゞ'
	]
	for t in t_lst :
		print(normalize(t))
