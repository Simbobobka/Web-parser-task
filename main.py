import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from datetime import datetime
import json
import asyncio
import signal
import sys
import logging
import csv

def load_config():
    with open("config.json") as f:
        return json.load(f)

def signal_handler(sig, frame):
    logging.info("Script terminated by user.")
    print("\nScript terminated gracefully.")
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

config = load_config()
interval = config["interval"] # time when parser make request (in seconds)
proxy = config["proxy"]["https"] # proxy server setup
output_format = config["output_format"] # choose format to save parsed data
logging.basicConfig(filename="scraping_log.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def save_data(data):
    timestamp = datetime.now().isoformat()
    object_count = len(data)
    status = "success" if data else "failed"
    save_info = {
        "timestamp": timestamp,
        "object_count": object_count,
        "status": status,
        "data": data
    }
    
    if output_format == "json":
        try:
            with open("scraped_data.json", "r") as f:
                existing_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = []

        existing_data.append(save_info)

        with open("scraped_data.json", "w") as f:
            json.dump(existing_data, f, indent=4)

    elif output_format == "csv":
        with open("scraped_data.csv", "a", newline="") as f:
            writer = csv.writer(f)
            if f.tell() == 0:  
                writer.writerow(["Timestamp", "Object Count", "Status", "Name", "Protocols", "TVL"])
            for item in data:
                writer.writerow([timestamp, object_count, status, item["name"], item["protocols"], item["tvl"]])

# Function to fetch data from the website
async def fetch_data():
    options = uc.ChromeOptions()
    if proxy:
        options.add_argument(f'--proxy-server={proxy}')
    
    try:
        driver = uc.Chrome(options=options)
        driver.get("https://defillama.com/chains")
        
        # Parse page source
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        script_tag = soup.find("script", id="__NEXT_DATA__")
        json_data = json.loads(script_tag.string)

        products = json_data.get("props", {}).get("pageProps", {}).get("chainTvls", [])
        scraped_data = []

        for a in products:
            name = a.get("name")
            protocols = a.get("protocols")
            tvl = a.get("tvl")
            scraped_data.append({"name": name, "protocols": protocols, "tvl": tvl})
        
        save_data(scraped_data)
        logging.info(f"Data scraped successfully - Time: {datetime.now()}, Count: {len(scraped_data)}, Status: Success")
        print(f"Data scraped successfully - Time: {datetime.now()}, Count: {len(scraped_data)}, Status: Success")
        
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        print(f"Error fetching data: {e}")
        save_data([])
        
    finally:
        driver.quit()

async def main():
    while True:
        await fetch_data()
        await asyncio.sleep(interval)

try:
    asyncio.run(main())
except Exception as e:
    logging.error(f"Script terminated unexpectedly: {e}")
    print(f"Script terminated unexpectedly: {e}")
finally:
    logging.info("Script exited.")
    print("Script exited.")