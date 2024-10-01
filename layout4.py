import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QPushButton, QCheckBox, QLineEdit, QLabel, QVBoxLayout, QGridLayout
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

        self.setWindowTitle("My Enhanced App")

        main_layout = QVBoxLayout()

        button = QPushButton("Haz Click")
        checkbox = QCheckBox("Accepta las cookies mostro")
        text_input = QLineEdit()
        label = QLabel("¿Nombre?:")

        main_layout.addWidget(label)
        main_layout.addWidget(text_input)
        main_layout.addWidget(checkbox)
        main_layout.addWidget(button)

        color_layout = QGridLayout()
        color_layout.addWidget(Color('red'), 0, 0)
        color_layout.addWidget(Color('green'), 1, 0)
        color_layout.addWidget(Color('blue'), 1, 1)
        color_layout.addWidget(Color('purple'), 2, 1)

        main_layout.addLayout(color_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()