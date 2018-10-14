# Table PDF to CSV

Turns PDF containing table to CSV, powered by Tesseract.

Crazy CPU hogger because of parallelization.

## Installation

1. Install the Python dependencies: `pip install -r requirements.txt`

2. Install Tesseract as per
https://github.com/tesseract-ocr/tesseract/wiki

## Usage

1. Turn PDF to images: `./pdf2img.py <PDF path>`

The images are stored in `page.d`

2. If necessary, do pre-processings on the images.

3. Start the conversion: `./run.sh`

4. The CSV will be stored in `result.csv`.

## Mechanism

1. Chops table to cells

2. OCRs the cells with Tesseract

3. Puts the OCRed cell text together in their original position, and generate the CSV.
