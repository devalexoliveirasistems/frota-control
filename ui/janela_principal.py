from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
)

from telas.dashboard import Dashboard
from telas.frota import Frota
from telas.fretes import Fretes


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gestão de Frotas")
        self.resize(1200, 700)

        # Widget principal
        central = QWidget()
        self.setCentralWidget(central)

        # Layout principal
        layout_principal = QHBoxLayout(central)

        # MENU LATERAL
        menu = QWidget()
        menu.setFixedWidth(220)

        menu_layout = QVBoxLayout(menu)

        titulo = QLabel("GESTÃO DE FROTAS")
        menu_layout.addWidget(titulo)

        botao_dashboard = QPushButton("Dashboard")
        botao_frota = QPushButton("Frota")
        botao_fretes = QPushButton("Fretes")
        botao_motoristas = QPushButton("Motoristas")
        botao_manutencao = QPushButton("Manutenção")
        botao_abastecimento = QPushButton("Abastecimento")
        botao_custos = QPushButton("Custos")

        menu_layout.addWidget(botao_dashboard)
        menu_layout.addWidget(botao_frota)
        menu_layout.addWidget(botao_fretes)
        menu_layout.addWidget(botao_motoristas)
        menu_layout.addWidget(botao_manutencao)
        menu_layout.addWidget(botao_abastecimento)
        menu_layout.addWidget(botao_custos)

        menu_layout.addStretch()

        botao_configuracoes = QPushButton("Configurações")
        menu_layout.addWidget(botao_configuracoes)
        botao_dashboard.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.tela_dashboard)
        )

        botao_frota.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.tela_frota)
        )
        botao_fretes.clicked.connect(
            lambda: self.stack.setCurrentWidget(self.tela_fretes)
        )

        # ÁREA PRINCIPAL
        # ÁREA PRINCIPAL
        conteudo = QWidget()
        conteudo_layout = QVBoxLayout(conteudo)

        self.stack = QStackedWidget()

        self.tela_dashboard = Dashboard()
        self.tela_frota = Frota()
        self.tela_fretes = Fretes()

        self.stack.addWidget(self.tela_dashboard)
        self.stack.addWidget(self.tela_frota)
        self.stack.addWidget(self.tela_fretes)

        conteudo_layout.addWidget(self.stack)

        # JUNTANDO MENU + CONTEÚDO
        layout_principal.addWidget(menu)
        layout_principal.addWidget(conteudo)
