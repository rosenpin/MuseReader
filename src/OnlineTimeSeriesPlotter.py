import matplotlib.pyplot as plt
import numpy as np


class OnlineTimeSeriesPlotter:

    def __init__(self, line_size, y_min, y_max, threshold=None):
        self.buffer = np.zeros(line_size)
        self.line = None
        self.ax = None
        self.fig = None
        self.y_min = y_min
        self.y_max = y_max
        self.threshold = threshold

    def init_plot(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        plt.ylim([self.y_min, self.y_max])
        plt.ion()
        self.ax.axhline(y=self.threshold, color='r', linestyle='-')
        self.line, = self.ax.plot(self.buffer, 'r-')  # Returns a tuple of line objects, thus the comma
        plt.show()

    def render(self, x):
        """
        adds new sample x to buffer
        :param x:
        :return:
        """
        self.buffer = np.concatenate([self.buffer[1:], [x]])  # update the buffer

        self.line.set_ydata(self.buffer)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        plt.pause(0.001)
