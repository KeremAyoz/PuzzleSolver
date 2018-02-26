import htmlPy
from controller import Controller
import os
import PySide

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# GUI initializations
app = htmlPy.AppGUI(title=u"PuzzleSolver", maximized=True, plugins=True)


# GUI configurations
app.static_path = os.path.join(BASE_DIR, "static/")
app.template_path = os.path.join(BASE_DIR, "templates/")

app.window.setWindowIcon(PySide.QtGui.QIcon(BASE_DIR + "/static/img/icon.png"))

# Register back-end functionalities
app.bind(Controller(app, BASE_DIR))

app.template = ("index.html", {})

if __name__ == "__main__":
    app.start()