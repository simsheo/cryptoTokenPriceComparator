**Problem Statement**

Establish a system to validate the authenticity of the MiMatic market price and implement a real-time monitoring system to verify this accuracy on an ongoing basis. Additionally, leverage external pricing data sources for comparative purposes (e.g., any price aggregator).

**Solution Overview**

**Solution-A**

       1. Framework to get prices from DIA-Polygon, DIA-Fantom, CoinGecko, and CoinMarketCap. 
       2. Demonstrated different ways to get price from different sources which includes  - API , GraphQL, DATA Scraping
       3. Deviation thresholds are defined and deviations are reported via email and slack.
   
**Solution-B: Great Expectations-based Data Quality Validation Framework**

       1. Great Expectations-based framework is used for data validation.
       2. Data is retrieved from DIA API endpoints.
       3. Expectations are defined for data quality, e.g. mandatory fields ,price range for MiMatic,column orders/expected values
       4. If data does not meet expectations, it's reported as a failure.
       5. Great Expectations is chosen for its powerful data quality validation capabilities.

**Solution-C:CRON job for real-time monitoring system to verify accuracy on an ongoing basis**

      1. The cron scheduler runs the job between 11:00 AM and 1:00 PM every 30mins, frequency and timing can be adjusted.
      2. When the job runs, it sends all fetched prices to Slack and email.
      3. If the price deviation exceeds the defined threshold, a breach report is sent.
      4. Separate Slack channels for price reports and threshold breach reports are recommended.
      
**Project Structure**

       1. a) api: get prices from DIA and coingecko using API endpoints.
              #API aren't always available to get price, so wanted to demonstrate how graphql and scraping could be used too
              a.i)  api/graphql: get price from DIA using graphql.
              a.ii) api/price_scraper:get price from coinmarketcap using data scraping. 
          b) config: Stores configuration files for URLs and token addresses.
          c) utils: Contains code for email, Slack integration, and price comparison.
          d) github workflows: Configuration files for GitHub Actions.
       2. great_expectations: Contains code for Solution-B, utilizing Great Expectations.

**Running the Project**

       GitHub Secrets-Add/Setup GitHub secrets for SLACK_TOKEN:for slack integration(sending messages on slack).
       GitHub Actions workflows (great_expectation.yml and price_validation_monitoring.yml) automate the project.
       Adjust scheduling parameters in price_validation_monitoring.yml as needed.

**Getting Started- Local Setup**

       Clone the repository: git clone https://github.com/simsheo/cryptoTokenPriceComparator.git
       1. cd cryptoTokenPriceComparator
       2. pip install -r requirements.txt
       3. run code using : python mimatic_token_monitoring.py
       4. run great expectation : python ge_unit_data_validation
             

**Reports from different solutions:**

Great expectation Reports: 
![image](https://github.com/simsheo/cryptoTokenPriceComparator/assets/91950874/a04d5621-40df-43ee-ba02-8977e6d156ee)
![image](https://github.com/simsheo/cryptoTokenPriceComparator/assets/91950874/b33828a4-031b-45c7-ba02-3dc22177cbbb)

Slack Notifications: 
![image](https://github.com/simsheo/cryptoTokenPriceComparator/assets/91950874/96047057-97ea-4bbe-a9df-62cac34a65ed)

Email Notifications:
![image](https://github.com/simsheo/cryptoTokenPriceComparator/assets/91950874/ebe047f4-eba5-4f13-b07f-7fb1e2e72003)
![image](https://github.com/simsheo/cryptoTokenPriceComparator/assets/91950874/44615d88-456d-48bb-a3ae-551e6e03fdc6)

