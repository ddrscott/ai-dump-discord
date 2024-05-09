from cachetools import TTLCache
import json
import os
import httpx

FIREBASE_WEB_API_KEY = os.getenv('FIREBASE_WEB_API_KEY')
REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')
DATATURD_API_URL = os.getenv('DATATURD_API_URL')

cache = TTLCache(maxsize=1, ttl=3500)

def fetch_id_token_with_refresh():
    if cache.get('id_token'):
        return cache['id_token']
    # Firebase API endpoint for exchanging a refresh token for an ID token
    refresh_api_url = 'https://securetoken.googleapis.com/v1/token'
    params = {
        'key': FIREBASE_WEB_API_KEY,
    }
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': REFRESH_TOKEN,
    }
    response = httpx.post(refresh_api_url, params=params, json=data)
    tokens = response.json()
    id_token = tokens.get('id_token')
    cache['id_token'] = id_token
    return id_token

async def generate(messages):
    # Example usage
    headers = {
        'Authorization': f'Bearer {fetch_id_token_with_refresh()}',
    }
    client = httpx.AsyncClient()
    async with client.stream('POST', DATATURD_API_URL, headers=headers, json=messages) as response:
        async for chunk in response.aiter_lines():
            if not chunk == '\n':
                line = json.loads(chunk)
                yield line

if __name__ == '__main__':
    for line in generate("How old is Tom Hanks multiplied by Tom Hollands age?"):
        print(line, end='')
