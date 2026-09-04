from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QDateEdit,
    QTableWidget,
    QGroupBox,
    QHeaderView,
)

from PySide6.QtCore import QDate, Qt
from PySide6.QtGui import QKeyEvent


class TabelaFretes(QTableWidget):
    def keyPressEvent(self, evento: QKeyEvent):
        barra_horizontal = self.horizontalScrollBar()
        barra_vertical = self.verticalScrollBar()

        if evento.key() == Qt.Key_Left:
            barra_horizontal.setValue(
                barra_horizontal.value() - barra_horizontal.singleStep()
            )
            return

        if evento.key() == Qt.Key_Right:
            barra_horizontal.setValue(
                barra_horizontal.value() + barra_horizontal.singleStep()
            )
            return

        if evento.key() == Qt.Key_Up:
            barra_vertical.setValue(
                barra_vertical.value() - barra_vertical.singleStep()
            )
            return

        if evento.key() == Qt.Key_Down:
            barra_vertical.setValue(
                barra_vertical.value() + barra_vertical.singleStep()
            )
            return

        super().keyPressEvent(evento)


class Fretes(QWidget):
    def __init__(self):
        super().__init__()

        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(20, 20, 20, 20)
        layout_principal.setSpacing(15)

        titulo = QLabel("Fretes")
        titulo.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            """)

        layout_principal.addWidget(titulo)

        # ==================================
        # CAIXA DE LANÇAMENTO
        # ==================================

        caixa_lancamento = QGroupBox("Lançamento do Frete")
        layout_lancamento = QVBoxLayout()
        layout_lancamento.setSpacing(10)

        # Linha 1
        linha_1 = QHBoxLayout()

        self.campo_dia = QDateEdit()
        self.campo_dia.setCalendarPopup(True)
        self.campo_dia.setDate(QDate.currentDate())

        self.campo_os = QLineEdit()
        self.campo_os.setPlaceholderText("Nº da OS")

        self.campo_transportadora = QLineEdit()
        self.campo_transportadora.setPlaceholderText("Transportadora")

        linha_1.addWidget(QLabel("Dia"))
        linha_1.addWidget(self.campo_dia)

        linha_1.addWidget(QLabel("OS"))
        linha_1.addWidget(self.campo_os)

        linha_1.addWidget(QLabel("Transportadora"))
        linha_1.addWidget(self.campo_transportadora, 2)

        layout_lancamento.addLayout(linha_1)

        # Linha 2
        linha_2 = QHBoxLayout()

        self.campo_embarque = QLineEdit()
        self.campo_embarque.setPlaceholderText("Local de embarque")

        self.campo_destino = QLineEdit()
        self.campo_destino.setPlaceholderText("Local destino da carga")

        self.campo_placa = QLineEdit()
        self.campo_placa.setPlaceholderText("Placa do caminhão")

        linha_2.addWidget(QLabel("Embarque"))
        linha_2.addWidget(self.campo_embarque, 2)

        linha_2.addWidget(QLabel("Destino"))
        linha_2.addWidget(self.campo_destino, 2)

        linha_2.addWidget(QLabel("Placa"))
        linha_2.addWidget(self.campo_placa)

        layout_lancamento.addLayout(linha_2)

        # Linha 3
        linha_3 = QHBoxLayout()

        self.campo_frete = QLineEdit()
        self.campo_frete.setPlaceholderText("Valor total do frete")

        self.campo_pedagio = QLineEdit()
        self.campo_pedagio.setPlaceholderText("Valor do pedágio")

        self.campo_adiantamento = QLineEdit()
        self.campo_adiantamento.setPlaceholderText("Valor do adiantamento")
        self.campo_saldo = QLineEdit()
        self.campo_saldo.setPlaceholderText("Saldo recebido (após descarga)")

        self.campo_status = QComboBox()
        self.campo_status.addItems(
            [
                "Pendente",
                "Aguardando carregamento",
                "Carregado",
                "Em viagem",
                "Aguardando descarga",
                "Descarregado",
                "Aguardando saldo",
                "Frete quitado",
                "Cancelado",
            ]
        )

        linha_3.addWidget(QLabel("Frete"))
        linha_3.addWidget(self.campo_frete)

        linha_3.addWidget(QLabel("Pedágio"))
        linha_3.addWidget(self.campo_pedagio)

        linha_3.addWidget(QLabel("Adiantamento"))
        linha_3.addWidget(self.campo_adiantamento)

        linha_3.addWidget(QLabel("Status"))
        linha_3.addWidget(self.campo_status, 2)

        layout_lancamento.addLayout(linha_3)

        # Botão
        linha_botao = QHBoxLayout()
        linha_botao.addStretch()

        botao_lancar = QPushButton("Lançar frete")
        botao_lancar.setMinimumWidth(140)

        linha_botao.addWidget(botao_lancar)

        layout_lancamento.addLayout(linha_botao)

        caixa_lancamento.setLayout(layout_lancamento)

        layout_principal.addSpacing(10)
        layout_principal.addWidget(caixa_lancamento)

        # ==================================
        # CAIXA DE FRETES LANÇADOS
        # ==================================

        caixa_fretes = QGroupBox("Fretes Lançados")
        layout_fretes = QVBoxLayout()

        self.tabela_fretes = TabelaFretes()
        self.tabela_fretes.setColumnCount(11)

        self.tabela_fretes.setHorizontalHeaderLabels(
            [
                "Dia",
                "OS",
                "Transportadora",
                "Embarque",
                "Destino",
                "Placa",
                "Frete",
                "Pedágio",
                "Adiantamento",
                "Saldo",
                "Status",
            ]
        )

        self.tabela_fretes.setAlternatingRowColors(True)
        self.tabela_fretes.setSelectionBehavior(QTableWidget.SelectItems)
        self.tabela_fretes.setFocusPolicy(Qt.StrongFocus)
        cabecalho = self.tabela_fretes.horizontalHeader()

        cabecalho.setSectionResizeMode(QHeaderView.Interactive)

        self.tabela_fretes.setColumnWidth(0, 100)  # Dia
        self.tabela_fretes.setColumnWidth(1, 130)  # OS
        self.tabela_fretes.setColumnWidth(2, 220)  # Transportadora
        self.tabela_fretes.setColumnWidth(3, 180)  # Embarque
        self.tabela_fretes.setColumnWidth(4, 180)  # Destino
        self.tabela_fretes.setColumnWidth(5, 110)  # Placa
        self.tabela_fretes.setColumnWidth(6, 130)  # Frete
        self.tabela_fretes.setColumnWidth(7, 120)  # Pedágio
        self.tabela_fretes.setColumnWidth(8, 150)  # Adiantamento
        self.tabela_fretes.setColumnWidth(9, 130)  # Saldo
        self.tabela_fretes.setColumnWidth(10, 190)  # Status

        layout_fretes.addWidget(self.tabela_fretes)

        caixa_fretes.setLayout(layout_fretes)

        layout_principal.addWidget(caixa_fretes, 1)

        # ==================================
        # CAIXA DE COMISSÕES
        # ==================================

        caixa_comissoes = QGroupBox("Comissões dos Motoristas")
        layout_comissoes = QVBoxLayout()

        self.tabela_comissoes = QTableWidget()
        self.tabela_comissoes.setColumnCount(6)

        self.tabela_comissoes.setHorizontalHeaderLabels(
            [
                "Dia",
                "OS",
                "Motorista",
                "Placa",
                "Viagem",
                "Comissão",
            ]
        )

        self.tabela_comissoes.setAlternatingRowColors(True)
        self.tabela_comissoes.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabela_comissoes.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )

        layout_comissoes.addWidget(self.tabela_comissoes)

        caixa_comissoes.setLayout(layout_comissoes)

        layout_principal.addWidget(caixa_comissoes, 1)

        self.setLayout(layout_principal)
