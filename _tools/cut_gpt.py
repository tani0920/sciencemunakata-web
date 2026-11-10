# -*- coding: utf-8 -*-
"""GPTでつくった画像（白背景）を、背景を透明にして切り出す。
アイコンのシートは3×3に分けて1個ずつ assets/img/icons/<名前>.webp に保存する。
使い方: python3 _tools/cut_gpt.py   （元画像は _tools/src/gpt/ に置く）"""
import os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'src', 'gpt')
import sys
# 書き出し先（OneDriveが遅いときは別フォルダに書き出してからコピーする）
IMG = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'assets', 'img')
os.makedirs(os.path.join(IMG, 'icons'), exist_ok=True)

SHEETS = {
    'icons-menu_v01.png':  ['news', 'classes', 'teachers', 'videos', 'play', 'join', 'contact', 'about', 'camera'],
    'icons-info_v01.png':  ['star', 'ticket', 'kid', 'calendar', 'pin', 'family', 'line', 'chat', 'mountain'],
    'icons-pages_v01.png': ['person', 'heart', 'work', 'history', 'rule', 'shield', 'fire', 'home', 'link'],
    # ヒーローの飾り（assets/img/deco/ に入る）
    'deco_v01.png': ['deco/leaf', 'deco/butterfly', 'deco/star', 'deco/planet', 'deco/flask', 'deco/beaker',
                     'deco/pencil', 'deco/paint', 'deco/ladybug'],
}
SINGLES = {  # 元画像: (保存名, 横幅px)
    'about-venn_v01.png': ('about-venn.webp', 760),
    'naze-bubble_v01.png': ('naze-bubble.webp', 520),
    # 形だけ左右反転したもの（_tools/flip_bubble.py でつくる）。「里山ラボって？」で使う
    'naze-bubble-flip.png': ('naze-bubble-flip.webp', 520),
}


def shift(m, dy, dx):
    o = np.zeros_like(m)
    h, w = m.shape
    o[max(dy, 0):h + min(dy, 0), max(dx, 0):w + min(dx, 0)] = m[max(-dy, 0):h + min(-dy, 0), max(-dx, 0):w + min(-dx, 0)]
    return o


def dilate(m):
    return m | shift(m, 1, 0) | shift(m, -1, 0) | shift(m, 0, 1) | shift(m, 0, -1)


def cutout(im):
    """外側につながっている白だけを透明にする（絵の中の白は残す）。ふちは白をにじみ抜きする"""
    a = np.asarray(im.convert('RGB')).astype(np.float32)
    mn = a.min(axis=2)
    white = mn > 232
    bg = np.zeros_like(white)
    bg[0, :] = white[0, :]; bg[-1, :] = white[-1, :]; bg[:, 0] = white[:, 0]; bg[:, -1] = white[:, -1]
    while True:
        nb = dilate(bg) & white
        if nb.sum() == bg.sum():
            break
        bg = nb
    alpha = np.where(bg, 0.0, 1.0)
    ring = dilate(dilate(bg)) & ~bg   # 背景のすぐ内側
    ra = np.clip((255 - mn) / 150.0, 0, 1)
    alpha = np.where(ring, np.maximum(ra, 0.0), alpha)
    al = np.maximum(alpha, 1e-3)[..., None]
    rgb = np.clip((a - 255 * (1 - al)) / al, 0, 255)
    out = np.dstack([rgb, alpha * 255]).astype(np.uint8)
    return Image.fromarray(out)


def split(prof, near, win=90):
    """near の近くで、絵のない（いちばん空いている）位置を区切りにする"""
    seg = prof[near - win:near + win]
    m = seg.min()
    idx = np.where(seg == m)[0]
    # いちばん長い空きの真ん中
    best, run = [], [idx[0]]
    for a, b in zip(idx, idx[1:]):
        if b == a + 1:
            run.append(b)
        else:
            best = max(best, run, key=len); run = [b]
    best = max(best, run, key=len)
    return near - win + best[len(best) // 2]


def main_blob(cell, gap=28):
    """セルの端に写り込んだ、となりのアイコンの切れはしを消す。
    縦・横それぞれ、すき間で区切ったまとまりのうち一番大きいものだけ残す"""
    a = np.asarray(cell).copy()
    for axis in (0, 1):
        prof = (a[..., 3] > 8).sum(axis=axis)
        runs, start, last = [], None, None
        for i, v in enumerate(prof):
            if v:
                if start is None:
                    start = i
                elif i - last > gap:
                    runs.append((start, last)); start = i
                last = i
        if start is not None:
            runs.append((start, last))
        if len(runs) > 1:
            lo, hi = max(runs, key=lambda r: prof[r[0]:r[1] + 1].sum())
            if axis == 0:
                a[:, :lo, 3] = 0; a[:, hi + 1:, 3] = 0
            else:
                a[:lo, :, 3] = 0; a[hi + 1:, :, 3] = 0
    return Image.fromarray(a)


def trim(im, pad_ratio=0.04, square=True):
    box = im.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
    im = im.crop(box)
    w, h = im.size
    s = max(w, h) if square else None
    pad = int(max(w, h) * pad_ratio)
    W, H = (s + pad * 2, s + pad * 2) if square else (w + pad * 2, h + pad * 2)
    c = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    c.paste(im, ((W - w) // 2, (H - h) // 2))
    return c


for f, names in SHEETS.items():
    sheet = cutout(Image.open(os.path.join(SRC, f)))
    W, H = sheet.size
    al = np.asarray(sheet)[..., 3] > 8
    ys = [0] + [split(al.sum(axis=1), H * k // 3) for k in (1, 2)] + [H]
    for i, name in enumerate(names):
        r, c = divmod(i, 3)
        band = al[ys[r]:ys[r + 1]]
        xs = [0] + [split(band.sum(axis=0), W * k // 3) for k in (1, 2)] + [W]
        cell = sheet.crop((xs[c], ys[r], xs[c + 1], ys[r + 1]))
        ic = trim(main_blob(cell)).resize((160, 160), Image.LANCZOS)
        out = os.path.join(IMG, name + '.webp') if '/' in name else os.path.join(IMG, 'icons', name + '.webp')
        os.makedirs(os.path.dirname(out), exist_ok=True)
        ic.save(out, quality=92, method=6)
for f, (name, width) in SINGLES.items():
    im = trim(cutout(Image.open(os.path.join(SRC, f))), 0.01, square=False)
    im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im.save(os.path.join(IMG, name), quality=90, method=6)
print('ok')
