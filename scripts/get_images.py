import os, random, calendar, datetime, json

import unsplash_api
import database

from location_utils import match_country, get_location_info

output_directory = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../public/challenge-lists')
)
api_limit = 30 # for now at least, ultimately we want 32?

def sync_photos():
    known_photos = database.get_all()
    known_ids = [photo['provider_id'] for photo in known_photos]
    print(f'pulling current collection content.')
    collection = unsplash_api.get_collection_data()
    photo_ids, _ = unsplash_api.get_photo_ids(collection)
    unknown_ids = [id for id in photo_ids if id not in known_ids]

    log = f'{len(unknown_ids)} photos not in database - inserting ids' if len(unknown_ids) > 0 \
        else 'no new photos to add'
    print(log)

    for id in unknown_ids:
        new_photo = database.create_photo(id)
        known_photos.append(new_photo)
    
    missing_data = [photo for photo in known_photos if not photo['photo_url']]
    print(f'{len(missing_data)} photos missing information')

    for _, photo in zip(range(api_limit), missing_data):
        unsplash_data = unsplash_api.get_photo_data(photo['provider_id'])
        original_country_name = unsplash_data['location_country']

        print(f'checking data for photo {unsplash_data["provider_id"]}:')
        missing_info = []
        if not unsplash_data['location_lat'] or not unsplash_data['location_lng']:
            missing_info.append('coordinates')
        if not original_country_name:
            missing_info.append('country')
        if not unsplash_data['location_name']:
            missing_info.append('location_name')
        
        if missing_info:
            print(f'\tmissing information: {", ".join(missing_info)}')
            if 'location_name' in missing_info or 'country' in missing_info:
                print(f'\tmanual input required. photo at: {unsplash_data["page_url"]}')
                if not unsplash_data['location_name']:
                    unsplash_data['location_name'] = input('\tlocation name: ')
                if not original_country_name:
                    original_country_name = input('\tcountry name: ')
            if 'coordinates' in missing_info:
                print(f'\tasking GPT for missing coordinates (location name: {unsplash_data["location_name"]})')
                coordinates = get_location_info(unsplash_data['location_name'])
                open_ai_response_approved = False
                latitude, longitude = 0.0, 0.0
                if coordinates:
                    latitude = coordinates['latitude']
                    longitude = coordinates['longitude']

                    print(f'\tsuggested coordinates: ({latitude}, {longitude})')
                    confirm = input('\ty to confirm, n to input manually: ')
                    open_ai_response_approved = confirm == 'y'
                
                if not open_ai_response_approved:
                    latitude = float(input('\tlatitude: '))
                    longitude = float(input('\tlongitude: '))

                unsplash_data['location_lat'] = latitude
                unsplash_data['location_lng'] = longitude

        else:
            print('\teverything OK!')

        matched_country_name, iso_code = match_country(original_country_name)

        while iso_code == 'ERR':
            print(f'\tmanual input required. could not match country {original_country_name}. photo at: {unsplash_data["page_url"]}')
            manual_country_name = input('\tcorrect country name: ')
            matched_country_name, iso_code = match_country(manual_country_name)

        if original_country_name in unsplash_data['location_name']:
            unsplash_data['location_name'] = unsplash_data['location_name'].replace(original_country_name, matched_country_name)
        else: 
            unsplash_data['location_name'] = ', '.join([unsplash_data['location_name'], matched_country_name])

        unsplash_data['country_code'] = iso_code
        unsplash_data['country_name'] = matched_country_name
        database.set_photo_data(photo['provider_id'], unsplash_data)

def generate_challenge_list():
    today = datetime.datetime.today()
    year, month = today.year, today.month

    existing_lists = os.listdir(output_directory)
    if existing_lists:
        last_existing_list = sorted(existing_lists, reverse=True)[0]
        last_existing_date = last_existing_list.split('.')[0].split('-')
        year, month = (int(last_existing_date[0]), int(last_existing_date[1])) 

    next_year, next_month = (year, month + 1) if month != 12 \
        else (year + 1, 1)
    # next_year, next_month = (year, month)
      
    days_in_month = calendar.monthrange(next_year, next_month)[1]

    eligible_photos = database.get_eligible()
    selections = list(random.sample(eligible_photos, k=min(days_in_month, len(eligible_photos))))

    daily_dict = {}
    for index, selection in zip(range(days_in_month), selections):
        daily_challenge_date = f'{next_year:04}-{next_month:02}-{(index+1):02}'
        daily_dict[daily_challenge_date] = selection
        selection['daily_challenge_date'] = daily_challenge_date
        database.set_photo_data(selection['provider_id'], selection)

    new_list_name = f'{next_year:04}-{next_month:02}.json'
    with open(os.path.join(output_directory, new_list_name), 'w') as output_file:
        json.dump(daily_dict, output_file, indent=4)

def main():
    sync_photos()
    # generate_challenge_list()

    
if __name__ == '__main__':
    main()
