from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from componentes.card import Card
from banco.sessao import SessionLocal
from banco.modelos import Veiculo


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()

        layout_principal = QVBoxLayout()

        linha_cards = QHBoxLayout()

        self.card_veiculos = Card("Veículos", self.contar_veiculos())
        self.card_motoristas = Card("Motoristas", 0)
        self.card_manutencoes = Card("Manutenções", 0)

        linha_cards.addWidget(self.card_veiculos)
        linha_cards.addWidget(self.card_motoristas)
        linha_cards.addWidget(self.card_manutencoes)

        layout_principal.addLayout(linha_cards)

        self.setLayout(layout_principal)

    def contar_veiculos(self):
        sessao = SessionLocal()

        try:
            quantidade = sessao.query(Veiculo).count()
            return quantidade

        finally:
            sessao.close()
