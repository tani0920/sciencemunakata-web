# -*- coding: utf-8 -*-
"""SNSでシェアされたときの画像（OGP）をつくる。1200×630
使い方: python3 _tools/make_ogp.py [書き出し先]  （ふだんは assets/img/ogp.jpg）"""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, '..', 'assets', 'img')
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(IMG, 'ogp.jpg')
FB = os.path.expanduser('~/Library/Fonts/FOT-GMaruGoPro-B.otf')
FM = os.path.expanduser('~/Library/Fonts/FOT-GMaruGoPro-M.otf')
INK, INK2, PINK, BLUE = (38, 49, 77), (86, 96, 122), (230, 51, 111), (59, 111, 193)
W, H = 1200, 630

c = Image.new('RGBA', (W, H), (255, 251, 241, 255))
grid = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(grid)
for x in range(0, W, 30):
    gd.line([(x, 0), (x, H)], fill=(59, 111, 193, 20), width=1)
for y in range(0, H, 30):
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
pw, ph, px, py = 520, 430, 640, 70
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
hd.ellipse([-300, 545, 700, 900], fill=(166, 216, 138, 255))
hd.ellipse([420, 560, 1500, 960], fill=(93, 182, 62, 255))
c.alpha_composite(hill)

# 飾り・キャラクター・吹き出し
paste('deco/leaf.webp', 70, (1110, 40), -10)
paste('deco/butterfly.webp', 64, (700, 30), 8)
paste('deco/star.webp', 56, (1120, 455), 0)
paste('deco/flask.webp', 52, (1140, 300), -8)
paste('chara/blue-1.webp', 150, (585, 425))
paste('naze-bubble.webp', 132, (548, 318), 4)

# ロゴ
paste('logo-color.png', 300, (58, 46))

# キャッチコピー（色分け）
d = ImageDraw.Draw(c)
f1 = ImageFont.truetype(FB, 52)


def line(parts, y, x=60, font=f1):
    for text, col in parts:
        d.text((x, y), text, font=font, fill=col)
        x += font.getlength(text)


line([('しぜんの', INK), ('「なぜ？」', PINK), ('を', INK)], 205)
line([('かがく', BLUE), ('で あそぼう！', INK)], 275)
d.line([(64, 340), (64 + f1.getlength('かがく') - 4, 340)], fill=(255, 197, 61), width=6)

f2 = ImageFont.truetype(FM, 25)
d.text((62, 372), '宗像の里山で、大学の先生といっしょに', font=f2, fill=INK2)
d.text((62, 408), '実験・観察・ものづくり。', font=f2, fill=INK2)

# 札
f3 = ImageFont.truetype(FB, 24)
t = '小学生とご家族の 体験型科学教室'
tw = f3.getlength(t)
d.rounded_rectangle([60, 462, 60 + tw + 44, 512], radius=25, fill=(255, 255, 255), outline=INK, width=4)
d.text((82, 472), t, font=f3, fill=INK)

c.convert('RGB').save(OUT, quality=88)
print('ok', OUT)
