#!/usr/bin/env python3

from PIL import Image
import subprocess
import os
from collections import defaultdict
import sys
import csv
import json

cell_d = sys.argv[1]
page = os.path.basename(cell_d).split(".")[0]

text_d = "tmp.d/text.d/" + page
if not os.path.exists(text_d):
    os.makedirs(text_d)

row = list()
row_number = None

def output(row):
    if row != None:
        with open("tmp.d/result.d/" + page + ".csv", "a") as output_file:
            csv.writer(output_file, quoting=csv.QUOTE_ALL).writerow(row)

for cell_path in sorted(os.listdir(cell_d)):
    file_parts = cell_path.split("-")
    y = file_parts[0]
    x = file_parts[1]
    
    if y != row_number:
        output(row)
        row = list()
        row_number = y
        print("[OCR] " + page + "-" + y)

    image_path = os.path.join(cell_d, cell_path)
    text_filename = os.path.join(text_d, cell_path)
    subprocess.run(["tesseract", "--psm", "6", image_path, text_filename])
    with open(text_filename + ".txt", "r") as text_file:
        cell_lines = list()
        for line in text_file.readlines():
            cell_lines.append(line.strip())
        row.append(" ".join(cell_lines))

output(row)
