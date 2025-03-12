import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def print_webpage(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Failed to retrieve the webpage")
        return

    print(response.text)


def download_images(url, folder="images"):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Failed to retrieve the webpage")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    img_tags = soup.find_all("img")

    if not os.path.exists(folder):
        os.makedirs(folder)

    for img in img_tags:
        img_url = img.get("src")
        if img_url:
            img_url = urljoin(url, img_url)
            try:
                img_data = requests.get(img_url, headers=headers).content
                img_name = os.path.join(folder, os.path.basename(img_url))
                with open(img_name, "wb") as img_file:
                    img_file.write(img_data)
                print(f"Downloaded: {img_name}")
            except Exception as e:
                print(f"Failed to download {img_url}: {e}")


if __name__ == "__main__":
    website_url = "https://bluearchive-cn.com/"
    print_webpage(website_url)
    download_images(website_url)