import os
import requests
import logging

class VisionAPIManager:
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.api_url = 'https://qa-pic.lizziepika.workers.dev/analyze-image'

    def get_image_description(self, image_path:str, prompt:str) -> str:
        if not os.path.exists(image_path):
            self.logger.error(f"Image file not found at : {image_path}")
            return 'error: file not found'

        try:
            with open(image_path, 'rb') as image_file:
                files = {
                    'image': (os.path.basename(image_path), image_file, 'image/jpeg'),
                    'text':(None, prompt),
                }
                headers = {
                    'accept':'*/*',
                }

                response = requests.post(self.api_url, headers = headers,
                                         files=files, timeout = 30)


                if response.status_code == 200:
                    try:
                        data = response.json()
                        description = data.get('response','')
                        self.logger.info(f"API response for {os.path.basename(image_path)}:'{description}'")
                        return description.strip().lower()
                    except requests.exceptions.JSONDecodeError:
                        self.logger.warning(f"Failed to decode JSON from response for {image_path}. Response text: {response.text}")
                        return 'error:invalid json response'
                else:
                    self.logger.error(f"API request for {image_path} failed with status code: {response.status_code} ")
                    return f'error: http {response.status_code}'
        except requests.RequestException as e:
            self.logger.error(f"An exception occurred during API request for {image_path}:{e}")
            return f"error:{e}"
        except Exception as e:
            self.logger.error(f"An unexpected error occurred in get_image_description for {image_path} : {e} ")
            return "error: unexpected"
