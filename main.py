#mitmproxy --listen-port 8080
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import json
driver = uc.Chrome()

# Go to the URL
driver.get("https://defillama.com/chains")
html = driver.page_source
driver.close()
soup = BeautifulSoup(html, "html.parser")
script_tag = soup.find("script", id="__NEXT_DATA__")
json_data = json.loads(script_tag.string)

products = json_data.get("props", {}).get("pageProps", {}).get("chainTvls", {})
for a in products:
    name =  a['name']
    protocols =  a['protocols']
    tvl =  a['tvl']