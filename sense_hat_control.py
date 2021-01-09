from sense_hat import SenseHat
from time import sleep
from datetime import datetime
from random import randint
#from sense_emu import SenseHat

X = [0, 255, 0]  # Red
O = [0, 0, 0]  # Dark

happy_smile = [
O, O, O, O, O, O, O, O,
O, O, X, O, O, X, O, O,
O, O, O, O, O, O, O, O,
O, O, O, O, O, O, O, O,
O, X, O, O, O, O, X, O,
O, O, X, X, X, X, O, O,
O, O, O, O, O, O, O, O,
O, O, O, O, O, O, O, O
]


class MySense:
    def __init__(self):
        self.sense = SenseHat()
        self.sense.set_imu_config(False, False, True)
        self.init_acc = self.sense.get_accelerometer_raw()
        self.clear()
        self.sense.set_rotation(90)
        if 9 < datetime.now().hour < 18:
            self.sense.low_light = False
        else:
            self.sense.low_light = True

    def get_temp(self):
        return round(self.sense.get_temperature(), 1)

    def get_humid(self):
        return round(self.sense.get_humidity(), 1)

    def get_press(self):
        return round(self.sense.get_pressure(), 1)

    def get_events(self):
        return self.sense.stick.get_events()

    def get_acceleration(self):
        return self.sense.get_accelerometer_raw()

    def check_movement(self):
        accel = self.get_acceleration()
        for k in accel:
            #print(accel[k])
            if abs(accel[k]) > 1.3:
                return True
        return False

    def print_message(self, message):
        self.sense.show_message("{}".format(message))

    def set_happy(self):
        self.sense.set_pixels(happy_smile)

    def red_blink(self):
        self.blink(color=(255, 0, 0))

    def green_blink(self):
        self.blink(color=(0, 255, 0))

    def blink(self, blinks=6, color=None, blink_time=0.5):
        if not color:
            color = self.get_random_color()
        for i in range(blinks):
            if i % 2 == 0:
                self.clear()
            else:
                self.clear(color)
            sleep(blink_time)
        self.clear()

    def clear(self, color=None):
        if color:
            color_rgb = color
        else:
            color_rgb = (0, 0, 0)
        self.sense.clear(color_rgb)

    def moving_pixel(self):
        for i in range(8):
            for j in range(8):
                #print(i, j)
                self.sense.set_pixel(i, j, randint(10,170)+j*10, randint(10,170)+i*10, randint(10,170)+(i+j)*5)
                sleep(0.1)
                self.sense.set_pixel(i, j, 0, 0, 0)

    def random_light_up(self):
        O = [0, 0, 0]
        board = [
            O, O, O, O, O, O, O, O,
            O, O, O, O, O, O, O, O,
            O, O, O, O, O, O, O, O,
            O, O, O, O, O, O, O, O,
            O, O, O, O, O, O, O, O,
            O, O, O, O, O, O, O, O,
            O, O, O, O, O, O, O, O,
            O, O, O, O, O, O, O, O
        ]
        run = True
        while run:
            run = False
            for i, led in enumerate(board):
                if led == O:
                    run = True
                    if randint(0,63) == 1:
                        board[i] = self.get_random_color()
                        self.sense.set_pixels(board)
                        sleep(0.02)

    @staticmethod
    def get_random_color():
        red = green = blue = 0
        while red == 0 and green == 0 and blue == 0:
            red = randint(0,1)
            green = randint(0,1)
            blue = randint(0,1)
        return (255*red, 255*green, 255*blue)


if __name__ == '__main__':
    my_sense = MySense()
    t = my_sense.get_temp()
    my_sense.print_message(t)
    #my_sense.clear()

    #my_sense.moving_pixel()
    #my_sense.random_light_up()
    #my_sense.blink(10)

    #for i in range(20):
    #    print(my_sense.get_acceleration())
    #    sleep(0.5)

    while not my_sense.check_movement():
        sleep(1)

    my_sense.blink(10)
    sleep(5)
    my_sense.clear()
