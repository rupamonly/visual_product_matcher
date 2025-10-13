import time
import json
import uuid
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# --- Configuration ---
# Path setup (this is our robust version)
SERVER_DIR = Path(__file__).resolve().parent.parent
OUTPUT_FILE = SERVER_DIR / "data" / "products.json"

# Define all the categories and their URLs we want to scrape
CATEGORIES_TO_SCRAPE = {
     # Footwear
    "Men's Sneakers": "https://www.myntra.com/men-sneakers",
    "Men's Casual Shoes": "https://www.myntra.com/men-casual-shoes",
    "Women's Heels": "https://www.myntra.com/women-heels",
    "Women's Flats": "https://www.myntra.com/women-flats",
    
    # Apparel
    "Men's T-Shirts": "https://www.myntra.com/men-tshirts",
    "Men's Jeans": "https://www.myntra.com/men-jeans",
    "Women's Kurtas": "https://www.myntra.com/women-kurtas-suits",
    "Women's Tops": "https://www.myntra.com/women-tops",

    # Accessories
    "Watches": "https://www.myntra.com/watches",
    "Sunglasses": "https://www.myntra.com/sunglasses",
    "Women's Handbags": "https://www.myntra.com/women-handbags",
    "Backpacks": "https://www.myntra.com/backpacks",
    
    # Personal Care
    "Lipstick": "https://www.myntra.com/lipstick",
    "Perfume": "https://www.myntra.com/perfume",
    "Deodorant": "https://www.myntra.com/deodorant"
}

def scrape_category(driver, url, category_name):
    """Scrapes product data for a single category."""
    print(f"\n--- Scraping category: {category_name} from {url} ---")
    
    driver.get(url)
    print("Waiting for products to load...")
    try:
        # Wait for the main product container to show up
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "results-base"))
        )
        print("Products loaded.")
        time.sleep(5)  # Wait for images to lazy-load

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        product_list = soup.find_all('li', class_='product-base')
        
        if not product_list:
            print(f"No products found for {category_name}.")
            return []

        category_products = []
        print(f"Found {len(product_list)} products on the page.")

        for product in product_list:
            product_name_tag = product.find('h4', class_='product-product')
            product_name = product_name_tag.text.strip() if product_name_tag else 'N/A'
            
            image_tag = product.find('img', class_='img-responsive')
            image_url = image_tag['src'] if image_tag and 'src' in image_tag.attrs else 'N/A'

            if product_name != 'N/A' and image_url != 'N/A':
                product_data = {
                    "id": str(uuid.uuid4()),
                    "name": product_name,
                    "category": category_name,
                    "image_url": image_url
                }
                category_products.append(product_data)
        
        print(f"Successfully scraped {len(category_products)} products from {category_name}.")
        return category_products

    except Exception as e:
        print(f"An error occurred while scraping {category_name}: {e}")
        return []


# --- Main Scraper Execution ---
if __name__ == '__main__':
    # --- Selenium Setup ---
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    
    driver = webdriver.Chrome(service=service, options=options)
    
    all_products = []
    try:
        # Loop through each category and scrape it
        for category, url in CATEGORIES_TO_SCRAPE.items():
            products = scrape_category(driver, url, category)
            all_products.extend(products)
            time.sleep(2) # Be polite and wait a bit between requests

    finally:
        driver.quit() # Always close the browser

    print(f"\n--- Scraping complete. Total products scraped: {len(all_products)} ---")

    # Save all collected products to the JSON file
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(all_products, f, indent=4)
    
    print(f"All data saved successfully to {OUTPUT_FILE}")




# import time
# import json
# import uuid
# import os
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# from bs4 import BeautifulSoup
# from pathlib import Path


# SERVER_DIR=Path(__file__).resolve().parent.parent
# OUTPUT_FILE = SERVER_DIR/"data"/"products.json"


# # --- Configuration ---
# TARGET_URL = "https://www.myntra.com/men-sneakers"
# CATEGORY = "Men's Sneakers"

# def scrape_myntra():
#     """Scrapes product data from a Myntra category page using Selenium."""
#     print(f"Scraping category: {CATEGORY} from {TARGET_URL}")

#     # --- Selenium Setup ---
#     service = Service(ChromeDriverManager().install())
#     options = webdriver.ChromeOptions()
#     # options.add_argument('--headless')
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-dev-shm-usage')
#     options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    
#     driver = webdriver.Chrome(service=service, options=options)

#     # --- Scrape the Page ---
#     try:
#         driver.get(TARGET_URL)

#         print("Waiting for products to load...")
#         wait = WebDriverWait(driver, 20)
#         wait.until(EC.presence_of_element_located((By.CLASS_NAME, "results-base")))
#         print("Products loaded.")

#         time.sleep(5) 

#         page_source = driver.page_source
#         soup = BeautifulSoup(page_source, 'html.parser')
#         product_list = soup.find_all('li', class_='product-base')

#         if not product_list:
#             print("Could not find product list even with Selenium.")
#             return

#         scraped_products = []
#         print(f"Found {len(product_list)} products on the page.")

#         for product in product_list:
#             product_name_tag = product.find('h4', class_='product-product')
#             product_name = product_name_tag.text.strip() if product_name_tag else 'N/A'
            
#             image_tag = product.find('img', class_='img-responsive')
#             image_url = image_tag['src'] if image_tag and 'src' in image_tag.attrs else 'N/A'

#             if product_name != 'N/A' and image_url != 'N/A':
#                 product_data = {
#                     "id": str(uuid.uuid4()),
#                     "name": product_name,
#                     "category": CATEGORY,
#                     "image_url": image_url
#                 }
#                 scraped_products.append(product_data)

#         print(f"Successfully scraped {len(scraped_products)} products.")

#         # Ensure the output directory exists
#         os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

#         # Save the data to a JSON file (Only need this block ONCE)
#         with open(OUTPUT_FILE, 'w') as f:
#             json.dump(scraped_products, f, indent=4)

#         print(f"Data saved successfully to {OUTPUT_FILE}")

#     finally:
#         # Important: always close the browser
#         driver.quit()

# # --- Run the Scraper ---
# if __name__ == '__main__':
#     scrape_myntra()