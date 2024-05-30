import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor


def download_image(img_url, folder_path):
    # Get file name from URL
    img_name = os.path.basename(img_url)

    if img_name.count("jpg") == 0:
        img_name += ".jpg"

    # Path for saving the image
    img_path = os.path.join(folder_path, img_name)

    # Download the image
    try:
        img_response = requests.get(img_url)
        if img_response.status_code == 200:
            with open(img_path, 'wb') as f:
                f.write(img_response.content)
            print(f"Downloaded: {img_name}")
        else:
            print(f"Failed to download {img_name}")
    except Exception as e:
        print(f"Error downloading {img_name}: {e}")


def download_images_from_site(url, folder_path, border):
    # Create a directory if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to access {url}")
        return

    # Parse HTML page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find <img> tags
    img_tags = soup.find_all('img')

    img_urls = []
    for index, img in enumerate(img_tags):
        if index < border:
            continue
        # Extract the URL from data-src or src attribute
        img_url = img.get('data-src') or img.get('src')
        img_url = urljoin(url, img_url)
        img_urls.append(img_url)

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(download_image, img_url, folder_path) for img_url in img_urls]
        for future in futures:
            future.result()
