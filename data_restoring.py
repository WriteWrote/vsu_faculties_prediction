def restore_groups(groups_path: str):
    lines = []
    with open(groups_path, 'r', encoding='utf-8') as file:
        lines = file.read().split('\n')
    file.close()
    return lines


def scrape_groups_ids(full_data: list, groups_list: list):
    clean_groups = []

    for group in full_data:
        clean_groups.append(str(group[0]))

    result = []

    for group in groups_list:
        if clean_groups.__contains__(group):
            result.append(1)
        else:
            result.append(0)

    return result
