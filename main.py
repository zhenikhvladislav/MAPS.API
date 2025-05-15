from PyQt6.QtWidgets import QApplication
from mapapi_QT import MapApp

if __name__ == '__main__':
    app = QApplication([])
    window = MapApp()
    window.show()
    app.exec()
