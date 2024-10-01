import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt6.QtGui import QPalette, QColor

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Vertical y Horizontal")

        main_layout = QVBoxLayout()

        button_layout = QHBoxLayout()

        button1 = QPushButton("Boton 1")
        button2 = QPushButton("Boton 2")
        button3 = QPushButton("Boton 3")

        button_layout.addWidget(button1)
        button_layout.addWidget(button2)
        button_layout.addWidget(button3)

        main_layout.addLayout(button_layout)

        color_widget = Color('cyan')
        main_layout.addWidget(color_widget)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()