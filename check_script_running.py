import psutil
import os
from subprocess import Popen


def is_running(script):
    for q in psutil.process_iter():
        if q.name().startswith('python'):
            print(q.name(), q.pid)
            if len(q.cmdline())>1 and script in q.cmdline()[1] and q.pid !=os.getpid():
                print("'{}' Process is already running".format(script))
                return True

    return False


if __name__ == '__main__':
    if not is_running("sense_hat_reminder.py"):
        print("sense_hat_control.py is not running")
        cmd = ["python3", "sense_hat_reminder.py"]
        Popen(cmd)
    else:
        print("sense_hat_control.py is already running")