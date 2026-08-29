from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class Card(QWidget):
    def __init__(self, titulo, valor):
        super().__init__()

        self.titulo_label = QLabel(titulo)
        self.valor_label = QLabel(str(valor))

        layout = QVBoxLayout()
        layout.addWidget(self.titulo_label)
        layout.addWidget(self.valor_label)

        self.setLayout(layout)

    def atualizar_valor(self, valor):
        self.valor_label.setText(str(valor))
