import requests
import xml.etree.ElementTree as ET

def get_live_news_data(topic, count=20):
    print(f"Connecting to Google News to fetch real headlines about '{topic}'...")
    
    # Google News RSS URL (100% Free, No API Keys needed!)
    # We replace spaces with '+' for the URL search query
    formatted_topic = topic.replace(" ", "+")
    url = f"https://news.google.com/rss/search?q={formatted_topic}&hl=en-US&gl=US&ceid=US:en"
    
    try:
        response = requests.get(url)
        
        if response.status_code != 200:
            print(f"Failed to fetch data. Status Code: {response.status_code}")
            return
            
        # Parse the XML response
        root = ET.fromstring(response.content)
        
        extracted_headlines = []
        # Find all 'item' tags which contain the news articles
        for item in root.findall('.//item'):
            title = item.find('title').text
            if title:
                extracted_headlines.append(title)
                
        print(f"\n✅ Total Real Headlines Found: {len(extracted_headlines)}")
        
        print("\n--- Top 3 Headlines for Sanity Check ---")
        for i, text in enumerate(extracted_headlines[:3]):
            print(f"{i+1}. {text}\n")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # You can change this topic to anything: "iPhone 16", "Elections", "Stock Market"
    get_live_news_data("iPhone 16")