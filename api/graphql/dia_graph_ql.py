import requests
import json
import logging

def fetch_graphql_price(url ):
    query = """
    {
      GetFeed(
        Filter: "mair",
        BlockSizeSeconds: 480,
        BlockShiftSeconds: 480,
        StartTime: 1690535975,
        EndTime: 1693294891,
        FeedSelection: [
          {
            Address: "0xa3Fa99A148fA48D14Ed51d610c367C61876997F1",
            Blockchain: "Polygon",
            Exchangepairs: [],
          },
        ],
      )
      {
        Name
        Time
        Value
        Pools
        Pairs
      }
    }
    """

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "query": query
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    json_data = response.json()

    if response.status_code == 200:
        feed_data = json_data.get("data", {}).get("GetFeed", [])
        if feed_data:
            # Find the entry with the latest timestamp
            latest_entry = max(feed_data, key=lambda x: x["Time"])
            # Extract the latest price and timestamp
            latest_price = latest_entry["Value"]
            latest_timestamp = latest_entry["Time"]
            logging.info(f"dia_graph_ql:fetch_graphql_price--> latest price : {latest_price}, latest time stamp: {latest_timestamp}")
            return latest_price
        else:
            return None
    else:
        logging.error("Request failed with status code:", response.status_code)
        return None 
    
