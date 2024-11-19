import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from urllib.parse import urljoin, urlparse

# Define the base URL of the website's documentation
base_url = "https://docs.website.com/"  # Replace with the target website URL

# List of extensions to skip (e.g., images, scripts)
SKIP_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.webp', '.js', '.css')

# Function to crawl and extract content recursively
def crawl_page(url, visited, unique_text_file, progress_bar):
    if url in visited:
        return
    visited.add(url)

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
    except requests.RequestException as e:
        print(f"Failed to fetch URL: {url}, Error: {e}")
        return

    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Save the page content
    unique_text_file.write(f"\n--- {url} ---\n\n")
    page_text = soup.get_text()
    unique_text_file.write(page_text + "\n")
    print(f"Processed page: {url}")

    # Find and process links on the page
    for link in soup.find_all('a', href=True):
        href = link['href']
        # Create a full URL from a relative URL
        full_url = urljoin(base_url, href)
        # Skip non-HTML content
        if any(full_url.lower().endswith(ext) for ext in SKIP_EXTENSIONS):
            continue
        # Only crawl links within the same domain
        if urlparse(full_url).netloc == urlparse(base_url).netloc:
            progress_bar.update(1)
            crawl_page(full_url, visited, unique_text_file, progress_bar)

# Open a text file to save all content and initialize progress bar
with open("website_content.txt", "w", encoding="utf-8") as f:
    visited_urls = set()
    with tqdm(total=1, desc="Crawling website documentation") as progress_bar:
        crawl_page(base_url, visited_urls, f, progress_bar)

print("All pages have been crawled and content has been saved.")