#!/usr/bin/env python3

import re

import MeCab

from furigana.ruby import Ruby
from furigana.duplex import Duplex

class Text(Ruby) :
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

	def auto(self, txt, mecab_param='') :
		mecab = MeCab.Tagger(mecab_param)
		txt = self.escape_special(txt)
		print(txt)
		stack = list()
		for line in mecab.parse(txt).splitlines() :
			print(line)
			if line == 'EOS' :
				break
			token, null, desc = line.partition('\t')
			desc_lst = [c if c != '*' else None for c in desc.split(',')]
			if (len(desc_lst) > 7 and desc_lst[7] is not None) :
				p = Duplex(token, desc_lst[7])
				if p.is_equal() :
					stack.append(p._k_original)
				else :
					if self.split(p) is None :
						stack.append('｛{0}｜{1}｝'.format(p._k_original, p._f_normal))
					else :
						stack.append('{0}（{1}）'.format(p._k_original, p._f_normal))
			else :
				stack.append(token)
		txt = self.restore_special(''.join(stack))
		return txt


if __name__ == '__main__' :
	import sys

	u = RubyText().default_config()


	s = """
多くの先進国では1997年京都議定書の締結により、法的強制力のある断熱化基準を改正したり建造物の断熱化を新たに義務付けた。しかし、日本の断熱化基準には強制力が一切なく、複層ガラス普及率は先進国の中でも最低レベルである[5]。

1999年に建設省から日本の断熱化基準である次世代省エネルギー基準が改定された。しかし、法的拘束力がない上に、断熱化基準が欧米と比べてゆるく設定されている。2000年（平成12年）における日本の複層ガラスの普及率は5.1%となっており、欧州やその他の先進国と比較すると低い普及率となっている[5]。また、特殊な金属膜を設けた高断熱複層ガラスの普及率に関しては、米国が48.0%なのに対し、日本は0.3%と非常に低い数値となっている[6]。

その後も、世界各地での熱波や寒波の発生により、複層ガラスの世界的な需要は年ごとに高まっていったが、日本の普及率は低いままだった。背景として、市場でアルミサッシ（断熱性能は低い）が圧倒的に強く、複層ガラス向きの樹脂サッシ（断熱性能は高い）は北海道などの寒冷地を除いてほとんど普及していなかったことがある。

しかし、2011年の福島第一原子力発電所事故以降の電力不足を背景に、「アルミサッシ+単板ガラス」を「樹脂サッシ+複層ガラス」へ置き換える施策がにわかに活発化し、新たなビジネスチャンスとなっている[7]。
"""

	s = """
1999年に建設省から日本の断熱化基準である次世代省エネルギー基準が改定された。しかし、法的拘束力がない上に、断熱化基準が欧米と比べてゆるく設定されている。2000年（平成12年）における日本の複層ガラスの普及率は5.1%となっており、欧州やその他の先進国と比較すると低い普及率となっている[5]。また、特殊な金属膜を設けた高断熱複層ガラスの普及率に関しては、米国が48.0%なのに対し、日本は0.3%と非常に低い数値となっている[6]
"""

	r = u.auto(u.protect(s))

	p = u.clean(r)

	print(r)
	print(p)
