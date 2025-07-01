import sys
from PyQt5.QtWidgets import QApplication

from ui.pipeline import Pipeline


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Pipeline()
    window.show()
    sys.exit(app.exec_())
