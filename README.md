# img2csv

Turns a set of table images to one CSV, powered by Tesseract.

Crazy CPU hog because of parallelization.

## Installation

1. Install the Python dependencies: `pip install -r requirements.txt`

2. Install Tesseract as per
https://github.com/tesseract-ocr/tesseract/wiki

## Usage

1. Put images to `page.d`, with **ordered** filenames.

2. If necessary, do pre-processings on the images to make them contain only tables.

3. Start the conversion: `./run.sh`

4. The CSV will be stored in `result.csv`

## Mechanism

1. Chops table into cells.

2. OCRs the cells with Tesseract.

3. Puts the OCRed cell texts together in their original positions, and generates the CSV.
