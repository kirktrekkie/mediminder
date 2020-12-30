import os
from json import load
from webapp import check_color, give_medicine, write_medicine_status
from gpiozero import LED, Button
from datetime import datetime, timedelta
from time import  sleep
import threading

path = "/".join(os.path.realpath(__file__).split('/')[:-1])
MEDICINE_STATUS_FILE = os.path.join(path, "medicine_status.json")
TIME_LIMITS = os.path.join(path, "time_limits.json")

IO_PINS = {
    'morning': {
        'green': LED(17),
        'red': LED(27),
        'button': Button(22)
    },
    'day': {
        'green': LED(23),
        'red': LED(24),
        'button': Button(25)
    },
    'night': {
        'green': LED(5),
        'red': LED(6),
        'button': Button(26)
    }
}


def read_time_limits():
    with open(TIME_LIMITS) as time_limits_file:
        time_limits = load(time_limits_file)

    return time_limits


def wait_for_button_input(key):  # thread method
    # print("Wait for button {}".format(key))
    IO_PINS[key]['button'].wait_for_press(timeout=1)
    if IO_PINS[key]['button'].is_pressed:
        print('Button {} is pressed'.format(key))
        with open(MEDICINE_STATUS_FILE) as ms_json:
            medicine_status = load(ms_json)
        medicine_status = give_medicine(medicine_status, key)
        write_medicine_status(medicine_status)
        IO_PINS[key]['green'].on()
        IO_PINS[key]['red'].off()


def loop(time_limits):
    today = datetime.today().day
    is_checked = False

    while True:
        current_time = datetime.now().time()

        # Check every other minute
        if current_time.minute % 2 == 0:
            if not is_checked:
                is_checked = True
                with open(MEDICINE_STATUS_FILE) as ms_json:
                    medicine_status = load(ms_json)

                for key in time_limits:
                    # Check if green led should be lit
                    if medicine_status[key]['given']:
                        print('Turn on green led for {}'.format(key))
                        IO_PINS[key]['green'].on()
                    else:
                        print('No green led for {}'.format(key))

                        alert_time_object = datetime.strptime(time_limits[key]["red"], "%H:%M").time()
                        end_time_object = alert_time_object.replace(minute=alert_time_object.minute + 1)

                        # Check if red led should be lit
                        if alert_time_object < current_time: # < end_time_object:
                            print('Turn on red led for {}'.format(key))
                            print('pin {}'.format(IO_PINS[key]['red']))
                            IO_PINS[key]['red'].on()
                        else:
                            print('No red led needed, time not in range')
        else:
            is_checked = False

        # Check button pressed
        button_thread = []
        for key in IO_PINS:
            thread = threading.Thread(target=wait_for_button_input, args=(key,))
            thread.start()
            button_thread.append(thread)
        for thread in button_thread:
            thread.join()
            # if IO_PINS[key]['button'].is_pressed:
            #     with open(MEDICINE_STATUS_FILE) as ms_json:
            #         medicine_status = load(ms_json)
            #     medicine_status = give_medicine(medicine_status, key)
            #     write_medicine_status(medicine_status)
            #     IO_PINS[key]['green'].on()
            #     IO_PINS[key]['red'].off()

        # Turn off all leds on new day
        if today != datetime.today().day:
            for key in IO_PINS:
                IO_PINS[key]['red'].off()
                IO_PINS[key]['green'].off()
                today = datetime.today().day

        # sleep(1)


if __name__ == '__main__':
    print('Starting led control')
    tl = read_time_limits()
    loop(tl)
