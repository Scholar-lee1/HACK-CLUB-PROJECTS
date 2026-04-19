import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

class OpenRouterService:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        # Using Gemini 2.0 Flash via OpenRouter (Standard for 2026)
        self.model = "google/gemini-2.0-flash-001"

    def get_simulation(self, action):
        prompt = f"""
        Act as the 'Future Me Judge'. 
        The user choice: "{action}"
        Predict 3 futures. Return ONLY a valid JSON object.
        {{
            "best_case": "...",
            "worst_case": "...",
            "unexpected": "..."
        }}
        """

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "response_format": { "type": "json_object" }
        }

        try:
            response = requests.post(self.url, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            
            result = response.json()
            # OpenRouter follows the OpenAI format
            content = result['choices'][0]['message']['content']
            
            return json.loads(content)

        except Exception as e:
            print(f"--- OPENROUTER ERROR: {e} ---")
            return {
                "best_case": "The Judge is currently offline.",
                "worst_case": f"Connection Error: {str(e)[:40]}",
                "unexpected": "Try refreshing the page or checking your API key."
            }