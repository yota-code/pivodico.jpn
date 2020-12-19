#!/usr/bin/env python3

import MeCab
import json, pickle
import os

from pathlib import Path

pivodir = Path(os.environ['PIVODIR'])
def pivo_pth(* k_lst) :
	return Path(pivodir, * k_lst)
	

sample = """
北海道には８月に続けてたくさんの台風が来て、多くの野菜に被害が出ています。十勝地方では、雨がとてもたくさん降って、畑に水が入ってじゃがいもや豆が悪くなったり、強い風でとうもろこしが倒れたりしました。

お菓子を作る会社の「カルビー」は、北海道のじゃがいもを使った４種類のポテトチップスを９月５日から売る予定でした。しかし、雨でじゃがいもが足りなくなったため、１０月ごろから売ることにしました。

南富良野町で「湖池屋」という会社のポテトチップスを作っている工場も、中に水が入ったため、休んでいます。
"""


"""
En unicode, il y a plus de katakana que d'hiragana, une fonction de conversion
ne peut donc pas être bijective

https://en.wikipedia.org/wiki/Katakana_(Unicode_block)
https://en.wikipedia.org/wiki/Hiragana_(Unicode_block)

"""

def hiragana_to_katakana(txt) :
	return ''.join(chr(ord(c) + 0x60) if '\u3041' <= c <= '\u3096' else c for c in txt)

def katakana_to_hiragana(txt) :
	return ''.join(chr(ord(c) - 0x60) if '\u30A1' <= c <= '\u30F6' else c for c in txt)

def kana_equal(a, b) :
	return htok(a) == htok(b)
	
def htok(h) :
	return chr(ord(h) + 0x60) if '\u3041' <= h <= '\u3096' else h

def set_ruby(txt) :
	for left, right in parse(txt) :
		if right[-1] == right[-2] :
			pass

class Furigana() :
	def __init__(self) :
		with pivo_pth('data', 'monash.edu.au/kanjidic/yomi_tree.pson').open('rb') as fid :
			self.yomi_tree = pickle.load(fid)
		self.mecab = MeCab.Tagger("")
		print(self.mecab)
		
	def split(self, kanji, furigana) :
		base = hiragana_to_katakana(kanji)
		for c in base :
			if c in self.yomi_map :
				for p in self.yomi_map[c] :
					print('* ', p)
			else :
				print(c)

	def parse(self, txt) :
		stack = list()
		parsed = self.mecab.parse(txt)
		for line in parsed.split('\n') :
			if not line.strip() :
				continue
			if line.strip() == 'EOS' :
				return stack
			left, null, right = line.partition('\t')
			item = (left, [(c if c != '*' else None) for c in right.split(',')][-2])
			stack.append(item)
		return stack
		
	def match_ruby(self, kanji_lst, furigana_lst, result=None, depth=0) :
		if result is None :
			result = list()
		kanji = kanji_lst.pop(0)
		if kanji in self.yomi_map :
			while True :
				c = furigana_lst.pop(0)
				m = self.yomi_map[c]
				print(m)
				if None in m :
					return self.match_ruby(kanji_lst, furigana_lst, result, depth+1)
		else :
			result.append(kanji)
				
			print(self.yomi_map[kanji[0]])
		return result
		
	def split_ruby(self, kanji, furigana) :
		result = list()
		while furigana :
			k = kanji[0]
			f = furigana[0]
			if kana_equal(k, f) :
				result.append(k)
				furigana = furigana[1:]
				kanji = kanji[1:]
				continue
			m = self.yomi_tree
			for i, f in enumerate(furigana) :
				if f in m :
					if None in m[f] :
						if k in m[f][None] :
							result.append((k, furigana[:i+1]))
							furigana = furigana[i+1:]
							kanji = kanji[1:]
							break
				m = m[f]
		return result
		
	def set_ruby(self, txt) :
		stack = list()
		for item in self.parse(txt) :
			furigana = katakana_to_hiragana(item[1])
			if hiragana_to_katakana(item[0]) == item[1] :
				print("OK", item)
				stack.append(item[0])
			else :
				print("KO", item)
				stack.append([item[0], furigana])
		print(''.join(
			item if isinstance(item, str) else "{0}（{1}）".format(* item)
			for item in stack
		))
		#print(''.join(
		#	item if isinstance(item, str) else "\\rb{{{0}|{1}}}".format(* item)
		#	for item in stack
		#))
		
		#self.split(* stack[0])


if __name__ == '__main__' :

	u = Furigana()
	#u.set_ruby('引っ越しました')
	
	#u.split_ruby('引っ越しました', 'ひっこしました')
	
	#u.split_ruby('運ぶ', 'はこぶ')
	#u.split_ruby('運ぶつ', 'はこぶ')
	
	
	u = Furigana().set_ruby(sample)



