#!/usr/bin/env python3

from furigana import Ruby, Duplex, test

test(
	Ruby(explicit=True, debug=False).default_config().split,
	[
		[[Duplex('食べる', 'たべる'),], {}, [('食', 'た'), ('べる', 'べる')]],
		[[Duplex('たべる', 'たべる'),], {}, [('たべる', 'たべる')]],
		[[Duplex('昨日', 'きのう'),], {}, [('昨日', 'きのう')]],
		[[Duplex('昨日は', 'きのうは'),], {}, [('昨日', 'きのう'), ('は', 'は')]],
		[[Duplex('は昨日', 'はきのう'),], {}, [('は', 'は'), ('昨日', 'きのう')]],
		[[Duplex('止め', 'とどめ'),], {}, [('止', 'とど'), ('め', 'め')]],
	]
)

test(
	Ruby(explicit=False, debug=False).default_config().split,
	[
		[[Duplex('を食べる', 'たべる'),], {}, ['を', ('食', 'た'), ('べる', 'べる')]],
	]
)