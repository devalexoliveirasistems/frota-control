from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class Fretes(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        titulo = QLabel("Fretes")

        layout.addWidget(titulo)

        self.setLayout(layout)
