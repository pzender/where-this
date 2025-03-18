import requests
import json

credentials = {}

with open('./credentials.json')  as credentials_file:
    credentials = json.load(credentials_file)

unsplash_client_id = credentials['unsplashClientID']
unsplash_collection_id = credentials['unsplashCollectionID']
unsplash_base_url = 'https://api.unsplash.com/'
items_per_page = 30
allowed_unsplash_requests = 50

def get_photo_ids(collection_data):
    photo_ids = []
    pages = 0
    while collection_data['total_photos'] > len(photo_ids) and pages < allowed_unsplash_requests / 2:
        photos_url = f'{unsplash_base_url}/collections/{unsplash_collection_id}/photos'
        collection_photos_request = requests.get(photos_url, 
                                         params={
                                             'page': pages + 1,
                                             'per_page': items_per_page,
                                         }, 
                                         headers=get_request_headers())
        if collection_photos_request.status_code != 200:
            print(f'Failed to pull collection photos! Status code: {collection_photos_request.status_code}') 
            return (photo_ids, pages)
        pages += 1
        photo_ids.extend([photo['id'] for photo in collection_photos_request.json()])
    return (photo_ids, pages)

def get_collection_data():
    collection_url = f'{unsplash_base_url}/collections/{unsplash_collection_id}'
    collection_request = requests.get(collection_url, headers=get_request_headers())
    if collection_request.status_code != 200:
        print(f'Failed to pull collection details! Status code: {collection_request.status_code}') 
        return {}
    return collection_request.json()

def get_photo_data(photo_id):
    photo_url = f'{unsplash_base_url}/photos/{photo_id}'
    photo_request = requests.get(photo_url, headers=get_request_headers())
    if photo_request.status_code != 200:
        print(f'Failed to pull photo details! Status code: {photo_request.status_code}')
        return {}
    return map_photo_response(photo_request.json())

def get_request_headers():
    return {
        'Authorization': f'Client-ID {unsplash_client_id}',
        'Accept-Version': 'v1',
    }

def map_photo_response(src_data):
    location = src_data['location']
    return {
        'provider_id': src_data['id'],
        'daily_challenge_date': None,
        'photo_url': src_data['urls']['raw'],
        'author_url': src_data['user']['links']['html'],
        'author_name': src_data['user']['name'],
        'location_name': location['name'] if 'name' in location else f'{location["city"]}, {location["country"]}',
        'location_country': location['country'],
        'location_lat': location['position']['latitude'],
        'location_lng': location['position']['longitude'],
        # may need description to help with matching?
    }