import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import json
import asyncio
import time
import logging
from datetime import datetime
import csv

# Load configuration from config file
def load_config():
    with open("config.json") as f:
        return json.load(f)

config = load_config()
interval = config["interval"]
proxy = config["proxy"]["https"]
output_format = config["output_format"]
logging.basicConfig(filename="scraping_log.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Function to save data to JSON or CSV
def save_data(data):
    if output_format == "json":
        with open("scraped_data.json", "w") as f:
            json.dump(data, f, indent=4)
    elif output_format == "csv":
        with open("scraped_data.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Protocols", "TVL"])
            for item in data:
                writer.writerow([item["name"], item["protocols"], item["tvl"]])

# Function to fetch data from the website
async def fetch_data():
    options = uc.ChromeOptions()
    #options.add_argument(f'--proxy-server={proxy}')
    
    try:
        # Initialize Chrome driver with options
        driver = uc.Chrome(options=options)
        driver.get("https://defillama.com/chains")
        
        # Parse page source
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        script_tag = soup.find("script", id="__NEXT_DATA__")
        json_data = json.loads(script_tag.string)

        products = json_data.get("props", {}).get("pageProps", {}).get("chainTvls", {})
        scraped_data = []

        for a in products:
            name = a.get('name')
            protocols = a.get('protocols')
            tvl = a.get('tvl')
            scraped_data.append({"name": name, "protocols": protocols, "tvl": tvl})

        save_data(scraped_data)
        logging.info(f"Data scraped successfully at {datetime.now()}")
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
    finally:
        driver.quit()

# Main function to run the scraper 
async def main():
    while True:
        await fetch_data()
        await asyncio.sleep(interval)

# Run the scraper
asyncio.run(main())
