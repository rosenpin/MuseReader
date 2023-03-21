class GestureHandler:
    """
    This class checks a model value against a threshold, calls a given function upon detection, and ensures that
    an entire buffer passes before next gesture detection
    """

    def __init__(self, threshold, buffer_length, shift_length):
        self.threshold = threshold
        self.buffer_length = buffer_length
        self.shift_length = shift_length
        self.event_flag = False
        self.event_count = 0

    def evaluate_gesture(self, model_value, call_on_detect):
        if model_value > self.threshold:
            if not self.event_flag:
                self.event_flag = True

                call_on_detect()

            else:
                if self.event_count * self.shift_length > self.buffer_length:
                    self.event_flag = False
                    self.event_count = 0
                else:
                    self.event_count += 1
        else:
            self.event_flag = False
            self.event_count = 0