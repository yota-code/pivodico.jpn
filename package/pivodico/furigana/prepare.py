#!/usr/bin/env python3

"""
the main source is the jpn/data/reference/joyodb.tsv file, which is extracted from the project joyodb
"""

import collections
import os

from cc_pathlib import Path

data_dir = Path(os.environ["PIVODICO_jpn_DIR"]) / "data"

joyodb_map = collections.defaultdict(set)
for k, * f_lst in Path(data_dir / "reference" / "joyodb.tsv") :
	for f in f_lst :
		if '.' in f :
			f, a = f.split('.')
		joyodb_map[k].add(f)