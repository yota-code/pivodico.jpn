#!/usr/bin/env zsh

setopt ERR_EXIT

set -x

pushd $PIVODIR/reference/monash.edu.au/kanjidic
	./reference_to_repository.py
popd

cp $PIVODIR/repo/other/monash.edu.au/kanjidic/yomi.tsv $PIVODIR/repo/local/monash.edu.au/kanjidic/yomi.tsv

pushd $PIVODIR/source/furigana/script
	./repository_to_database.py
popd

json_to_javascript.py \
	/mnt/storage/pivodico/tmp/mecab/furigana_test_corpus.json \
	/mnt/storage/pivodico/data/furigana/yomi_tree.json > test_mecab.js

