#!/usr/bin/env bash

rm -rf tmp.d
mkdir -p tmp.d/cell.d
mkdir tmp.d/result.d
mkdir tmp.d/text.d

for page in $(ls page.d); do
  ./chop.py "page.d/$page" &
done
wait

for cell_page in $(ls tmp.d/cell.d); do
  ./ocr.py "tmp.d/cell.d/$cell_page" 2>/dev/null &
done
wait

touch result.csv
for result in $(ls tmp.d/result.d); do
  echo "[merge] $result"
  cat "tmp.d/result.d/$result" >> result.csv
done

rm -rf tmp.d
