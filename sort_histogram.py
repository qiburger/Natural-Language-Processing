__author__ = 'QHe'

#Take a dictionary and return sorted lists of tuples, one by keys and one by values


def sort_histogram(dict):
    sort_by_values = zip(dict.values(), dict.keys())
    sort_by_keys = dict.items()
    print sort_by_keys
    print sort_by_values
    sorted(sort_by_keys, reverse = True)
    sorted(sort_by_values, reverse = True)
    print sort_by_keys
    return (sort_by_keys, sort_by_values)

if __name__ == '__main__':
    sort_histogram(dict())
    