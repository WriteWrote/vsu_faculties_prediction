import requests
import time

token = '23b3b4d823b3b4d823b3b4d8da23c88e21223b323b3b4d841b75f0d3f717ddc8e9c27cd'


def get_person_groups(person_url):
    result = []
    try:
        user_id = scrape_id(person_url)
        result = scrape_groups(user_id)
    except Exception:
        print(Exception)

    return result


def scrape_id(person_url):
    # typical vk.com urls:
    # https://vk.com/captainofwardrobe
    # or
    # https://vk.com/id219869843

    # removing https + vk.com:
    s = person_url.split("https://vk.com/")[1]  # god forgive me for this mess

    id = ""
    if s.__contains__("id"):
        id = s.split("id")[1].strip()
    else:
        response = requests.get('https://api.vk.com/method/utils.resolveScreenName', params={
            'access_token': token,
            'v': 5.103,
            # 'type': 'user',
            # 'object_id': s,
            'screen_name': s
        }).json()['response']

        id = response['object_id']

    return id


def count_offset(user_id):
    response = requests.get('https://api.vk.com/method/users.getSubscriptions', params={
        'access_token': token,
        'v': 5.103,
        'sort': 'id_desc',
        'user_id': user_id,
        'extended': 1,
        'offset': 0,
        'fields': 'id'
    }).json()
    #['response']['count']
    count = response['response']['count']
    return count // 20


def scrape_groups(user_id):
    groups_list = []

    offset = 0
    max_offset = count_offset(user_id)

    while offset <= max_offset:
        response = requests.get('https://api.vk.com/method/users.getSubscriptions', params={
            'access_token': token,
            'v': 5.103,
            'sort': 'id_desc',
            'user_id': user_id,
            'extended': 1,
            'offset': offset * 20,
            #'offset': 0,
            'fields': 'id'
        }).json()['response']

        offset += 1

        for item in response['items']:

            try:
                s = item['id'], item['name']
                groups_list.append(s)

            # if any group produces error, only this group should be excluded
            except KeyError as E:
                # print(user_id, item, E)
                # faulty_groups.append((user_id, item, E))
                continue

    return groups_list
