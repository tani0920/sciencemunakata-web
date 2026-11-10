# -*- coding: utf-8 -*-
"""「なぜ？」の吹き出しを、形だけ左右反転させる（文字の「なぜ？」は反転させない）。
_tools/src/gpt/naze-bubble_v01.png → _tools/src/gpt/naze-bubble-flip.png
できたあと python3 _tools/cut_gpt.py で背景を抜く"""
import os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'src', 'gpt', 'naze-bubble_v01.png')
OUT = os.path.join(HERE, 'src', 'gpt', 'naze-bubble-flip.png')


def shift(m, dy, dx):
    o = np.zeros_like(m); h, w = m.shape
    o[max(dy, 0):h + min(dy, 0), max(dx, 0):w + min(dx, 0)] = m[max(-dy, 0):h + min(-dy, 0), max(-dx, 0):w + min(-dx, 0)]
    return o


def flood(seed, allowed):
    reg = seed & allowed
    while True:
        n = (reg | shift(reg, 1, 0) | shift(reg, -1, 0) | shift(reg, 0, 1) | shift(reg, 0, -1)) & allowed
        if n.sum() == reg.sum():
            return reg
        reg = n


a = np.asarray(Image.open(SRC).convert('RGB')).copy()
H, W = a.shape[:2]
white = a.min(axis=2) > 200
# 吹き出しの中の白（文字のすぐ上あたりを起点にする）
seed = np.zeros_like(white); seed[300, W // 2] = True
assert white[300, W // 2], '起点が白ではありません'
inside = flood(seed, white)
# 外側（画面のふちにつながる部分）
border = np.zeros_like(white); border[0, :] = border[-1, :] = border[:, 0] = border[:, -1] = True
outer = flood(border, ~inside)
text = ~inside & ~outer                     # 吹き出しの中に囲まれた部分＝文字
ys, xs = np.where(text)
cx = (xs.min() + xs.max()) / 2

f = a[:, ::-1].copy()                       # まるごと反転
f[(inside | text)[:, ::-1]] = 255           # 反転した中身（文字）を消して白に
dx = int(round((W - 1 - cx) - cx))          # 文字は反転せず、反転後の吹き出しの中央へ
ty, tx = np.where(text)
f[ty, tx + dx] = a[ty, tx]
Image.fromarray(f).save(OUT)
print('ok', xs.min(), xs.max(), ys.min(), ys.max(), 'dx', dx)
