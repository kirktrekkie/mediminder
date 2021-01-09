import os
from json import load
from webapp import check_color, give_medicine, write_medicine_status, update_day, read_medicine_status
from datetime import datetime, timedelta
from time import  sleep
from sense_hat_control import MySense
import threading

path = "/".join(os.path.realpath(__file__).split('/')[:-1])
MEDICINE_STATUS_FILE = os.path.join(path, "medicine_status.json")
TIME_LIMITS = os.path.join(path, "time_limits.json")


def read_time_limits():
    with open(TIME_LIMITS) as time_limits_file:
        time_limits = load(time_limits_file)

    return time_limits


def loop(time_limits):
    today = datetime.today().day
    sense = MySense()
    is_checked = False

    while True:
        current_time = datetime.now().time()

        # Check every other minute
        if current_time.minute % 2 == 0:
            if not is_checked:
                print("Current time: {}".format(current_time))
                is_checked = True
                with open(MEDICINE_STATUS_FILE) as ms_json:
                    medicine_status = load(ms_json)

                for key in time_limits:
                    # Check if green led should be lit
                    if medicine_status[key]['given']:
                        print('Medicine given for {}'.format(key))
                    else:
                        print('Medicine not given for {}'.format(key))

                        alert_time_object = datetime.strptime(time_limits[key]["red"], "%H:%M").time()
                        end_time_object = alert_time_object.replace(minute=alert_time_object.minute + 1)

                        # Check if red led should be lit
                        if alert_time_object < current_time: # < end_time_object:
                            print('Show message for {}'.format(key))
                            sense.red_blink()
                            sense.print_message('Give {} medicine!'.format(key))
                            sense.red_blink()
                            is_checked = False
                        else:
                            print('No message needed, time not in range')
        else:
            is_checked = False

        # Check button pressed
        events = sense.get_events()
        for event in events:
            update_given()
            print("The joystick was {} {}".format(event.action, event.direction))
            sense.green_blink()

        # Check movement
        if sense.check_movement():
            update_given()
            print("Movement detected")
            sense.green_blink()

        # Check new day
        if today != datetime.today().day:
            update_day()
            today = datetime.today().day

        sleep(1)


def update_given():
    medicine_status = read_medicine_status(MEDICINE_STATUS_FILE)
    current_hour = datetime.now().hour
    if current_hour < 12:
        check_and_give(medicine_status, "morning")
    elif current_hour < 18:
        check_and_give(medicine_status, "day")
    else:
        check_and_give(medicine_status, "night")


def check_and_give(medicine_status, time_of_day):
    if not medicine_status[time_of_day]['given']:
        give_medicine(medicine_status, time_of_day)


if __name__ == '__main__':
    print('Starting sense reminder')
    tl = read_time_limits()
    loop(tl)
