__author__ = 'QHe'

import sys
import matplotlib.pyplot as plt

def simple_plot(x, y):
    try:
        plt.plot(x, y)
    except:
        print 'plot function takes x and y values to make a simple plot'
    else:
        plt.show()

if __name__ == '__main__':
    simple_plot(*sys.args)