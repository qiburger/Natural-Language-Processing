__author__ = 'QHe'

#Take a dictionary and return sorted lists of tuples, one by keys and one by values


def sort_histogram(dict):
    sort_by_values = sorted(zip(dict.values(), dict.keys()), reverse=True)
    sort_by_keys = sorted(dict.items())
    return (sort_by_keys, sort_by_values)

