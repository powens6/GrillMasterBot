class Servo:
    def __init__(self, min_angle, max_angle, min_pulse, max_pulse):
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.min_pulse = min_pulse
        self.max_pulse = max_pulse

    def calculate_pulse_length(self, angle):
        return int((angle - self.min_angle) * (self.max_pulse - self.min_pulse) / (self.max_angle - self.min_angle) + self.min_pulse)