import re
import json
import os
from datetime import datetime
from typing import Optional, Dict, Any

# Configuration
HISTORY_FILE = "extraction_history.json"

def clean_budget_value(value) -> Optional[int]:
    """
    Standardizes budget extraction. Handles ranges (takes MAX) 
    and Hinglish unit conversion.
    """
    if value is None:
        return None
    if isinstance(value, int):
        return value

    try:
        val_str = str(value).lower().replace(',', '').replace('/-', '')
        
        # 1. Handle common unit patterns before extracting numbers
        # This prevents "50k to 1 lakh" from being miscalculated
        val_str = val_str.replace('lakh', '00000').replace('l ', '00000 ')
        val_str = val_str.replace('cr', '0000000').replace('crore', '0000000')
        val_str = val_str.replace('k', '000')

        # 2. Extract all numbers
        nums = re.findall(r"[-+]?\d*\.\d+|\d+", val_str)
        if not nums:
            return None

        # 3. Convert all found numbers to integers and return the MAX
        # This handles "2.5 to 3.5" -> [250000, 350000] -> 350000
        all_values = [int(float(n)) for n in nums]
        
        # Filter out accidental zero or tiny extractions
        valid_values = [v for v in all_values if v > 100] 
        
        return max(valid_values) if valid_values else None

    except (ValueError, TypeError, IndexError):
        return None

def detect_injection_patterns(text: str) -> bool:
    """
    Security Layer: Pre-filters common LLM jailbreak and prompt 
    injection patterns to protect system integrity.
    """
    suspicious_patterns = [
        r"ignore (all )?previous",
        r"you are now",
        r"forget (all )?instructions",
        r"reveal your (instructions|rules|prompt)",
        r"system (prompt|instruction)",
        r"set confidence to",
        r"tell me how to" # General safety guard
    ]
    
    text_lower = text.lower()
    for pattern in suspicious_patterns:
        if re.search(pattern, text_lower):
            return True
    return False

def normalize_text(text: str) -> str:
    """Cleans up voice-to-text artifacts and whitespace."""
    if not text:
        return ""
    text = text.strip()
    text = re.sub(r'[^\w\s\d,.?!-]', '', text)
    return text

def save_to_history(input_text: str, result_dict: Dict[str, Any], provider: str):
    """
    Saves extraction results to a local JSON file.
    Accepts a pre-serialized dictionary (result_dict) to avoid circular 
    dependencies with src.schema.
    """
    history_entry = {
        "timestamp": datetime.now().isoformat(),
        "input": input_text,
        "provider": provider,
        "output": result_dict  # Already serialized by caller via .model_dump()
    }
    
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []
            
    history.append(history_entry)
    
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def load_history():
    """Retrieves all past extractions for the UI dashboard."""
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []