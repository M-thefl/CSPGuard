# CSPGuard
Web Data Extractor is a Python tool for analyzing web pages. It extracts domains and resources from CSP headers and JavaScript files, and organizes them into folders named after URLs. Outputs include text, JSON, and CSV files.

# Web Data Extractor

## Overview

Web Data Extractor is an advanced Python tool designed for analyzing web pages. It captures and processes various types of data from the web, including Content Security Policy (CSP) headers, JavaScript files, images, and iframes. The tool organizes the extracted data into folders named after the hostnames of the provided URLs and saves them in multiple formats such as text, JSON, and CSV.

## Features

- **CSP Header Analysis**: Extracts and processes domains and JavaScript URLs from CSP headers.
- **JavaScript Parsing**: Fetches and parses JavaScript files to detect domains.
- **Resource Detection**: Captures URLs of images and iframes.
- **Data Organization**: Creates folders for each URL and saves data in text files, JSON, and CSV formats.
- **Concurrent Processing**: Supports concurrent fetching and parsing of JavaScript files for efficient data extraction.

## Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.7 or higher
- [Playwright](https://playwright.dev/python/docs/intro)

### Installing Dependencies


1. **Clone the repository**:
    ```bash
    git clone https://github.com/M-thefl/CSPGuard.git
    cd CSPGuard
    pip install -r requirements.txt

2. **Install Playwright**:
   ```bash
   pip install playwright
   playwright install
   
3. **Install Required Python Packages**:
   ```bash
   pip install requests

## Usage 
To use Web Data Extractor, run the script with one or more URLs as arguments. The script will create folders based on the hostnames of the provided URLs and save the extracted data accordingly.
 <br /> 
**Command Line Usage**:
  ```py
python main.py <URL1> [<URL2> ... <URLN>]
```

**Example**:
  ```py
python main.py https://example.com https://another-example.com
```

## Output
**For each URL provided, the script will create a folder with the following structure**: <br /> 

├── hostname <br /> 
├── detected_domains.txt <br /> 
├── detected_domains.json <br /> 
├── detected_images.txt <br /> 
├── detected_iframes.txt <br /> 
└── detected_data.csv <br /> 

- detected_domains.txt: A list of detected domains.
- detected_domains.json: A JSON file containing detected domains.
- detected_images.txt: A list of detected image URLs.
- detected_iframes.txt: A list of detected iframe URLs.
- detected_data.csv: A CSV file with all detected data including domains, images, and iframes.


## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🖋 Contact
If you have any questions or suggestions, feel free to contact me at Mahbodfl1@gmail.com

``good luck (; 🌙``<br />
``for life``<br />
``fl``
🚀
