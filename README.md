# Table PDF to CSV

Turns **scanned** PDF containing table to CSV, powered by Tesseract.

Crazy CPU hog because of parallelization.

If your PDF is not scanned, i.e., contains actual data,
please consider [Tabular](http://tabula.technology).

## Installation

1. Install the Python dependencies: `pip install -r requirements.txt`

2. Install poppler: `apt install poppler-utils`

3. Install Tesseract as per
https://github.com/tesseract-ocr/tesseract/wiki

## Usage

1. Turn PDF to images: `./pdf2img.py <PDF path>`

2. If necessary, do pre-processings on the images in `page.d`

3. Start the conversion: `./run.sh`

4. The CSV will be stored in `result.csv`

## Mechanism

1. Chops table into cells.

2. OCRs the cells with Tesseract.

3. Puts the OCRed cell texts together in their original positions, and generates the CSV.
