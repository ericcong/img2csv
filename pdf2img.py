#!/usr/bin/env python3

from pdf2image import convert_from_path
import sys

i = 0
for img in convert_from_path(sys.argv[1], dpi=600):
    print("Export page " + str(i))
    img.save("page.d/page" + str(i).zfill(3) + ".png")
    i += 1
