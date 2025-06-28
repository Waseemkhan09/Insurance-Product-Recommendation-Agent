import os
import json
from dotenv import load_dotenv
import google.generativeai as genai 
import requests

# Loading environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

class LLMService:
    def __init__(self, model_name="gemini-2.0-flash"):
        self.model_name = os.getenv("MODEL_NAME")
        self.api_key = os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable not set. "
                "Please get a Google Gemini API key from Google AI Studio and add it to your .env file."
            )

        try:
            print(f"Google Generative AI model name set to: {self.model_name}")
        except Exception as e:
            raise RuntimeError(
                f"Failed to configure Google Generative AI: {e}. "
                "Ensure the model name is correct and API key is valid."
            )

    def _call_llm_api(self, prompt: str) -> str:
        """
        Calls the Google Gemini API for text generation using requests.
        """
        try:
            api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}"

            chat_history = []
            chat_history.append({ "role": "user", "parts": [{ "text": prompt }] })
            payload = { "contents": chat_history }

            response = requests.post(
                api_url,
                headers={ 'Content-Type': 'application/json' },
                data=json.dumps(payload)
            )
            response.raise_for_status() 
            result = response.json()

            if result.get("candidates") and len(result["candidates"]) > 0 and \
               result["candidates"][0].get("content") and \
               result["candidates"][0]["content"].get("parts") and \
               len(result["candidates"][0]["content"]["parts"]) > 0:
                return result["candidates"][0]["content"]["parts"][0]["text"]
            else:
                # Providing more specific error info if content parts are missing or blocked by safety
                error_detail = result.get("promptFeedback", {}).get("blockReason") or \
                               result.get("candidates", [{}])[0].get("finishReason") or \
                               result.get("candidates", [{}])[0].get("safetyRatings") or \
                               json.dumps(result, indent=2) 
                raise RuntimeError(f"Unexpected Gemini API response structure or no content: {error_detail}")

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Gemini API request failed: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to get response from LLM (Gemini): {e}")

    def generate_recommendation(self, user_answers: dict, insurance_products: list) -> str:
        """
        Generates insurance product recommendations based on user answers and product data.
        Leverages the LLM to process user answers and formulate a personalized recommendation.
        """
        # Step 1: User answers
        user_summary_prompt = f"""
        Given the following user information, summarize their situation and identify their most probable insurance needs.
        User Information: {json.dumps(user_answers, indent=2)}

        Focus on aspects like:
        - Age (e.g., young, middle-aged, retired)
        - Dependents (e.g., single, family with kids)
        - Income/Assets (e.g., high earner, significant assets to protect)
        - Health status (e.g., generally healthy, pre-existing conditions)
        - Travel frequency (e.g., frequent international traveler)
        - Budget for premiums

        Provide a concise summary of their likely insurance priorities.
        Example: "This user is a middle-aged individual with dependents, a good income, and a house. Their priorities likely include protecting their family's financial future, their health, and their assets."
        """
        user_profile_summary = self._call_llm_api(user_summary_prompt)

        # Step 2: recommendation prompt 
        product_data_str = json.dumps(insurance_products, indent=2)

        recommendation_prompt = f"""
        Based on the following user profile and available insurance products, recommend the most suitable product(s) for the user.
        Explain why each recommended product fits their needs. If multiple products are suitable, mention them all.
        If no products are a perfect fit, suggest the closest options and mention what might be missing.

        User Profile Summary:
        {user_profile_summary}

        Available Insurance Products:
        {product_data_str}

        Please consider the following criteria for recommendations:
        - **Life Insurance:** High priority if user has dependents and a stable income.
        - **Health Insurance:** Important for all, but tailor recommendations based on health status and income/budget.
        - **Auto Insurance:** Relevant if user has a car (implied by assets).
        - **Homeowner's/Property Insurance:** Relevant if user owns a house or significant assets.
        - **Travel Insurance:** High priority if user travels frequently internationally.
        - **Investment-linked Insurance:** For users with higher income and desire for wealth growth.

        Format your response clearly, starting with "Here are the insurance product(s) recommended for you:"
        Then, for each product, provide:
        - **Product Name:**
        - **Description:** (brief, from product data)
        - **Why it's suitable:** (based on user profile)
        """
        return self._call_llm_api(recommendation_prompt)

