#!/usr/bin/env python3

""" comme text.py/RubyText mais sans dépendance à Ruby """

import re

import MeCab
import furigana

from reccipe.file import Path

class Mecab() :
	def __init__(self, mecab_param='') :
		self.mecab = MeCab.Tagger(mecab_param)

	def escape_special(self, txt) :
		txt = txt.replace('\\｛', '__obrace__')
		txt = txt.replace('\\（', '__oparen__')
		return txt

	def restore_special(self, txt) :
		txt = txt.replace('__obrace__', '\\｛')
		txt = txt.replace('__oparen__', '\\（')
		return txt

	def clean(self, txt) :
		txt = self.escape_special(txt)
		txt = re.sub('（[^）]+?）', '', txt)
		txt = re.sub('｛[^｜]+?｜[^｝]+?｝', '', txt)
		txt = self.restore_special(txt)
		return txt

	def protect(self, txt) :
		txt = txt.replace('｛', '\\｛')
		txt = txt.replace('（', '\\（')
		return txt

	def text_prepare(self, txt) :
		txt = '\n'.join(line.strip() for line in txt.splitlines())
		txt = re.sub(r'\n\n+', r'\n\n', txt)
		txt = txt.replace('｛', '\｛').replace('（', '\（')
		return txt

	def to_html5(self, txt) :
		pass

	def process(self, txt) :
		txt = self.text_prepare(txt)
		paragraph = list()
		for phrase in txt.splitlines() :
			stack = list()
			for line in self.mecab.parse(phrase).splitlines() :
				if line == 'EOS' :
					break
				token, null, desc = line.partition('\t')
				desc_lst = [c if c != '*' else None for c in desc.split(',')]
				if (len(desc_lst) >= 6 and desc_lst[5] is not None) :
					p = furigana.Duplex(token, desc_lst[5])
					if p.is_equal() :
						stack.append(p._k_original)
					else :
						stack.append('｛{0}｜{1}｝'.format(p._k_original, p._f_normal))
				else :
					stack.append(token)
			paragraph.append(self.restore_special(''.join(stack)))
		return '\n'.join(paragraph)

def txt_to_html5(s) :
	m = furigana.mecab.Mecab("--dicdir=/var/lib/mecab/dic/juman-utf8")
	r = furigana.ruby.Ruby().default_config()
	t = m.process(s)
	print(t)

if __name__ == '__main__' :
	import sys
	txt_to_html5(Path(sys.argv[1]).read_text())
