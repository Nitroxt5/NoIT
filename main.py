import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from ui.widgets.main_widget import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('media\\icon.ico'))
    window = MainWindow(app.primaryScreen().availableGeometry())
    window.show()
    sys.exit(app.exec_())
