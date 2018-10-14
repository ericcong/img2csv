#!/usr/bin/python3

from PIL import Image, ImageEnhance
import sys
import os
import threading
from operator import itemgetter
from itertools import groupby
from collections import defaultdict

LEFT_MARGIN = 1
RIGHT_MARGIN = 1
TOP_MARGIN = 1
BOTTOM_MARGIN = 1
BLANK = (255, 255, 255)
CONTRAST_ENHANCEMENT_FOR_BORDER = 10
SHARPNESS_ENHANCEMENT_FOR_BORDER = 10

def find_margins(height, width, getpixel):
    left_margins = defaultdict(int)
    right_margins = defaultdict(int)
    for y in range(height):
        left_margin = 0
        for x in range(width // 2):
            if getpixel(x, y) == BLANK:
                left_margin += 1
            else:
                break
        left_margins[left_margin] += 1

        right_margin = 0
        for x in range(width - 1, width // 2 - 1, -1):
            if getpixel(x, y) == BLANK:
                right_margin += 1
            else:
                break
        right_margins[right_margin] += 1
    return (max(left_margins, key = left_margins.get),
            max(right_margins, key = right_margins.get))

def crop(img):
    img = (ImageEnhance.Contrast(ImageEnhance.Sharpness(img)
            .enhance(SHARPNESS_ENHANCEMENT_FOR_BORDER))
            .enhance(CONTRAST_ENHANCEMENT_FOR_BORDER))

    left_margin, right_margin = find_margins(
            img.height, img.width, lambda x, y: img.getpixel((x, y)))

    top_margin, bottom_margin = find_margins(
            img.width, img.height, lambda y, x: img.getpixel((x, y)))

    return img.crop((left_margin + 1,
                     top_margin + 1,
                     img.width - right_margin,
                     img.height - bottom_margin))

def get_groups(max_value, raw_list):
    groups = list()
    for k, g in groupby(
            enumerate(set(range(max_value)) - set(raw_list)),
            lambda x: x[0] - x[1]):
        group = (map(itemgetter(1), g))
        group = list(map(int, group))
        groups.append((group[0], group[-1]))
    return groups

print("[chop] " + sys.argv[1])

img = crop(Image.open(sys.argv[1]))
border_enhanced_img = (ImageEnhance.Contrast(
    ImageEnhance.Sharpness(img).enhance(SHARPNESS_ENHANCEMENT_FOR_BORDER))
    .enhance(CONTRAST_ENHANCEMENT_FOR_BORDER))

row_lines = list()

for y in range(border_enhanced_img.height):
    reference = border_enhanced_img.getpixel((0, y))
    is_row_line = True
    for x in range(1, border_enhanced_img.width):
        if border_enhanced_img.getpixel((x, y)) != reference:
            is_row_line = False
            break
    if is_row_line:
        row_lines.append(y)

rows = get_groups(img.height, row_lines)

row_imgs = list()

for start_y, end_y in rows:
    if start_y == end_y:
        continue
    row_imgs.append(img.crop((
        0, start_y + TOP_MARGIN, img.width, end_y - BOTTOM_MARGIN)))

for i in range(len(row_imgs)):
    col_lines = list()
    for x in range(border_enhanced_img.width):
        reference = border_enhanced_img.getpixel((x, rows[i][0]))
        is_col_line = True
        for y in range(1, rows[i][1] - BOTTOM_MARGIN + 1):
            if border_enhanced_img.getpixel((x, y)) != reference:
                is_col_line = False
                break
        if is_col_line:
            col_lines.append(x)

    cols = list()
    cols = get_groups(img.width, col_lines)
    
    col_imgs = list()

    for start_x, end_x in cols:
        if start_x == end_x:
            continue
        col_imgs.append(row_imgs[i].crop((
            start_x + LEFT_MARGIN,
            TOP_MARGIN,
            end_x - RIGHT_MARGIN,
            rows[i][1] - BOTTOM_MARGIN - rows[i][0] - TOP_MARGIN)))

    for j in range(len(col_imgs)):
        try:
            page = os.path.basename(sys.argv[1]).split(".")[0]
            if not os.path.exists("tmp.d/cell.d/" + page):
                os.makedirs("tmp.d/cell.d/" + page)
            col_imgs[j].save("tmp.d/cell.d/" + page + "/"
                    + str(i).zfill(3) + "-" + str(j).zfill(3) + ".png")
        except Exception:
            continue

