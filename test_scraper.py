from ntscraper import Nitter

# Initialize the Nitter scraper
scraper = Nitter()

topic = "iPhone" # Define the topic to search
target_tweets = 100

print(f"Fetching {target_tweets} tweets about '{topic}' from the internet. Please wait...")

# Start the scraping process
try:
    data = scraper.get_tweets(topic, mode='term', number=target_tweets)
    
    # Verify the exact number of tweets extracted
    extracted_tweets = data.get('tweets', [])
    total_found = len(extracted_tweets)
    
    print(f"\nTotal Tweets Found: {total_found}")
    
    # Display the first 3 tweets for a quick sanity check
    print("\n--- Top 3 Tweets for Sanity Check ---")
    for i, tweet in enumerate(extracted_tweets[:3]):
        print(f"{i+1}. {tweet['text']}\n")
        
except Exception as e:
    print(f"An error occurred during scraping: {e}")