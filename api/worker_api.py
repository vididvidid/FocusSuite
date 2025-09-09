import logging
import time
import requests
import json

class WorkerTextAPIManager:
    def __init__(self, logger):
        self.logger = logger

    def test_connection(self, api_url: str) -> bool:
        """
        Tests the connection to the worker endpoint by sending a simple POST request.
        """
        if not api_url or not api_url.startswith("http"):
            self.logger.warning(f"Invalid Worker API URL for testing: {api_url}")
            return False
        try:
            # The worker endpoint expects a POST request with a specific JSON payload.
            # We send a minimal payload to verify the connection is active and correctly configured.
            payload = {
                "system": "This is a connection test.",
                "user": "Ping"
            }
            headers = {'Content-Type': 'application/json'}

            # Use requests.post() to match the worker's expected method
            response = requests.post(api_url, headers=headers, json=payload, timeout=15)

            response.raise_for_status() 
            self.logger.info("Worker API connection successful.")
            return True
        except requests.RequestException as e:
            self.logger.error(f"Failed to connect to Worker API endpoint: {e}")
            return False
    
    def generate_with_retry(self, text_chunk: str, system_prompt: str, api_url: str, max_retries=3) -> dict | None:
        """
        Sends a chunk of OCR text to the worker endpoint for analysis
        and returns the parsed JSON response from the worker
        """

        if not api_url:
            self.logger.error("Worker API URL is not configured.")
            return None

        # The payload structure required by your workers.dev enpoint
        payload = {
            "system": system_prompt,
            "user": text_chunk
        }

        headers = {'Content-Type': 'application/json'}

        for attempt in range(max_retries):
            try:
                response = requests.post(api_url, headers = headers, json=payload, timeout=60)
                response.raise_for_status()

                data = response.json()
                # The worker returns a JSON object with a 'response' key containing the AI's text.
                response_str = data.get('response', '{}')

                try:
                    inner_data = json.loads(response_str)
                    return inner_data
                except json.JSONDecodeError:
                    self.logger.warning(f"Worker did not return valid inner JSON: {response_str}")
                    match = re.search(r'\{.*\}', response_str, re.DOTALL)
                    if match:
                        try:
                            return json.loads(match.group(0))
                        except json.JSONDecodeError:
                            pass
                        return None
                except requests.exceptions.RequestsException as e:
                    self.logger.warning(f"Worker API request failed (attempt {attempt + 1}/{max_retries}): {e}")
                    time.sleep(2**attempt) 
            except Exception as e:
                    self.logger.error(f"An unexpected error occurred during Worker API call (attempt { attempt + 1}):{e}")
                    time.sleep(2)

            self.logger.error("Worker API call failed after multiple retries")
            return None
