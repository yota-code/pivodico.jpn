#!/usr/bin/env python3

import reccipe

import pivo
import pivo.lang.ja

class Furigana_map(dict) :
	def __init__(self, * pth_lst) :
		for pth in pth_lst :
			self.load(pth)

	def load(self, pth) :
		for k, * f_lst in reccipe.data.tsv_load(pth) :
			for f in f_lst :
				g = None
				if '/' in f :
					f, null, g = f.partition('/')
				self.push(k, f, g)

	def push(self, k, f, g=None) :
		if k not in self :
			self[k] = dict()
		self[k][f] = g

	def dump(self, pth, mkdir=False, comment=None) :
		stack = list()
		for k in sorted(self) :
			stack.append([k,] + [
				('/'.join(v) if v[1] is not None else v[0])
				for v in sorted(self[k].items())
			])
		reccipe.data.tsv_dump(stack, pth, mkdir, comment)

	@staticmethod
	def is_voiced(a, b) :
		return (
			a != b and
			pivo.lang.ja.undiacritics(a[0]) == b[0] and
			a[1:] == b[1:]
		)

	def extract_voiced(self) :
		voiced_map = Furigana_map()
		for k in self :
			for f_a in self[k] :
				for f_b in self[k] :
					if self.is_voiced(f_a, f_b) :
						voiced_map.push(k, f_a, f_b)
		for k in voiced_map :
			for f in voiced_map[k] :
				del self[k][f]
		return voiced_map

	@staticmethod
	def is_glottized(a, b) :
		return (
			len(a) > 1 and
			a != b and
			a[:-1] == b[:-1] and
			a[-1] == 'っ' and
			b[-1] in 'くつ'
		)

	def extract_glottized(self) :
		glottized_map = Furigana_map()
		for k in self :
			for f_a in self[k] :
				for f_b in self[k] :
					if self.is_glottized(f_a, f_b) :
						glottized_map.push(k, f_a, f_b)
		for k in glottized_map :
			for f in glottized_map[k] :
				del self[k][f]
		return glottized_map

class Jukujikun_map(dict) :
	def __init__(self, * pth_lst) :
		for pth in pth_lst :
			self.load(pth)

	def load(self, pth) :
		for k, * j_lst in reccipe.data.tsv_load(pth) :
			for j in j_lst :
				m = self
				for c in reversed(k) :
					if c not in m :
						m[c] = dict()
					m = m[c]
				m[j] = None
