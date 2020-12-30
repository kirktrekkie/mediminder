#from sense_hat import SenseHat
from sense_emu import SenseHat


class MySense:
    def __init__(self):
        self.sense = SenseHat()

    def get_temp(self):
        return self.sense.get_temperature()

    def get_humid(self):
        return self.sense.get_humidity()

    def get_press(self):
        return self.sense.get_pressure()

    def get_events(self):
        return self.sense.stick.get_events()

    def print_message(self, message):
        self.sense.show_message("Temperature: {}".format(message))


if __name__ == '__main__':
    my_sense = MySense()
    t = my_sense.get_temp()
    my_sense.print_message(t)
