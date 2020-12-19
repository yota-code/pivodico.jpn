#!/usr/bin/env python3

from furigana import Ruby, Duplex, test

test(
	Ruby(explicit=True, debug=True).default_config().match_jukujikun,
	[
		[[Duplex('ああ昨日', 'ああきのう'),], {}, [('昨日', 'きのう', 2, 2)]],
		[[Duplex('ああ昨日', 'ああキノウ'),], {}, [('昨日', 'キノウ', 2, 2)]],
	]
)