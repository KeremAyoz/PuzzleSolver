import htmlPy
import datetime


class Controller(htmlPy.Object):

    def __init__(self, app):
        super(Controller, self).__init__()
        self.app = app

    @htmlPy.Slot()
    def say_hello_world(self):
        self.app.html = u"Hello, world"

    @htmlPy.Slot(str, result=str)
    def get_puzzle(self, json_data):
        return "testing"

    @htmlPy.Slot(str, str)
    def console_log(self, log, type):
        if type == "log":
            print(str(datetime.datetime.now().time()) + "[LOG] " + log)
        elif type == "error":
            print(str(datetime.datetime.now().time()) + "[ERROR] " + log)
        else:
            print(str(datetime.datetime.now().time()) + "[UNKNOWN] " + log)
