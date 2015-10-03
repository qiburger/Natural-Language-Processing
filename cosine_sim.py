__author__ = 'Qi_He'

import math

# calculate cosine similarity of two lists of integers
def cosine_sim(l1, l2):

    if all(x == 0 for x in l1) or all(y == 0 for y in l2):
        return 0
    xx = 0
    yy = 0
    xy = 0
    for i in range(len(l1)):
        x = l1[i]
        y = l2[i]
        xy += x * y
        xx += x ** 2
        yy += y ** 2
    return xy / math.sqrt(xx * yy)