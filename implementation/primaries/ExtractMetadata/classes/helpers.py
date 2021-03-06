def combine_dictionaries(dict1, dict2):
    new_dict = dict1
    for key in dict2:
        if key not in new_dict:
            new_dict[key] = dict2[key]
        elif isinstance(new_dict[key], dict):
            new_dict[key] = combine_dictionaries(new_dict[key], dict2[key])
        elif isinstance(new_dict[key], dict):
            new_dict[key]["other"] = dict2[key]
        elif isinstance(dict2[key], dict):
            cpy = new_dict[key]
            new_dict[key] = {"other": cpy}
            new_dict[key].update(dict2[key])
        else:
            new_dict[key].extend(dict2[key])
    return new_dict


def init_kv(elem, key, init_value=list()):
    """
    Initialise a key in a dictionary with a default value if it doesn't exist already
    """
    if key not in elem:
        elem[key] = init_value


def get_set_of_dict_values(data):
    return [set(data[key]) for key in data]
