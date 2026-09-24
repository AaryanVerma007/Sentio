import requests
import xml.etree.ElementTree as ET

def get_reddit_data_bypass(topic):
    print(f"Connecting to Reddit RSS to fetch real discussions about '{topic}'...")
    
    formatted_topic = topic.replace(" ", "+")
    url = f"https://www.reddit.com/r/all/search.rss?q={formatted_topic}&sort=new"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Failed to fetch data. Status Code: {response.status_code}")
            return
            
        root = ET.fromstring(response.content)
        namespace = {'atom': 'http://www.w3.org/2005/Atom'}
        
        extracted_posts = []
        for entry in root.findall('atom:entry', namespace):
            title_element = entry.find('atom:title', namespace)
            if title_element is not None and title_element.text:
                text = title_element.text.strip()
                
                # 🧹 DATA CLEANING FILTER: Ignore titles with less than 6 words
                if len(text.split()) >= 6:
                    extracted_posts.append(text)
                
        print(f"\n✅ Total Clean Reddit Posts Found: {len(extracted_posts)}")
        
        print("\n--- Top 5 Cleaned Reddit Posts ---")
        for i, text in enumerate(extracted_posts[:5]):
            print(f"{i+1}. {text}\n")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    get_reddit_data_bypass("samsung galaxy s26 ultra")  # Aap is topic ko change kar sakte ho, jaise "iPhone 16", "Elections", "Stock Market"