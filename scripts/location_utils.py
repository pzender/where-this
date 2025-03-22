import json, os
import openai

countries = []

with open(os.path.join(os.path.dirname(__file__), './country_dict.json'), encoding='utf-8')  as countries_file:
    countries_content = json.load(countries_file)
    countries = [
        {
            'name': country['name'],
            'iso_code': country['iso_code'],
            'alt_names': [name.lower() for name in country['alt_names']]
        } for country in countries_content
    ]

with open(os.path.join(os.path.dirname(__file__), './credentials.json'))  as credentials_file:
    credentials = json.load(credentials_file)
open_ai_api_key = credentials['openAIKey']

def match_country(src_name):
    matches = [country for country in countries if src_name.lower() in country['alt_names']]
    match = matches[0] if matches else {}
    if not match:
        return(src_name, 'ERR')
    return(match['name'], match['iso_code'])

def get_location_info(location_description):
    open_ai_client = openai.OpenAI(api_key = open_ai_api_key)
    response = open_ai_client.chat.completions.create(
        model = 'gpt-4o-mini',
        messages=[
            {'role': 'developer', 'content': 'In response to a location description, reply with GPS coordinates. Use a valid JSON object following the example format: \{\"latitude\": XXX, \"longitude\": YYY\}'},
            {'role': 'user', 'content': location_description}
        ]
    )
    coordinates = json.loads(response.choices[0].message.content)
    if 'latitude' not in coordinates or 'longitude' not in coordinates:
        print('\tGPT couldn\'t provide GPS coordinates')
        return None
    return coordinates