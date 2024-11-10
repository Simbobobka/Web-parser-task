# Web Scraping test task

### Table of content
- [About](#about)
    - [Key features](#key-features)
        1. Periodic Data Collection
        2. Proxy Support
        3. Data Persistence and Structure
        4. Error Handling and Logging
- [Quick start](#quick-start)
- [Project setup](#project-setup)
    - [Configuration details](#configuration)
- [Run script](#run-script)
- [Example of output](#output-example)
- [Project stack](#project-stack)
- [Contact information](#contact-information)



### About
This project is a robust web scraper designed to gather data from DeFi Llama’s chain information page, https://defillama.com/chains. This data, which includes protocol names, TVL, and other key metrics, is collected and stored locally for analysis. Designed with flexibility and reliability in mind, the scraper can be customized to meet various data collection needs.

#### Key Features

__Periodic Data Collection__

The scraper runs at configurable intervals (default: every 5 minutes), allowing continuous data collection without manual intervention. This interval is easily adjustable through a configuration file to suit different data refresh requirements.

__Proxy Support__

To enhance anonymity and avoid request blocks, the scraper supports the use of proxies. The proxy server can be configured directly from a settings file, allowing dynamic adjustments based on network or privacy requirements.

__Data Persistence and Structure__

Each data fetch is saved as an entry in a __JSON/CSV__ file, maintaining a structured format that includes:

- __Timestamp__: The time when the data was retrieved.
- __Record Count__: The number of records retrieved.
- __Status__: Indicates whether the fetch was successful or encountered an issue.
- __Scraped Data__: The actual records retrieved from the website.
This format allows for easy tracking of data over time, supports debugging, and provides context for each entry.

__Error Handling and Logging__

The project is equipped with detailed logging for tracking its actions, including:

- __Connection Errors__: Logs issues related to connectivity and request failures.
- __Proxy Issues__: Logs proxy connection errors or unresponsive proxies.
- __Scraping Status__: Tracks each scraping attempt, recording successes and failures along with relevant metadata.

### Quick start
Install all dependencies from  ```requirements.txt``` using command: 

```bash
pip install -r requirements.txt
```

Execute ```python main.py``` to run script.

### Project setup
1. __Clone the Repository__

```bash
git clone <repository-url>
cd <repository-folder>
```

2. __Install Dependencies__

This project uses `venv` for managing dependencies. Follow these steps to install set up the project.

Create and activate a virtual environment with ```venv``` or ```pipenv``` for dependency management, and then install all requirements:

```bash
python -m venv .venv
source .venv/scripts/activate
pip install -r requirements.txt
```

After this, all required libraries would be installed.

> Using a virtual environment (venv or pipenv) is recommended to manage dependencies and avoid conflicts. Make sure to activate your environment before running the above commands.

#### Configuration

In the ```config.json``` file are specifed settings for parser. There you could change intervals of execution, proxy servers and output format.

```JSON
{
    "interval": 300, 
    "proxy": {
        "http": "",
        "https": ""
    },
    "output_format":"json"
}
```

Parameters:
- __interval__ - define intervals between execution(__in seconds__)
- __proxy__ - define proxy server in correct format in empty spaces: 
    - https://<i></i>your-proxy-ip:port
    - http://<i></i>your-proxy-ip:port
    > Script could also work without proxy. Just leave fields blank as in the example.
- __output_format__ - define type of output data to be saved to(only __json/csv__ options available)

#### Run script
To perform execution simply run ```main.py``` as python file

```bash
python main.py
```

To stop script use ```ctrl + C```.

#### Output example

In this repository are attached ```scraped_data.json``` and ```scraping_log.log``` files. 

The ```scraped_data.json``` stores scraped data and information about process:
```json
[
    {
        "timestamp": "2024-11-09T22:30:29.835987",
        "object_count": 323,
        "status": "success",
        "data": [
            {
                "name": "Ethereum",
                "protocols": 1213,
                "tvl": 119477878040.23448
            },
            {
                "name": "Solana",
                "protocols": 174,
                "tvl": 14693392458.668772
            }
            ...
```

This project includes ```logging``` to track the scraping process and monitor script performance. Key activities such as data __retrieval__, __parsing success__, __errors__, and the __interval between executions__ are logged. This provides insight into the script's operations, making it easier to debug issues and verify successful data collection.

Each log entry includes:

- Timestamp of the action
- Status of the scraping attempt (success/failure)
- Any errors encountered
- Summary details, such as the number of items parsed

Example of ```scraping_log.log``` file:

```log
2024-11-09 22:30:25,617 - INFO - patching driver executable C:\Users\tomas\appdata\roaming\undetected_chromedriver\undetected_chromedriver.exe
2024-11-09 22:30:29,840 - INFO - Data scraped successfully - Time: 2024-11-09 22:30:29.840991, Count: 323, Status: Success
2024-11-09 22:30:37,568 - INFO - Script terminated by user.
2024-11-09 22:30:37,569 - INFO - Script exited.
```

### Project stack
- asyncio
- csv
- json
- BeautifulSoup4
- undetected-chromedriver
- logging
- signal

#### Contact information

- Phone: 093 489 3704
- email: tomashuk.oleg2005@gmail.com
- Telegram: @Simbobobka
