#!/usr/bin/env python3

import collections
import os
import unicodedata

from cc_pathlib import Path

import pivodico.jpn.tool as jpn_tool

lang_dir = Path(os.environ["PIVODICO_jpn_DIR"])

class Corpus() :
	def __init__(self, pth) :
		self.corpus_pth = pth.with_suffix('.tsv')
		self.corpus_map = collections.defaultdict(set)

	def normalize(self, txt) :
		txt = unicodedata.normalize("NFKC", txt)
		txt = jpn_tool.to_katakana_trm.translate(txt)
		return txt

	def load(self) :
		if self.corpus_pth.is_file() :
			for k, * f_lst in self.corpus_pth.load() :
				for f in f_lst :
					self.corpus_map[k].add(f)
		return self

	def save(self) :
		corpus_lst = list()
		for k in sorted(self.corpus_map) :
			corpus_lst.append([k,] + list(self.corpus_map[k]))
		self.corpus_pth.save(corpus_lst)

	def __enter__(self) :
		self.load()
		return self

	def __exit__(self, exc_type, exc_value, traceback) :
		self.save()

	def push_to_corpus(self, kanji, furigana) :
		kanji = self.normalize(kanji)
		furigana = self.normalize(furigana)

		if jpn_tool.only_hiragana_katakana_kanji_rec.match(kanji) and jpn_tool.any_kanji(kanji) and jpn_tool.only_katakana_rec.match(furigana) :
			if kanji and furigana :
				self.corpus_map[kanji].add(furigana)

	def __iter__(self) :
		for kanji in sorted(self.corpus_map) :
			for furigana in sorted(self.corpus_map[kanji]) :
				yield kanji, furigana

class CorpusTest() :
	def __init__(self) :
		self.joyodb_map = (lang_dir / "tmp" / f"joyodb.json").load()
		self.kanjidic_map = (lang_dir / "tmp" / f"kanjidic.json").load()

		self.potential_map = dict()
		for k in 'vpgi' :
			self.potential_map[k] = (lang_dir / "tmp" / f"potential_{k}.json").load()

		self.corpus_pth = (lang_dir / "tmp" / "corpus.tsv")
		self.corpus_obj = Corpus(self.corpus_pth).load()

	def run(self) :
		for kanji, furigana in self.corpus_obj :
			self.soliton_check(kanji, furigana)

	def soliton_check(self, kanji, furigana) :
		k_lst, f_lst = list(kanji), list(furigana)

		while k_lst and f_lst and k_lst[0] == f_lst[0] :
			k_lst.pop(0)
			f_lst.pop(0)
		while k_lst and f_lst and k_lst[-1] == f_lst[-1] :
			k_lst.pop(-1)
			f_lst.pop(-1)

		if len(k_lst) == 1 :
			self.furigana_check(k_lst[0], ''.join(f_lst), kanji, furigana)

	def furigana_check(self, k_part, f_part, k_source, f_source) :
		""" process to attempt to check a pair """
		k, f, u, m = self.pair_check(k_part, f_part, self.joyodb_map)
		if m == 'e' :
			k, f, u, m = self.pair_check(k_part, f_part, self.kanjidic_map)
			if m == 'e' :
				print(f"ERR -- {k_source} / {f_source} :: pair_check({k_part}, {f_part}) -> {self.joyodb_map.get(k_part, '**')} / {self.kanjidic_map.get(k_part, '**')}")
			else :
				print(f"KAN -- {k_source} / {f_source} :: pair_check({k_part}, {f_part}) -> {k}, {f}, {u}, {m} / {self.joyodb_map.get(k_part, '**')} / {self.kanjidic_map[k_part]}")
				return k, f, u, m
		else :
			print(f"JOY -- {k_source} / {f_source} :: pair_check({k_part}, {f_part}) -> {k}, {f}, {u}, {m} / {self.joyodb_map[k_part]}")
			return k, f, u, m
			
	def pair_check(self, k, furigana, r_map) :
		if k in r_map :
			f_lst = list()
			for f in r_map[k] :
				f = jpn_tool.to_katakana_trm.translate(f)
				f, e = f.split('.') if '.' in f else [f, None]
				f_lst.append((f, e))

			for f, e in f_lst :
				if furigana == f :
					return k, f, None, ''
				
			for f, e in f_lst :
				b = jpn_tool.add_dakuten_trm.translate(f[0]) + f[1:]
				if furigana == b :
					return k, f, b, 'b'

			for f, e in f_lst :
				p = jpn_tool.add_handakuten_trm.translate(f[0]) + f[1:]
				if furigana == p :
					return k, f, p, 'b'

			for f, e in f_lst :
				if f[-1] in 'コツ' :
					g = f[:-1] + 'ッ'
					if furigana == g :
						return k, f, g, 'g'

			for f, e in f_lst :
				if e is not None :
					i = f + e[0]
					if furigana == i :
						return k, f, i, 'i'
				
		return k, furigana, False, 'e'
		

if __name__ == '__main__' :
	u = CorpusTest().run()