#!/usr/bin/env python3

from furigana.ruby import Duplex

u = Duplex('泳ぐ', 'オヨグ')

i, j = u.seek()

i, j = u.seek()

print(u.normal(i, j, 3))
print(u.original(i, j, 3))
print(u.k_normal(i, 2))