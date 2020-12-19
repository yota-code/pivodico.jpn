#!/usr/bin/env python3

from furigana import Ruby, Duplex, test

test(
	Ruby(explicit=True, debug=False).default_config().match_kana,
	[
		[[Duplex('ふりがな', 'ふりがな'),], {}, ('ふりがな', 'ふりがな', 0, 0)],
		[[Duplex('ふりがな', 'フリガナ'),], {}, ('ふりがな', 'フリガナ', 0, 0)],
		[[Duplex('ふりがな', 'おくりがな'),], {}, ('りがな', 'りがな', 1, 2)],
		[[Duplex('ばっべびぼぶ', 'へー'),], {}, None],
		[[Duplex('たてちとぶ', 'ばべびぼぶ'),], {}, ('ぶ', 'ぶ', 4, 4)],
		[[Duplex('は昨日', 'はきのう'), 1, 1 ], {}, ('は', 'は', 0, 0)],
	]
)
