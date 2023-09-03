# cryptoTokenPriceComparator

**Problem Statement:**

1. Establish a system to validate the authenticity of the MiMatic market price
2. Implement a real-time monitoring system to verify this accuracy on an ongoing basis

       (Also, Leverage external pricing data sources for comparative purposes (e.g. any price aggregator))

**Solution for Problem-1**:

There are two fold solutions I have tried to build to establish a system to validate the authenticity of the MiMatic market price

**Solution-A:** Built a small python and great-expectations based framework that does these tasks:

a) reads data from DIA API end-points

b) we define expectations from our data, this is configurable, say price range for MiMatic is defined between (0.5, 3.5)

c) if price from api end-point is not in the expected range, then it will fail the test and reported as failure, failed status can be reported in json or via the data-docs (HTML format)

d) expectations can be easily defined for the data quality for the other fields such as expected complete json-schema of api response (name, order and type of fields), uniqueness of timestamp and signature etc.

**Reason for choosing Solution-A:** Great-Expectations (GE) is a very popular data quality validation tool, this is the one of the first tool that introduced assertion-on-data similar to asserting-code done in popular unit and functional testing framework. Most of the functionalities in GE are open-source and users can use pre-existing expectations or build their own custom expectations and assert data at any stage (inception or computed). The main programming language supported by GE is python which is simple to use. 

**Solution-A Structure:** To keep it simple, I have kept API end-point and expectations in the main script (these can be separated in different modules to make the code modular). 
This runs automatically as part of github workflow -> great_expectation.yml(  whenever a commit occurs )

**Solution-B:** Built a Python script that does these tasks:

a) reads price data from DIA-Polygon, DIA-Fantom, CoinGecko and CoinMarketCap and compare the prices 

b) define threshold for flagging the deviation

c) report any price deviations using email and slack

**Reason for choosing Solution-B:** As solution1 mostly focused on data quality of individual feeds and APIs, solution2 takes care of comparing prices between the APIs or with external sources. I have tried a few things such as:

a) Tried using both REST APIs and GraphQL and finding a solution to fetch data from both of them

b) Used CoinGecko and CoinMarketCap as external price sources to use as baselined data

c) Also, used API for getting price from CoinGecko and for CoinMarketCap scraped the price from the website as typically on day to day basis, not every source offers APIs to pull data and wanted to play around with scraping for this task

**Solution-B Structure:** To keep it simple, I have kept API end-point and expectations in the main script (these can be separated in different modules to make the code modular). 

To run this script:

1. Clone this GitHub Repo to your local directory
2. If not already installed, Install Python version > 3.8
3. Create a virtual env using this python command: python -m venv c:\path\to\myenv
4. Activate above virtual env: \path\to\myenv\Scripts\activate
5. Install dependencies using this command (requirements.txt file below has complete dependencies for this project): pip install -r /path/to/requirements.txt requirements.txt
6. Run this command to execute source code: python src/api_data_quality_validation.py

**Solution for Problem-2**: 

To implement a real-time monitoring system to verify this accuracy on an ongoing basis, both the above solutions can be used using schedulers or CI/CD tooling.

1. Solution-A using Great-Expectations above can be run using a scheduler at a set regular-interval and script will assert data with pre-defined expectations. In the above solution, I have put the logic under “while True:” condition with time.sleep(120 secs) as APIs under test get their prices updated every 120 secs, so the script will be running the assertions on API data every 120 secs, any changes in data and deviation from expectations will be flagged.
2. For Solution-B, I have set-up CI/CD using Github Actions and is configured to run at regular intervals
