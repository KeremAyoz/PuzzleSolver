import htmlPy


class Controller(htmlPy.Object):

    def __init__(self, app):
        super(Controller, self).__init__()
        self.app = app

    @htmlPy.Slot()
    def say_hello_world(self):
        self.app.html = u"Hello, world"

    @htmlPy.Slot(str, result = str)
    def get_puzzle(self, date):
        return "testing"
