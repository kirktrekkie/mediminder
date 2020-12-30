import os
from flask import Flask, redirect, request, render_template, url_for
from json import load, dump
from datetime import date, datetime, time
from sense_hat_control import MySense

app = Flask(__name__)

path = "/".join(os.path.realpath(__file__).split('/')[:-1])
MEDICINE_STATUS_FILE = os.path.join(path, "medicine_status.json")
TIME_LIMITS = os.path.join(path, "time_limits.json")
MEDICINE_STATUS_TEMPLATE = os.path.join(path, "medicine_status_template.json")


@app.route('/', methods=['GET', 'POST'])
def main_route():
    medicine_status = read_medicine_status(MEDICINE_STATUS_FILE)
    date_object = datetime.strptime(medicine_status["date"], "%y%m%d").date()

    if date_object != date.today():
        medicine_status = read_medicine_status(MEDICINE_STATUS_TEMPLATE)
        medicine_status["date"] = date.today().strftime("%y%m%d")
        write_medicine_status(medicine_status)

    if request.method == 'POST':
        medicine_status = give_medicine(medicine_status, request.form['submit_button'])
        write_medicine_status(medicine_status)
        return redirect(url_for('main_route'))

    medicine_status = read_medicine_status(MEDICINE_STATUS_FILE)
    morning = medicine_status["morning"]
    day = medicine_status["day"]
    night = medicine_status["night"]
    my_sense = MySense()
    sense = {'temperature': my_sense.get_temp(),
             'humidity': my_sense.get_humid(),
             'pressure': my_sense.get_press()}

    return render_template("index.html", morning=morning, day=day, night=night, sense=sense)


def check_color(medicine_status):
    """Check which color should be displayed."""
    current_time = datetime.now().time()
    with open(TIME_LIMITS) as time_limits_file:
        time_limits = load(time_limits_file)

        for key in medicine_status:
            print("key {} medicine_status {}".format(key, medicine_status[key]))
            if key != "date":
                if medicine_status[key]["given"]:
                    medicine_status[key]["color"] = "success"
                else:
                    time_object = datetime.strptime(time_limits[key]["red"], "%H:%M").time()
                    print ("time_object {}".format(time_object))
                    print("current_time {}".format(current_time))
                    if time_object < current_time:
                        medicine_status[key]["color"] = "danger"
                    elif datetime.strptime(time_limits[key]["yellow"], "%H:%M").time() < current_time:
                        medicine_status[key]["color"] = "warning"
                    else:
                        medicine_status[key]["color"] = "info"
            print("key {} medicine_status {}".format(key, medicine_status[key]))

    return medicine_status


def give_medicine(medicine_status, button):
    if not medicine_status[button.lower()]["given"]:
        current_time = datetime.now().time().strftime("%H:%M:%S")
        medicine_status[button.lower()]["time"] = current_time
        medicine_status[button.lower()]["given"] = True
        return medicine_status


def read_medicine_status(file):
    with open(file) as ms_json:
        medicine_status = load(ms_json)
        return check_color(medicine_status)


def write_medicine_status(medicine_status):
    print("medicine_status {}".format(medicine_status))
    if medicine_status:
        with open(MEDICINE_STATUS_FILE, "w") as ms_json:
            dump(medicine_status, ms_json)
    else:
        print("medicine_status not defined: {}".format(medicine_status))


if __name__ == '__main__':
   app.run(debug=True, host='localhost')