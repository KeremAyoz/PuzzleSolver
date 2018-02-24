import json
import htmlPy
from datetime import datetime


class Controller(htmlPy.Object):

    puzzles = None

    def __init__(self, app):
        super(Controller, self).__init__()
        self.app = app
        try:
            self.puzzles = json.load(open('back_end/Data/data.json'))
        except:
            self.console_log('data.json not found!', 'error')

    @htmlPy.Slot()
    def say_hello_world(self):
        self.app.html = u"Hello, world"

    @htmlPy.Slot(str)
    def get_puzzle(self, json_data):
        # Check date
        puzzle_date = datetime.strptime(json.loads(json_data)['date'], "%d-%m-%Y").date()
        if puzzle_date.weekday() == 5:
            self.app.evaluate_javascript("alert('You cannot get this puzzle because, it\\'s SATURDAY!')");
            return

        # Find Puzzle
        puzzle = None
        if self.puzzles is not None:
            for x in self.puzzles:
                if x['date'] == str(puzzle_date):
                    puzzle = x
                    break;

        # Not found
        if puzzle is None:
            self.app.evaluate_javascript("alert('Sorry, Puzzle not fetched yet!')");
            return
        self.app.evaluate_javascript("initPuzzle(" + json.dumps(puzzle) + ")")

    # Forward JS console.log to shell
    @htmlPy.Slot(str, str)
    def console_log(self, log, type="log"):
        if type == "log":
            print(str(datetime.now().time()) + "[LOG] " + log)
        elif type == "error":
            print(str(datetime.now().time()) + "[ERROR] " + log)
        else:
            print(str(datetime.now().time()) + "[UNKNOWN] " + log)
