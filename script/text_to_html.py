#!/usr/bin/env python3

""" take and utf8 text, add furigana on it and output an html """

import sys

from reccipe.file import Path

import furigana

html_template = """<!DOCTYPE html>
<html>

	<head>
		<meta charset="utf-8">
		<title>{0}</title>
	</head>
	<body lang="ja">
{1}
	</body>
</html>
"""

txt = Path(sys.argv[1]).read_text()
