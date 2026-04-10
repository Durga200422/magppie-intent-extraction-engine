import time
from src.extractor import extract_kitchen_intent

# The 4 test cases provided in the assessment [cite: 35, 36, 37, 38]
TEST_INPUTS = [
    "Straight kitchen, all white, under 1.5 lakh, need a chimney",
    "Something elegant, I don't know the layout, budget is flexible but not too high",
    "U-shape, dark wood finish, island counter, around 5 to 6 lakh",
    "Bana do kuch achha, budget 3 lakh, white color"
    # "I want a premium Italian marble finish but my budget is only 50,000 rupees.",
    # "I need a modular kitchen, budget is 2.5 Cr.",
    # "U-shape kitchen, white color, but absolutely no open shelving.",
    # "Actually, make it L-shape, wait no, U-shape is better."
]

def run_assessment():
    print("🚀 Starting Magppie Intent Extraction Assessment...\n")
    
    for i, user_input in enumerate(TEST_INPUTS, 1):
        print(f"--- Processing Input {i} ---")
        print(f"User Says: '{user_input}'")
        
        try:
            # Call our extraction pipeline
            result = extract_kitchen_intent(user_input)
            
            # Print the structured output nicely
            print(result.model_dump_json(indent=2))
            print(f"Confidence: {result.confidence}")
            print("-" * 30 + "\n")
            
            # Avoid hitting rate limits on the Gemini Free Tier
            time.sleep(5) 
            
        except Exception as e:
            print(f"❌ Error processing input {i}: {e}")

if __name__ == "__main__":
    run_assessment()