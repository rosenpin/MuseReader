class GestureHandler:
    """
    This class checks a model value against a threshold, calls a given function upon detection, and ensures that
    an entire buffer passes before next gesture detection
    """

    def __init__(self, threshold, time_delay_seconds, shift_length):
        """
        Constructor for a gesture handler
        :param threshold: The threshold to be compared against
        :param time_delay_seconds: time to wait between two consecutive positive detections.
        :param shift_length: Shift length in seconds between two consecutive buffers. Used to calculate the delay
        """
        self.threshold = threshold
        self.time_delay_seconds = time_delay_seconds
        self.shift_length = shift_length
        self.event_flag = False
        self.event_count = 0

    def evaluate_gesture(self, model_value, call_on_detect):
        """
        Compared model value to the set threshold and if higher calls call_on_detect(). Also Implements delay.
        :param model_value: the model result. A number
        :param call_on_detect: this function will be called if detection is successful.
        :return:
        """
        # if the event flag is raised, detection won't happen again
        if self.event_flag:
            if self.event_count * self.shift_length > self.time_delay_seconds:
                # return to base state
                self.event_flag = False
                self.event_count = 0
            else:
                self.event_count += 1
            return

        # check value against threshold
        if model_value > self.threshold:
            # detection successful. Update flag and call given function
            self.event_flag = True

            call_on_detect()
