import os
from time import sleep
from subprocess import run
from json import load
from datetime import datetime

DEVICE_IDS = ['4f82cc3213f4eff5']
KDECONNECT_COMMAND = 'kdeconnect-cli  -d {} --ping-msg'
MESSAGE = "Remember to give medicine!"

path = "/".join(os.path.realpath(__file__).split('/')[:-1])
MEDICINE_STATUS_FILE = os.path.join(path, "medicine_status.json")
TIME_LIMITS = os.path.join(path, "time_limits.json")


def send_alert():
    for device_id in DEVICE_IDS:
        cmd = KDECONNECT_COMMAND.format(device_id).split(' ')
        cmd.append(MESSAGE)
        run(cmd, check=True)


def check_if_alert_shall_be_sent():
    with open(MEDICINE_STATUS_FILE) as ms_json:
        medicine_status = load(ms_json)
    with open(TIME_LIMITS) as time_limits_file:
        time_limits = load(time_limits_file)

    current_time = datetime.now().time()

    for key in medicine_status:
        print("key {} medicine_status {}".format(key, medicine_status[key]))
        if key != "date":
            if not medicine_status[key]["given"]:
                alert_time_object = datetime.strptime(time_limits[key]["red"], "%H:%M").time()
                print("time_object {}".format(alert_time_object))
                print("current_time {}".format(current_time))
                if alert_time_object < current_time:
                    print("Send alert! {}".format(key))
                    send_alert()
                else:
                    print("No alert needed. {}".format(key))


if __name__ == '__main__':
    while True:
        check_if_alert_shall_be_sent()
        sleep(1800)
