# Manages all intereactions with the OpenAI chat Completion API

import time
import openai
from openai import AuthenticationError, APIConnectionError

class OpenAIAPIManager:
    def __init__(self, logger):
        self.logger = logger
        self.client = None

    def configure(self, api_key: str) -> bool:
        # Configures the OpenAI client and verifies the API key
        if not api_key or not api_key.startswith("sk-"):
            self.logger.warning("OpenAI API key is missing or invalid.")
            self.client = None
            return False
        try:
            self.client = openai.OpenAI(api_key=api_key)
            self.client.models.list() # Testing the connection
            self.logger.info("OpenAI API client configured and connection successful.")
            return True
        except openai.AuthenticationError:
            self.logger.error("Authentication failed. The Provided OpenAI API key is invalid.")
            self.client = None
            return False
        except Exception as e:
            self.logger.error(f"Failed to configure OpenAI client: {e}")
            self.client = None
            return False

    def is_available(self) -> bool:
        # checks is the client is configured and ready.
        return self.client is not None
    
    def test_connection(self) -> bool :
        if not self.client:
            self.logger.warning("Cannot test connection, API client not configured.")
            return False
        try:
            self.client.models.list()
            self.logger.info("OpenAI API connection successful.")
            return True
        except AuthenticationError:
            self.logger.error("Authentication failed. The provided OpenAI API key is invalid.")
            return False
        except APIConnectionError as e:
            self.logger.error(f"Failed to connect to OpenAI API : {e}")
            return False
        except Exception as e:
            self.logger.error(f"An unexpected error occurred during API connection test: {e}")
            return False


    def generate_with_retry(self, prompt: str, max_retries=3) -> str | None:
        # Generate a response from teh AI, with retries for transient errors.
        if not self.is_available():
            self.logger.warning("OpenAI client is not available. Cannot generate content.")
            return None

        system_message = (
            "You are a productivity assistant. Your task is to analyze text from the user's screen"
            "and identify phrases that are distracting relative to a specific focus topic ."
            "You must respond ONLY with a valid JSON object containg a single key 'distractions' which is a list of strings. "
            "Example: {\"distractions\": [\"distracting phrase 1\", \"unrelated news headline\"}. "
            "If nothing is distracting, respond with {\"distractions\":[]}."
        )

        for attempt in range(max_retries):
            try:
                response= self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user","content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.2,
                    timeout=25
                )
                return response.choices[0].message.content
            except (openai.APITimeoutError, openai.APIConnectionError) as e:
                self.logger.warning(f"OpenAI API timeout/connection error (attempt {attempt+1}/{max_retries}):{e}")
                time.sleep(2 ** attempt)  # Exponential backoff

            except openai.APIStatusError as e:
                self.logger.error(f"OpenAI API status error: {e.status_code} - {e.response}")
                return None

            except Exception as e:
                self.logger.error(f"An unexpected error occured during API call (attempt {attempt + 1}): {e}")
                time.sleep(2)

            self.logger.error("OpenAI API call failed after multiple retries.")
            return None
