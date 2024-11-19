import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from urllib.parse import urljoin, urlparse
from collections import deque
import time

# Define the base URL of the website's documentation
base_url = "https://docs.website.com/"  # Replace with the target website URL

# List of extensions to skip (e.g., images, scripts)
SKIP_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.webp', '.js', '.css')

# Function to check if a URL should be skipped
def should_skip_url(url):
    return any(url.lower().endswith(ext) for ext in SKIP_EXTENSIONS)

# Function to crawl and extract content iteratively
def crawl_site(base_url, unique_text_file):
    visited = set()
    queue = deque([base_url])  # Initialize the queue with the base URL

    with tqdm(total=1, desc="Crawling website documentation") as progress_bar:
        while queue:
            url = queue.popleft()  # Get the next URL from the queue
            if url in visited:
                continue
            visited.add(url)

            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise an error for bad status codes
            except requests.RequestException as e:
                print(f"Failed to fetch URL: {url}, Error: {e}")
                continue

            # Parse the page content with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Save the page content
            unique_text_file.write(f"\n--- {url} ---\n\n")
            page_text = soup.get_text()
            unique_text_file.write(page_text + "\n")
            print(f"Processed page: {url}")

            # Find and enqueue links on the page
            for link in soup.find_all('a', href=True):
                href = link['href']
                # Create a full URL from a relative URL
                full_url = urljoin(base_url, href)
                # Skip non-HTML content and external links
                if should_skip_url(full_url):
                    continue
                if urlparse(full_url).netloc == urlparse(base_url).netloc:
                    if full_url not in visited:
                        queue.append(full_url)
                        progress_bar.update(1)
            # Optional: Add a small delay to avoid overwhelming the server
            time.sleep(0.1)  # Adjust the delay as necessary

# Open a text file to save all content
with open("website_content.txt", "w", encoding="utf-8") as f:
    crawl_site(base_url, f)

print("All pages have been crawled and content has been saved.")