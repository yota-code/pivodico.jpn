#!/usr/bin/env python3

import collections
import os

from cc_pathlib import Path

class FuriganaJukujikun() :
	def __init__(self) :
		self.data_pth = Path(os.environ["PIVODICO_furigana_DIR"]) / "data" / "reference" / "jukujikun.tsv"
		self.j_map = collections.defaultdict(set)
		self.load(self.data_pth)

	def load(self, pth) :
		if pth.suffix != '.tsv' :
			raise ValueError

		for k, * f_lst in pth.load() :
			self.j_map[k] |= set(f_lst)

	def save(self) :
		t_lst = list()

		for k in sorted(self.j_map) :
			t_lst.append([k,] + sorted(self.j_map[k]))

		print(f" --> {self.data_pth}")
		self.data_pth.save(t_lst)
