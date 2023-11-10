def setup_occupation_list(path: str):
    occupation_list = []

    with open(path, "r") as occupation_file:
        tmp_occupation_list = occupation_file.readlines()
        for item in tmp_occupation_list:
            if item.startswith("#") or item.startswith("---"):
                continue
            occupation_list.append(item.strip())

    return occupation_list


def setup_occupation_dict(path: str):
    with open(path, "r") as occupation_file:
        tmp_occupation_list = occupation_file.readlines()
        occupation_dict = {}
        category = ""
        category_instances = []
        for item in tmp_occupation_list:
            if item.startswith("#"):
                continue
            if item.startswith("---"):
                category = item.lstrip("---")
                category = category.strip()
                continue
            if item == "\n":
                occupation_dict[category] = category_instances
                category_instances = []
                continue
            category_instances.append(item.strip())

    return occupation_dict


def get_occupation_category(occupation, occupation_dict):
    found_category = None
    for category in occupation_dict:
        if occupation in occupation_dict[category]:
            found_category = category
    return found_category


def extract_occupation(paragraph_text, occupation_list):
    occupation = None
    # only look at the first two paragraphs for now
    paragraph_text = paragraph_text.strip()
    for token in paragraph_text.split(" "):
        for occupation_candidate in occupation_list:
            if token.lower() == occupation_candidate.lower():
                occupation = token
                return occupation

    # sys.exit()
    return occupation
