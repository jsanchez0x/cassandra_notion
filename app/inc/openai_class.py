# -*- coding: UTF-8 -*-

import inc
import requests
import json

class OpenAI:

    def compose_basic_header_request(self) -> dict:
        # Generates a dictionary with the basic headers to make a request to the API.

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer " +  inc.cfg.openai_api_key
        }

        return headers


    def get_model_response(self, prompt: str) -> str:
        # Make a request to OpenAI using the Davinci model.
        # The response given by the model for the indicated prompt is returned.
        # Information for Completions API: https://beta.openai.com/docs/api-reference/completions

        url = "https://api.openai.com/v1/completions"
        payload = {
            "model": "text-davinci-003",
            "prompt": prompt,
            "suffix": "Cassandra: ",
            "max_tokens": 100,
            "temperature": 0.4,
            "n": 1,
            "frequency_penalty": 1,
            "best_of": 1,
        }
        model_response = requests.post(url, json=payload, headers=self.compose_basic_header_request())
        model_response_data = json.loads(model_response.text)

        try:
            cleaned_response = self.clean_model_response(model_response_data['choices'][0]['text'])

            return cleaned_response
        except KeyError:
            return "ERROR: The response received by the OpenAI API is not as expected."


    def clean_model_response(self, response: str) -> str:
        # Process Davinci's response to clean it up.

        # Remove the two new lines at the beginning.
        response = response.removeprefix("\n\n")

        return response
