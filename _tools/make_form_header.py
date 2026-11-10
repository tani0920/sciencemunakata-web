# -*- coding: utf-8 -*-
"""Googleフォーム（入会申込み）のヘッダー画像をつくる。1600×400（フォームのヘッダーは横4:1）
サイトのOGP（make_ogp.py）と同じ部品・色づかい。
使い方: python3 _tools/make_form_header.py 書き出し先.png"""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, '..', 'assets', 'img')
OUT = sys.argv[1]
FB = os.path.expanduser('~/Library/Fonts/FOT-GMaruGoPro-B.otf')
INK, INK2, PINK, BLUE = (38, 49, 77), (86, 96, 122), (230, 51, 111), (59, 111, 193)
W, H = 1600, 400

c = Image.new('RGBA', (W, H), (255, 251, 241, 255))
grid = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(grid)
for x in range(0, W, 32):
    gd.line([(x, 0), (x, H)], fill=(59, 111, 193, 20), width=1)
for y in range(0, H, 32):
    gd.line([(0, y), (W, y)], fill=(59, 111, 193, 20), width=1)
c.alpha_composite(grid)


def paste(path, box_w, xy, rot=0):
    im = Image.open(os.path.join(IMG, path)).convert('RGBA')
    im = im.resize((box_w, round(im.height * box_w / im.width)), Image.LANCZOS)
    if rot:
        im = im.rotate(rot, expand=True, resample=Image.BICUBIC)
    c.alpha_composite(im, xy)
    return im.size


# 写真（だ円）
pw, ph, px, py = 560, 330, 960, 28
photo = Image.open(os.path.join(IMG, 'hero', '1.webp')).convert('RGBA')
s = max(pw / photo.width, ph / photo.height)
photo = photo.resize((round(photo.width * s), round(photo.height * s)), Image.LANCZOS)
photo = photo.crop(((photo.width - pw) // 2, (photo.height - ph) // 2, (photo.width - pw) // 2 + pw, (photo.height - ph) // 2 + ph))
mask = Image.new('L', (pw, ph), 0); ImageDraw.Draw(mask).ellipse([0, 0, pw - 1, ph - 1], fill=255)
sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse([px, py + 10, px + pw, py + ph + 10], fill=(38, 49, 77, 70))
c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(2)))
c.paste(photo, (px, py), mask)
d = ImageDraw.Draw(c)
d.ellipse([px, py, px + pw, py + ph], outline=INK, width=7)

# 丘
hill = Image.new('RGBA', (W, H), (0, 0, 0, 0)); hd = ImageDraw.Draw(hill)
hd.ellipse([-300, 340, 900, 620], fill=(166, 216, 138, 255))
hd.ellipse([600, 350, 1900, 680], fill=(93, 182, 62, 255))
c.alpha_composite(hill)

# 飾り・キャラクター・吹き出し
paste('deco/leaf.webp', 64, (1525, 40), -10)
paste('deco/butterfly.webp', 60, (900, 18), 8)
paste('deco/star.webp', 52, (1530, 250), 0)
paste('deco/flask.webp', 46, (690, 60), -8)
paste('chara/blue-1.webp', 120, (800, 270))
paste('naze-bubble.webp', 110, (770, 160), 4)

# ロゴ
paste('logo-color.png', 330, (70, 40))

# 見出し
d = ImageDraw.Draw(c)
f1 = ImageFont.truetype(FB, 64)
x = 74
for text, col in [('入会', PINK), ('のお申し込み', INK)]:
    d.text((x, 196), text, font=f1, fill=col)
    x += f1.getlength(text)
d.line([(78, 276), (78 + f1.getlength('入会') - 6, 276)], fill=(255, 197, 61), width=7)

f3 = ImageFont.truetype(FB, 26)
t = '小学生とご家族の 体験型科学教室'
tw = f3.getlength(t)
d.rounded_rectangle([72, 302, 72 + tw + 44, 352], radius=25, fill=(255, 255, 255), outline=INK, width=4)
d.text((94, 312), t, font=f3, fill=INK)

c.convert('RGB').save(OUT)
print('ok', OUT)
