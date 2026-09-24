from apify_client import ApifyClient

# Initialize the ApifyClient with your API token
import os
# YAHAN APNI API KEY PASTE KAR 👇
client = ApifyClient(os.environ.get("APIFY_API_TOKEN", ""))

print("Connecting to Apify Cloud to fetch real tweets...")

# Prepare the input for the Twitter scraper actor (apidojo/tweet-scraper is very reliable)
run_input = {
    "searchTerms": ["iPhone"],
    "maxItems": 5,  # only 5 tweets for testing
    "sort": "Latest"
}

try:
    print("Scraping started on Cloud. This might take 15-30 seconds...")
    # Run the actor and wait for it to finish
    run = client.actor("apidojo/tweet-scraper").call(run_input=run_input)

    # Fetch and print results from the dataset
    print("\n--- Real Tweets Fetched ---")
    count = 1
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        text = item.get("text", "")
        if text:
            print(f"{count}. {text}\n")
            count += 1
            
    print("✅ Apify Cloud Test Successful!")

except Exception as e:
    print(f"An error occurred: {e}")