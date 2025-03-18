import unsplash_api
import database

def main():
    known_photos = database.get_all()
    known_ids = [photo['provider_id'] for photo in known_photos]
    collection = unsplash_api.get_collection_data()
    photo_ids, _ = unsplash_api.get_photo_ids(collection)
    unknown_ids = [id for id in photo_ids if id not in known_ids]
    
    for id in unknown_ids:
        database.create_photo(id)
    
    missing_data = [photo for photo in known_photos if not photo['photo_url']]
    api_limit = 3 # for now at least, ultimately we want 32?
    for _, photo in zip(range(api_limit), missing_data):
        print(photo)
        unsplash_data = unsplash_api.get_photo_data(photo['provider_id'])
        # TODO: 
        # * verify country with a list, assign ISO code
        # * make sure that coordinates exist (either GPT, or manual input)

        database.set_photo_data(photo['provider_id'], unsplash_data)

    eligible_photos = database.get_eligible()
    # TODO: 
    # * pick however many days is in the current/next month
    # * assign daily challenge days 
    # * save into json
    
if __name__ == '__main__':
    main()

