# -*- coding: utf-8 -*-
"""YouTube チャンネルのバナー画像をつくる。2560×1440（OGP と同じデザイン）
使い方: python3 _tools/make_youtube_banner.py [書き出し先.jpg]
見える範囲：テレビ＝全体／パソコン＝まん中の横帯（2560×423）／スマホ＝そのまたまん中（1546×423）
→ ロゴとキャッチはスマホでも切れないまん中（1546×423）に、写真はパソコンで見える左右に置く。"""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, '..', 'assets', 'img')
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'youtube_banner.jpg')
FB = os.path.expanduser('~/Library/Fonts/FOT-GMaruGoPro-B.otf')
FM = os.path.expanduser('~/Library/Fonts/FOT-GMaruGoPro-M.otf')
INK, INK2, PINK, BLUE = (38, 49, 77), (86, 96, 122), (230, 51, 111), (59, 111, 193)
W, H = 2560, 1440
BY0, BY1 = (H - 423) // 2, (H + 423) // 2          # パソコンで見える帯
SX0, SX1 = (W - 1546) // 2, (W + 1546) // 2         # スマホでも見える範囲

c = Image.new('RGBA', (W, H), (255, 251, 241, 255))
grid = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(grid)
for x in range(0, W, 40):
    gd.line([(x, 0), (x, H)], fill=(59, 111, 193, 20), width=2)
for y in range(0, H, 40):
    gd.line([(0, y), (W, y)], fill=(59, 111, 193, 20), width=2)
c.alpha_composite(grid)


def paste(path, box_w, xy, rot=0):
    im = Image.open(os.path.join(IMG, path)).convert('RGBA')
    im = im.resize((box_w, round(im.height * box_w / im.width)), Image.LANCZOS)
    if rot:
        im = im.rotate(rot, expand=True, resample=Image.BICUBIC)
    c.alpha_composite(im, xy)
    return im.size


def oval_photo(src, pw, ph, px, py, focus=0.5):
    photo = Image.open(os.path.join(IMG, src)).convert('RGBA')
    s = max(pw / photo.width, ph / photo.height)
    photo = photo.resize((round(photo.width * s), round(photo.height * s)), Image.LANCZOS)
    ox = (photo.width - pw) // 2; oy = round((photo.height - ph) * focus)
    photo = photo.crop((ox, oy, ox + pw, oy + ph))
    mask = Image.new('L', (pw, ph), 0); ImageDraw.Draw(mask).ellipse([0, 0, pw - 1, ph - 1], fill=255)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse([px, py + 12, px + pw, py + ph + 12], fill=(38, 49, 77, 70))
    c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(3)))
    c.paste(photo, (px, py), mask)
    ImageDraw.Draw(c).ellipse([px, py, px + pw, py + ph], outline=INK, width=8)


# 丘（テレビで見える下の方）
hill = Image.new('RGBA', (W, H), (0, 0, 0, 0)); hd = ImageDraw.Draw(hill)
hd.ellipse([-500, 1180, 1300, 1900], fill=(166, 216, 138, 255))
hd.ellipse([900, 1230, 3100, 2000], fill=(93, 182, 62, 255))
c.alpha_composite(hill)

# 写真（パソコンで見える左右）
oval_photo('hero/2.webp', 430, 350, 50, BY0 + 30, 0.35)     # 火おこし
oval_photo('hero/4.webp', 430, 350, W - 480, BY0 + 30, 0.3)  # ツリーイング
paste('deco/leaf.webp', 80, (440, BY0 + 10), -12)
paste('deco/ladybug.webp', 70, (30, BY1 - 70), 10)
paste('deco/planet.webp', 80, (W - 120, BY1 - 90), 0)
paste('deco/paint.webp', 72, (W - 520, BY0 + 6), 8)

# テレビ用の飾り（上下）
for p, w, xy, r in [('deco/butterfly.webp', 90, (340, 260), 8), ('deco/star.webp', 70, (1250, 200), 0),
                    ('deco/flask.webp', 80, (2150, 250), -8), ('deco/pencil.webp', 80, (700, 1080), -15),
                    ('deco/beaker.webp', 80, (1900, 1060), 6), ('deco/star.webp', 56, (2380, 1100), 0)]:
    paste(p, w, xy, r)

# まん中（スマホでも見える）：ロゴ・札／キャッチ／キャラクター
lw, lh = paste('logo-color.png', 440, (SX0 + 60, BY0 + 62))
d = ImageDraw.Draw(c)
f3 = ImageFont.truetype(FB, 30)
t = '小学生とご家族の 体験型科学教室'
tw = f3.getlength(t)
bx, by = SX0 + 60 + (440 - tw - 52) // 2, BY0 + 62 + lh + 36
d.rounded_rectangle([bx, by, bx + tw + 52, by + 62], radius=31, fill=(255, 255, 255), outline=INK, width=5)
d.text((bx + 26, by + 14), t, font=f3, fill=INK)

f1 = ImageFont.truetype(FB, 72)


def line(parts, y, x, font=f1):
    for text, col in parts:
        d.text((x, y), text, font=font, fill=col)
        x += font.getlength(text)


tx = SX0 + 590
line([('しぜんの', INK), ('「なぜ？」', PINK), ('を', INK)], BY0 + 78, tx)
line([('かがく', BLUE), ('で あそぼう！', INK)], BY0 + 178, tx)
d.line([(tx + 4, BY0 + 268), (tx + f1.getlength('かがく') - 4, BY0 + 268)], fill=(255, 197, 61), width=9)
f2 = ImageFont.truetype(FM, 30)
d.text((tx + 2, BY0 + 300), '宗像の里山で、大学の先生と実験・観察・ものづくり。', font=f2, fill=INK2)

ch = Image.open(os.path.join(IMG, 'chara/blue-1.webp')).convert('RGBA')
cw = 150; chh = round(ch.height * cw / ch.width)
paste('chara/blue-1.webp', cw, (SX1 - cw - 30, BY1 - chh - 12))
paste('naze-bubble.webp', 140, (SX1 - 190, BY1 - chh - 150), 4)

c.convert('RGB').save(OUT, quality=90)
print('ok', OUT, os.path.getsize(OUT) // 1024, 'KB')
