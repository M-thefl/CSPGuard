import asyncio
import re
import requests
import json
import csv
import logging
import os
from urllib.parse import urlparse
from playwright.async_api import async_playwright

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Function to extract domains from CSP headers
def extract_domains_from_csp(csp_header):
    domain_regex = re.compile(r'https?://[^\s/"\'<>]+')
    return set(domain_regex.findall(csp_header))

# Function to extract JavaScript URLs from CSP headers
def extract_js_urls_from_csp(csp_header):
    js_url_regex = re.compile(r'https?://[^\s/"\'<>]+\.js')
    return set(js_url_regex.findall(csp_header))

# Function to fetch and parse JavaScript for domains
def fetch_and_parse_js(url):
    try:
        logging.info(f"Fetching JS from: {url}")
        response = requests.get(url)
        response.raise_for_status()
        return parse_domains(response.text)
    except requests.RequestException as e:
        logging.error(f"Failed to fetch JS from {url}: {e}")
        return set()

# Function to parse domains from JavaScript code
def parse_domains(js_code):
    domain_regex = re.compile(r'https?://[^\s/"\'<>]+')
    return set(domain_regex.findall(js_code))

# Function to create a folder for each URL and save data
def create_folder_and_save_data(url, domains, images, iframes):
    # Create a folder named after the URL's hostname
    hostname = urlparse(url).hostname
    folder_name = hostname if hostname else 'unknown'
    
    # Sanitize folder name (remove invalid characters)
    folder_name = re.sub(r'[<>:"/\\|?*]', '', folder_name)
    
    os.makedirs(folder_name, exist_ok=True)
    
    # Save domains to a file
    if domains:
        with open(os.path.join(folder_name, 'detected_domains.txt'), 'w') as file:
            for domain in domains:
                file.write(f"{domain}\n")
        logging.info(f"Domains saved to {folder_name}/detected_domains.txt")
        
        with open(os.path.join(folder_name, 'detected_domains.json'), 'w') as file:
            json.dump(list(domains), file, indent=4)
        logging.info(f"Domains saved to {folder_name}/detected_domains.json")

    # Save images to a file
    if images:
        with open(os.path.join(folder_name, 'detected_images.txt'), 'w') as file:
            for image in images:
                file.write(f"{image}\n")
        logging.info(f"Images saved to {folder_name}/detected_images.txt")

    # Save iframes to a file
    if iframes:
        with open(os.path.join(folder_name, 'detected_iframes.txt'), 'w') as file:
            for iframe in iframes:
                file.write(f"{iframe}\n")
        logging.info(f"Iframes saved to {folder_name}/detected_iframes.txt")

    # Save all data to a CSV file
    with open(os.path.join(folder_name, 'detected_data.csv'), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Type', 'URL'])
        for domain in domains:
            writer.writerow(['Domain', domain])
        for image in images:
            writer.writerow(['Image', image])
        for iframe in iframes:
            writer.writerow(['Iframe', iframe])
    logging.info(f"All data saved to {folder_name}/detected_data.csv")

# Main function that uses Playwright to navigate and extract data
async def main(*urls):
    async with async_playwright() as p:
        # Launch headless browser
        logging.info("Launching headless browser...")
        browser = await p.chromium.launch(headless=True)
        tasks = []

        for target_url in urls:
            tasks.append(analyze_url(browser, target_url))

        await asyncio.gather(*tasks)
        await browser.close()

# Analyze a single URL
async def analyze_url(browser, target_url):
    page = await browser.new_page()

    script_urls = set()
    csp_headers = set()
    image_urls = set()
    iframe_urls = set()

    # Intercept requests to capture script, image, and iframe URLs
    async def on_request(request):
        if request.resource_type == "script":
            script_urls.add(request.url)
        elif request.resource_type == "image":
            image_urls.add(request.url)
        elif request.resource_type == "iframe":
            iframe_urls.add(request.url)

    # Intercept responses to capture CSP headers
    async def on_response(response):
        csp = response.headers.get("content-security-policy", "")
        if csp:
            csp_headers.add(csp)

    page.on("request", on_request)
    page.on("response", on_response)

    # Navigate to the target URL
    logging.info(f"Navigating to {target_url}...")
    await page.goto(target_url)
    await page.wait_for_timeout(3000)  # Wait for the page to load

    domains = set()

    # Process CSP headers to extract domains and JavaScript URLs
    for csp_header in csp_headers:
        domains.update(extract_domains_from_csp(csp_header))
        script_urls.update(extract_js_urls_from_csp(csp_header))

    # Fetch and parse JavaScript files concurrently for domains
    js_fetch_tasks = [asyncio.to_thread(fetch_and_parse_js, url) for url in script_urls]
    results = await asyncio.gather(*js_fetch_tasks)

    for result in results:
        domains.update(result)

    # Save results to a folder
    create_folder_and_save_data(target_url, domains, image_urls, iframe_urls)

    # Print all unique domains detected
    logging.info("\nDetected the following domains from CSP and Referenced JS:")
    for domain in domains:
        print(domain)

    # Optionally, you can print image and iframe URLs as well
    logging.info("\nDetected image URLs:")
    for url in image_urls:
        print(url)

    logging.info("\nDetected iframe URLs:")
    for url in iframe_urls:
        print(url)

    await page.close()

# Run the main function
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        logging.error(f"Usage: {sys.argv[0]} <URL1> [<URL2> ... <URLN>]")
        sys.exit(1)
    
    urls = sys.argv[1:]
    asyncio.run(main(*urls))