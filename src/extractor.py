import os
import time
import json
from google import genai
from google.genai import types 
from groq import Groq
from langsmith import traceable
from dotenv import load_dotenv
from src.schema import KitchenIntent
from src.utils import clean_budget_value, save_to_history
from src.prompts import SYSTEM_INSTRUCTION_V1, SYSTEM_INSTRUCTION_V2_STRICT

load_dotenv()

# Client Initialization
gemini_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

@traceable
def extract_kitchen_intent(customer_input: str, provider: str = "Gemini", version: str = "v1") -> KitchenIntent:
    # 1. Basic Validation
    if not customer_input.strip():
        return KitchenIntent(confidence=0.0, ambiguities=["Empty input provided"])

    # 2. Security Layer (Edge Case 3)
    from src.utils import detect_injection_patterns
    if detect_injection_patterns(customer_input):
        # We fail fast without wasting API tokens
        return KitchenIntent(
            confidence=0.0,
            ambiguities=["Security Alert: Input flagged for non-standard instructions. Please describe your kitchen needs naturally."]
        )

    # 3. Routing Logic (Existing logic)
    active_prompt = SYSTEM_INSTRUCTION_V2_STRICT if version == "v2_strict" else SYSTEM_INSTRUCTION_V1
    
    if "Groq" in provider:
        return extract_with_groq(customer_input, active_prompt)
    return extract_with_gemini(customer_input, active_prompt)

@traceable
def extract_with_gemini(customer_input: str, system_prompt: str, retries: int = 2) -> KitchenIntent:
    """Primary extraction using Gemini 2.5 Flash with retry logic."""
    for attempt in range(retries):
        try:
            response = gemini_client.models.generate_content(
                model='gemini-2.5-flash', 
                contents=customer_input,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    response_mime_type='application/json',
                    response_schema=KitchenIntent,
                )
            )
            result = response.parsed
            
            # Post-processing
            result.budget_max = clean_budget_value(result.budget_max)
            
            # Issue 1 Fix: Decoupled history saving
            save_to_history(customer_input, result.model_dump(), provider="Gemini")
            return result
            
        except Exception as e:
            error_str = str(e)
            # Issue 2 Fix: Handle retryable vs non-retryable errors
            if ("503" in error_str or "429" in error_str) and attempt < retries - 1:
                time.sleep(5 * (attempt + 1))
                continue
            
            failure_obj = KitchenIntent(
                confidence=0.0,
                ambiguities=[f"Gemini API Error: {error_str[:100]}"]
            )
            save_to_history(customer_input, failure_obj.model_dump(), provider="Gemini-Error")
            return failure_obj
        
@traceable
def extract_with_groq(customer_input: str, system_prompt: str) -> KitchenIntent:
    """Fallback extraction using Llama-3.3 via Groq LPU."""
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt + " IMPORTANT: Output ONLY valid JSON."},
                {"role": "user", "content": customer_input}
            ],
            model="llama-3.3-70b-versatile", 
            response_format={"type": "json_object"}
        )
        
        raw_content = chat_completion.choices[0].message.content
        result = KitchenIntent.model_validate_json(raw_content)
        
        result.budget_max = clean_budget_value(result.budget_max)
        save_to_history(customer_input, result.model_dump(), provider="Groq")
        return result

    except Exception as e:
        failure_obj = KitchenIntent(
            confidence=0.0,
            ambiguities=[f"Groq API Error: {str(e)[:100]}"]
        )
        save_to_history(customer_input, failure_obj.model_dump(), provider="Groq-Error")
        return failure_obj