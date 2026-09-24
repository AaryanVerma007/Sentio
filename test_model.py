import torch
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
import warnings

# T4 GPU ya naye environment ke chhote-mote warnings hide karne ke liye
warnings.filterwarnings('ignore')

# 1. Local folder se model aur tokenizer ko load karna
model_path = "./sentiment_model"  
print("🧠 Loading Local AI Model... (isme kuch seconds lag sakte hain)")

tokenizer = DistilBertTokenizerFast.from_pretrained(model_path)
model = DistilBertForSequenceClassification.from_pretrained(model_path)

# 2. Test karne ke liye kuch tricky sentences
test_sentences = [
    "I absolutely love the new design, it's fantastic!",
    "My laptop crashed again, this is the worst experience ever.",
    "The food was okay, nothing too special but not bad.",
    "This app is sickk af 🔥", # Checking slang
]

# 3. Model se prediction karwana
print("\n--- 🚀 AI Predictions ---")
for text in test_sentences:
    # Text ko numbers (tensors) mein convert karna
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
    
    # Model se prediction lena bina gradient calculate kiye (saves memory)
    with torch.no_grad():
        outputs = model(**inputs)
        
    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=1).item()
    
    # 0 = Negative, 1 = Positive
    sentiment = "Positive 😃" if predicted_class == 1 else "Negative 😡"
    
    print(f"Text: '{text}'")
    print(f"Sentiment: {sentiment}\n")
    print("-" * 30)