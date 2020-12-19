#!/usr/bin/env python3

import pivo.lang.ja

class Duplex() :
	def __init__(self, kanji, furigana) :
		
		self._k_original = kanji
		self._f_original = furigana
		self._k_normal = pivo.lang.ja.normalize(kanji)
		self._f_normal = pivo.lang.ja.normalize(furigana)
		
	def __str__(self) :
		return "original: {0} / {1} > normal: {2} / {3}".format(
			self._k_original, self._f_original,
			self._k_normal, self._f_normal
		)
		
	def __repr__(self) :
		return "Duplex({0!r}, {1!r})".format(self._k_original, self._f_original)
		
	def seek(self, i=None, j=None) :
		return (
			len(self._k_original) if i is None else i,
			len(self._f_original) if j is None else j
		)
		
	def is_equal(self) :
		return self._k_normal == self._f_normal
		
	def k_original(self, r, s=1) :
		l = r - s
		return self._k_original[l:r], l
		
	def k_normal(self, r, s=1) :
		l = r - s
		return self._k_normal[l:r], l

	def f_original(self, r, s=1) :
		l = r - s
		return self._f_original[l:r], l
		
	def f_normal(self, r, s=1) :
		l = r - s
		return self._f_normal[l:r], l		
		
	def normal(self, kr, fr, ks=1, fs=1) :
		kl, fl = kr - ks, fr - fs
		return self._k_normal[kl:kr], self._f_normal[fl:fr], kl, fl
		
	def original(self, kr, fr, ks=1, fs=1) :
		kl, fl = kr - ks, fr - fs
		return self._k_original[kl:kr], self._f_original[fl:fr], kl, fl
		
if __name__ == '__main__' :
	u = Duplex('引っ越す', 'ひっこす')
	