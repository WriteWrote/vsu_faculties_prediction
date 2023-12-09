import requests

TOKEN = '23b3b4d823b3b4d823b3b4d8da23c88e21223b323b3b4d841b75f0d3f717ddc8e9c27cd'
TRY_COUNT = 5


def get_person_groups(person_url):
    try:
        user_id = scrape_person_id(person_url)
    except Exception:
        return []

    for try_number in range(TRY_COUNT):
        try:
            result = scrape_groups(user_id)
            if len(result) > 0:
                return result
        except Exception:
            pass

    return []


def scrape_person_id(person_url):
    s = person_url.split("https://vk.com/")[1]  # god forgive me for this mess
    if s.__contains__("id"):
        return s.split("id")[1].strip()
    else:
        response = requests.get('https://api.vk.com/method/utils.resolveScreenName', params={
            'access_token': TOKEN,
            'v': 5.103,
            'screen_name': s
        }).json()['response']
        return response['object_id']


def count_offset(user_id):
    response = requests.get('https://api.vk.com/method/users.getSubscriptions', params={
        'access_token': TOKEN,
        'v': 5.103,
        'sort': 'id_desc',
        'user_id': user_id,
        'extended': 1,
        'offset': 0,
        'fields': 'id'
    }).json()
    count = response['response']['count']
    return count // 20


def scrape_groups(user_id):
    groups_list = []
    offset = 0
    max_offset = count_offset(user_id)

    while offset <= max_offset:
        response = requests.get('https://api.vk.com/method/users.getSubscriptions', params={
            'access_token': TOKEN,
            'v': 5.103,
            'sort': 'id_desc',
            'user_id': user_id,
            'extended': 1,
            'offset': offset * 20,
            'fields': 'id'
        }).json()['response']

        offset += 1

        for item in response['items']:
            try:
                s = item['id'], item['name']
                groups_list.append(s)
            except KeyError:
                continue

    return groups_list
