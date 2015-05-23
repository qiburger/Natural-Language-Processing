__author__ = 'QHe'

from pylab import *
import sys

def plot(x, y, label_1 = 'x', label_2 = 'y', plot_title = 'Simple Plot', filename = "test.png"):
    plot(x, y)

    xlabel(label_1)
    ylabel(label_2)
    title(plot_title)
    grid(True)
    savefig(filename)
    show()

if __name__ == '__main__':
    plot(*sys.args)