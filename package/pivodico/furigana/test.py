#!/usr/bin/env python3

import collections
import re
from pathlib import Path

import reccipe

import pivo

import furigana
import furigana.load
import furigana.dump

class RubyTest(furigana.Ruby) :
	def __init__(self, debug=False) :
				
		self.result = collections.defaultdict(dict)
		
		furigana.Ruby.__init__(self, debug=debug)
		
		self.irregular = reccipe.data.json_load(pivo.pth("tmp/jmdict/irregular.json"))
		
		self.failure = {
			'soliton' : self._failed_split_soliton,
			'voiced' : self._failed_kanji_voiced,
			'glottized' : self._failed_kanji_glottized,			
			'irregular' : self._failed_kanji_irregular,			
		}
		
	def save_pass(self, p) :
		furigana.dump.dump(self.missing, Path("pass.{0}.tsv".format(p)))					
		for k in self.missing :
			for f in self.missing[k] :
				if k not in self.furigana :
					self.furigana[k] = dict()
				self.furigana[k][f] = self.missing[k][f]
				if k not in self.result :
					self.result[k] = dict()				
				self.result[k][f] = self.missing[k][f]
		self._f_longest = None
		p = len(self.missing)
		self.missing.clear()
		return p
		
	def _failed_kanji_voiced(self, k, f) :
		r = pivo.lang.ja.undiacritics(f)
		if r in self.furigana[k] :
			#print("voiced: {0}\t{1}/{2}".format(k, f, r))	
			yield "{0}/{1}".format(f, r)
			
	def _failed_kanji_glottized(self, k, f) :
		if f.endswith('っ') and len(f) > 1 :
			for p in ['く', 'つ'] :
				r = f[:-1] + p
				if r in self.furigana[k] :
					#print("glottized: {0}\t{1}/{2}".format(k, f, r))
					yield "{0}/{1}".format(f, r)
					
	def _failed_kanji_irregular(self, k, f) :
		if k in self.irregular and f in self.irregular[k] :
			yield "{0}/{1}".format(f, self.irregular[k][f])
					
	def failed_match_kanji(self, w, i, j, depth=0) :
		self.dbg(">>> Ruby.failed_match_kanji({0}, {1}, {2}, {3})".format(
			w._k_original, w._f_original, i, j
		), depth=depth)
		k, p = w.k_normal(i)
		if k in self.furigana :
			for z in range(1, min(j, self.f_longest[k])+1) :
				f, q = w.f_normal(j, z)
				for t in ['voiced', 'glottized', 'irregular'] :
					yield from (
						(k, r + '#' + t, p, q) for r in self.failure[t](k, f)
					)
	
	def failed_split(self, w) :
		result = None
		for t in ['soliton',] :
			result = self.failure[t](w)
			if result is not None :
				break
		return result

	def _failed_split_soliton(self, w) :
		""" try if some unambiguous readings can be guessed using regular expressions """
		kanji, furigana = w._k_normal, w._f_normal
		
		if not pivo.lang.ja.is_hiragana(furigana) :
			# readings contains unexpected characters, give up.
			return None
			
		soliton_rep = ''.join((c if c in furigana else 'x') for c in kanji)
		if 'xx' in soliton_rep :
			# not suitable for unique guess
			self.dbg("soliton:pattern not suitable: {0}".format(soliton_rep))
			return None
			
		soliton_rec = re.compile('^' + soliton_rep.replace('x', '(.+)') + '$', re.UNICODE)
		furigana_res = soliton_rec.match(furigana)
		kanji_res = soliton_rec.match(kanji)
		
		if (
			(furigana_res is None) or
			(kanji_res is None) or
			(len(kanji_res.groups()) != len(furigana_res.groups()))
		) :
			self.dbg("soliton:unmatching soliton")
			return None
			
		result = list()
		k_start, f_start = None, None
		for i in range(len(kanji_res.groups())) :
			k_end, k_next = kanji_res.span(i+1)
			f_end, f_next = furigana_res.span(i+1)
			if kanji[k_start:k_end] :
				result.append((kanji[k_start:k_end], furigana[f_start:f_end]))
			k, f = kanji_res.group(i+1), furigana_res.group(i+1)
			# TODO: là on pourrait plutôt tester si c'est un kanji...
			if k not in self.furigana :
				return None
			result.append((k, f + ("" if f in self.furigana[k] else "#soliton")))
			k_start, f_start = k_next, f_next
		if kanji[k_start:] :
			result.append((kanji[k_start:], furigana[f_start:]))
		
		return result
					
if __name__ == '__main__' :
	
	import sys
	
	u = RubyTest(debug=True)
	
	u.load_furigana(pivo.pth('repo/local/lang/ja/furigana/joyodb.tsv'))
	u.load_furigana(pivo.pth('repo/local/lang/ja/furigana/kanjidic.tsv'))
	
	u.load_furigana(pivo.pth('repo/local/lang/ja/furigana/supplementary_f.tsv'))
	
	u.load_furigana(pivo.pth('repo/local/lang/ja/furigana/irregular.tsv'))
	
	u.load_jukujikun(pivo.pth('repo/local/lang/ja/furigana/jukujikun.tsv'))
	
	u.load_jukujikun(pivo.pth('repo/local/lang/ja/furigana/supplementary_j.tsv'))
	
	#kanji, furigana = '牛ケ瀬西ノ口', 'うしがせにしのくち'
	kanji, furigana = '牛ヶ首ノ鼻', 'うしがくびのはな'
	
	

	#kanji, furigana = '牛ノ戸焼', 'うしのとやき'
	#kanji, furigana = '閥桜', 'ばっさぐら'
	#kanji, furigana = '桜', 'さぐら'
	kanji, furigana = '食る', 'たべる'
	kanji, furigana = '引出し', 'ひきだし'
	print(u.split(kanji, furigana))
	
	