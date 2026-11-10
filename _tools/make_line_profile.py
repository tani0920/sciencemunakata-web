# -*- coding: utf-8 -*-
"""LINE公式アカウントのプロフィール用画像をつくる（サイトと同じ見た目）
  （背景はサイトの共有画像 assets/img/ogp.jpg をそのまま使う。LINEが2:1に切り抜く）
  とは_vNN.jpg : 授業の写真＋「くわしくはWEBサイト／申し込みはLINEメニュー」 1200×600
使い方: python3 _tools/make_line_profile.py <書き出しフォルダ> <版番号>"""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, '..', 'assets', 'img')
OUT, VER = sys.argv[1], sys.argv[2]
FB = os.path.expanduser('~/Library/Fonts/FOT-GMaruGoPro-B.otf')
FM = os.path.expanduser('~/Library/Fonts/FOT-GMaruGoPro-M.otf')
INK, INK2, PINK, BLUE, GREEN = (38, 49, 77), (86, 96, 122), (230, 51, 111), (59, 111, 193), (6, 170, 72)
CREAM = (255, 251, 241, 255)


def grid_canvas(w, h):
    c = Image.new('RGBA', (w, h), CREAM)
    g = Image.new('RGBA', (w, h), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    for x in range(0, w, 30): gd.line([(x, 0), (x, h)], fill=(59, 111, 193, 20), width=1)
    for y in range(0, h, 30): gd.line([(0, y), (w, y)], fill=(59, 111, 193, 20), width=1)
    c.alpha_composite(g)
    return c


def paste(c, path, box_w, xy, rot=0):
    im = Image.open(os.path.join(IMG, path)).convert('RGBA')
    im = im.resize((box_w, round(im.height * box_w / im.width)), Image.LANCZOS)
    if rot: im = im.rotate(rot, expand=True, resample=Image.BICUBIC)
    c.alpha_composite(im, xy)


# とは：左に授業の写真、右に案内
W, H = 1200, 600
c = grid_canvas(W, H)
hill = Image.new('RGBA', (W, H), (0, 0, 0, 0)); hd = ImageDraw.Draw(hill)
hd.ellipse([-300, 520, 700, 880], fill=(166, 216, 138, 255))
hd.ellipse([420, 535, 1500, 940], fill=(93, 182, 62, 255))
c.alpha_composite(hill)

pw, ph, px, py = 640, 480, 40, 48
ph_im = Image.open(os.path.join(IMG, 'classes', '2026-04-25-mobile-scene.webp')).convert('RGBA')
s = max(pw / ph_im.width, ph / ph_im.height)
ph_im = ph_im.resize((round(ph_im.width * s), round(ph_im.height * s)), Image.LANCZOS)
ph_im = ph_im.crop(((ph_im.width - pw) // 2, (ph_im.height - ph) // 2, (ph_im.width - pw) // 2 + pw, (ph_im.height - ph) // 2 + ph))
mask = Image.new('L', (pw, ph), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, pw - 1, ph - 1], radius=30, fill=255)
sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([px, py + 10, px + pw, py + ph + 10], radius=30, fill=(38, 49, 77, 70))
c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(2)))
c.paste(ph_im, (px, py), mask)
d = ImageDraw.Draw(c)
d.rounded_rectangle([px, py, px + pw, py + ph], radius=30, outline=INK, width=6)

paste(c, 'deco/butterfly.webp', 58, (636, 18), 8)
paste(c, 'deco/leaf.webp', 62, (1118, 22), -10)
paste(c, 'chara/blue-1.webp', 120, (1060, 420))

f1 = ImageFont.truetype(FB, 40)
f2 = ImageFont.truetype(FM, 22)
f3 = ImageFont.truetype(FB, 22)


def line(parts, y, x, font):
    for text, col in parts:
        d.text((x, y), text, font=font, fill=col)
        x += font.getlength(text)


X = 724
# 1つめ：WEBサイト
d.text((X, 70), 'くわしくは', font=f2, fill=INK2)
line([('WEBサイト', BLUE), ('を', INK)], 102, X, f1)
line([('ご覧ください', INK)], 152, X, f1)
d.line([(X + 2, 148), (X + f1.getlength('WEBサイト') - 2, 148)], fill=(255, 197, 61), width=6)
url = 'sciencemunakata.tech'
uw = f3.getlength(url)
d.rounded_rectangle([X, 214, X + uw + 40, 258], radius=22, fill=(255, 255, 255), outline=INK, width=4)
d.text((X + 20, 222), url, font=f3, fill=INK)

d.line([(X, 300), (1150, 300)], fill=(38, 49, 77, 60), width=2)

# 2つめ：申し込み
d.text((X, 324), '授業のお申し込みは', font=f2, fill=INK2)
line([('LINEメニュー', GREEN), ('の', INK)], 356, X, f1)
line([('「申し込む」から', INK)], 406, X, f1)
d.line([(X + 2, 402), (X + f1.getlength('LINEメニュー') - 2, 402)], fill=(255, 197, 61), width=6)

c.convert('RGB').save(os.path.join(OUT, f'とは_v{VER}.jpg'), quality=90)
print('ok')
