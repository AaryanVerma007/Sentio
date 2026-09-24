import re

# A tiny list of major cities/countries for lightweight regex matching without loading a full NER model.
# In a real enterprise system, a local NER model (spaCy) or a comprehensive lookup DB is used.
MAJOR_LOCATIONS = [
    "New York", "London", "Paris", "Tokyo", "Berlin", "San Francisco", "Los Angeles",
    "Toronto", "Sydney", "Mumbai", "Dubai", "Singapore", "Hong Kong", "Chicago",
    "Seattle", "Austin", "Boston", "Amsterdam", "Madrid", "Rome", "Seoul",
    "USA", "UK", "Canada", "Australia", "India", "Germany", "France", "Japan", "China", "Brazil",
    "Europe", "Asia", "Africa", "South America", "North America", "Middle East"
]

# Compile regex for fast lookup
LOC_PATTERN = re.compile(r'\b(' + '|'.join(re.escape(loc) for loc in MAJOR_LOCATIONS) + r')\b', re.IGNORECASE)

def extract_location(text):
    """
    Attempts to extract a legitimate geographic location from the text.
    Never invents or guesses randomly.
    """
    if not text:
        return None
    
    match = LOC_PATTERN.search(text)
    if match:
        return match.group(1).title()
    
    return None
