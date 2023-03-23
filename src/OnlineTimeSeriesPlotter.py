# External Packages Import
import matplotlib.pyplot as plt
import numpy as np


class OnlineTimeSeriesPlotter:
    """
    This class has a buffer on size line_size. It is updated on real time with every call to the render method after
    calling init_plot() once
    """

    def __init__(self, line_size, y_min, y_max, threshold=None):
        """
        constructor for the online time series plotter
        :param line_size: the size of the plotted line
        :param y_min: minimum y value in the figure
        :param y_max: maximum y value in the figure
        :param threshold: the threshold is plotted as a constant horizontal line
        """
        self.buffer = np.zeros(line_size)
        self.line = None
        self.ax = None
        self.fig = None
        self.y_min = y_min
        self.y_max = y_max
        self.threshold = threshold

    def init_plot(self):
        """
        this method creates the figure that will be updated at real time
        :return: None
        """
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        plt.ylim([self.y_min, self.y_max])
        plt.ion()
        self.ax.axhline(y=self.threshold, color='r', linestyle='-')
        self.line, = self.ax.plot(self.buffer, '-')  # Returns a tuple of line objects, thus the comma
        plt.show()

    def render(self, x):
        """
        adds new sample x to buffer and updates the figure
        :param x:
        :return:
        """
        self.buffer = np.concatenate([self.buffer[1:], [x]])  # update the buffer

        self.line.set_ydata(self.buffer)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        plt.pause(0.001)
