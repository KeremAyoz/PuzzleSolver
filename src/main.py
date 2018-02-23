import htmlPy
from back_end import BackEnd
import os
import PySide

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# GUI initializations
app = htmlPy.AppGUI(title=u"PuzzleSolver", maximized=False, plugins=True)


# GUI configurations
static = os.path.join(BASE_DIR, "static/")
print(str(static))
app.static_path = static
app.template_path = os.path.join(BASE_DIR, "templates/")

app.window.setWindowIcon(PySide.QtGui.QIcon(BASE_DIR + "/static/img/icon.png"))

# Register back-end functionalities
app.bind(BackEnd(app))

app.template = ("index.html", {})

if __name__ == "__main__":
    app.start()