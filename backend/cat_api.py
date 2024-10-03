import requests
import os
from dotenv import load_dotenv

load_dotenv()

class CatAPI:
    def __init__(self):
        self.api_key = os.getenv('CAT_API_KEY')
        self.base_url = 'https://api.thecatapi.com/v1'
        self.headers = {'x-api-key': self.api_key}

    def get_cats(self, breed=None, limit=1):
        params = {'limit': limit}
        if breed:
            breed_id = self.get_breed_id(breed)
            if breed_id:
                params['breed_ids'] = breed_id

        try:
            response = requests.get(f'{self.base_url}/images/search', headers = self.headers, params = params)
            cats = response.json()
            return cats
        except requests.exceptions.RequestException as e:
            return []
        
    def get_breed_id(self, breed_name):
        try:
            response = requests.get(f'{self.base_url}/breeds/search', headers = self.headers, params = {'q': breed_name})
            breeds = response.json()
            if breeds:
                return breeds[0]['id']
            return None
        except requests.exceptions.RequestException as e:
            return None