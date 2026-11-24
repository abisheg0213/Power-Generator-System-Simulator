class FrequencySensor:
    def __init__(self):
        self.frequency = 50
    def generator_providing_load(self):
        self.frequency -= 0.05
    def generator_not_providing_load_running(self):
        self.frequency += 0.12
    def generator_off_and_load_running(self):
        self.frequency -= 0.15
    def get_frequency(self):
        return self.frequency