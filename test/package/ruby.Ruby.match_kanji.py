#!/usr/bin/env python3

from furigana import Ruby, Duplex, test

test(
	Ruby(explicit=True, debug=False).default_config().match_kanji,
	[
		[[Duplex('ああ止', 'ああとど'),], {}, [('止', 'ど', 2, 3), ('止', 'とど', 2, 2)]],
	]
)
