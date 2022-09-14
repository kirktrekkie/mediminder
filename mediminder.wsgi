import sys
if sys.version_info[0] < 3:
    raise Exception("Python3 is required!")
sys.path.insert(0, '/home/pi/Public/git/mediminder/')
from webapp import app as application
