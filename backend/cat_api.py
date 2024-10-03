import requests
import os
from dotenv import load_dotenv

load_dotenv()

class CatAPI:
    def __init__(self):
        self.api_key = os.getenv('CAT_API_KEY')
        self.base_url = 'https://api.thecatapi.com/v1'

    def get_cats(self, breed=None, limit=1):
        headers = {'x-api-key': self.api_key}
        params = {'limit': limit}
        if breed:
            breed_id = self.get_breed_id(breed)
            if breed_id:
                params['breed_ids'] = breed_id

        try:
            response = requests.get(f'{self.base_url}/images/search', headers = headers, params = params)
            response.raise_for_status()
            cats = response.json()
            return cats
        except requests.exceptions.RequestException as e:
            return []
        
    def get_breed_id(self, breed_name):
        try:
            response = requests.get(f'{self.base_url}/breeds/search', headers={'x-api-key': self.api_key}, params={'q': breed_name})
            response.raise_for_status()
            breeds = response.json()
            if breeds:
                return breeds[0]['id']
            return None
        except requests.exceptions.RequestException as e:
            return None