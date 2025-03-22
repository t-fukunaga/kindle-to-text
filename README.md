# Kindle to PDF Converter for MacOS

A simple utility to capture Kindle pages from your screen and convert them to PDF format. This tool is designed specifically for MacOS users.

## Features

- Capture any portion of your screen containing Kindle content
- Automatically turn pages and capture each one
- Detect when you've reached the end of the book
- Convert all captured pages to a single high-quality PDF
- Simple, user-friendly interface

## Requirements

- Python 3.7 or higher
- MacOS (tested on Monterey and newer)
- Kindle app or Kindle Cloud Reader in a browser

## Installation

1. Clone this repository or download the script file:

```bash
git clone https://github.com/yourusername/kindle-to-pdf-mac.git
cd kindle-to-pdf-mac
```

2. Install required packages:

```bash
pip install -r requirements.txt
```



## Usage

1. Open your Kindle app and navigate to the book you want to capture
2. Run the script:

```bash
python kindle_to_pdf.py
```

3. Follow the prompts to:
   - Enter a name for your book
   - Position your cursor at the top-left corner of the reading area
   - Position your cursor at the bottom-right corner of the reading area
   - Wait for the capture process to complete

4. Find your PDF in the output folder (default: `~/Desktop/KindlePDF/your_book_name/`)

### Command Line Options

```
usage: kindle_to_pdf.py [-h] [--book BOOK] [--direction {right,left}]

optional arguments:
  -h, --help            show this help message and exit
  --book BOOK           Book name (used for folder naming)
  --direction {right,left}
                        Page turn direction (default: right)
```

## Customization

You can customize the behavior by creating a `.env` file in the same directory as the script with these settings:

```
OUTPUT_FOLDER=~/Documents/KindlePDF
PAGE_TURN_KEY=left
CAPTURE_DELAY=0.3
```

## Troubleshooting

### Pages are being skipped or not captured correctly

- Increase the `CAPTURE_DELAY` value in the `.env` file to give more time between page turns
- Make sure your Kindle app is in focus during capture
- Try using a smaller capture area to speed up the process

### The converter stops too early

- Some Kindle books have special pages that look similar - try manually checking if you've reached the end
- You can press Ctrl+C to stop the capture process at any time

## Limitations

- This tool works by taking screenshots and doesn't extract actual text content
- The quality of the PDF depends on your screen resolution
- DRM protection still applies to the content

## Legal Considerations

This tool is meant for personal use only to create backups of books you legally own. Please respect copyright laws and only use this for books you have purchased.