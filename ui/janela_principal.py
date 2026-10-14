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
from telas.motoristas import Motoristas
from telas.documentos import Documentos
from telas.abastecimento import TelaAbastecimento
from telas.simulador import SimuladorFretes


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
        menu.setObjectName("menuLateral")
        menu.setFixedWidth(240)

        menu_layout = QVBoxLayout(menu)
        menu_layout.setContentsMargins(12, 18, 12, 16)
        menu_layout.setSpacing(8)

        menu.setStyleSheet("""
            QWidget#menuLateral {
                background-color: #0f172a;
            }

            QWidget#menuLateral QLabel#marcaIcone {
                background-color: #2563eb;
                color: #ffffff;
                border-radius: 10px;
                font-size: 18px;
                font-weight: 800;
                padding: 0px;
                qproperty-alignment: AlignCenter;
            }

            QWidget#menuLateral QLabel#tituloMarca {
                color: #f8fafc;
                font-size: 15px;
                font-weight: 800;
                padding: 0px;
            }

            QWidget#menuLateral QLabel#subtituloMarca {
                color: #94a3b8;
                font-size: 9px;
                font-weight: 600;
                padding: 0px;
            }

            QWidget#menuLateral QPushButton {
                background-color: transparent;
                color: #cbd5e1;
                border: none;
                border-radius: 8px;
                text-align: left;
                padding: 12px 14px;
                font-size: 14px;
                font-weight: 600;
            }

            QWidget#menuLateral QPushButton:hover {
                background-color: #1e293b;
                color: #ffffff;
            }

            QWidget#menuLateral QPushButton[ativo="true"] {
                background-color: #1d4ed8;
                color: #ffffff;
                border-left: 3px solid #93c5fd;
            }

            QWidget#menuLateral QPushButton[ativo="true"]:hover {
                background-color: #1d4ed8;
                color: #ffffff;
            }

            QWidget#menuLateral QPushButton:pressed {
                background-color: #334155;
                color: #ffffff;
            }
        """)

        cabecalho_marca = QWidget()
        cabecalho_layout = QHBoxLayout(cabecalho_marca)
        cabecalho_layout.setContentsMargins(8, 8, 8, 22)
        cabecalho_layout.setSpacing(10)

        marca_icone = QLabel("FG")
        marca_icone.setObjectName("marcaIcone")
        marca_icone.setFixedSize(44, 44)

        coluna_marca = QVBoxLayout()
        coluna_marca.setContentsMargins(0, 0, 0, 0)
        coluna_marca.setSpacing(3)

        titulo = QLabel("FROTA GESTÃO")
        titulo.setObjectName("tituloMarca")

        subtitulo = QLabel("GESTÃO DE TRANSPORTE")
        subtitulo.setObjectName("subtituloMarca")

        coluna_marca.addWidget(titulo)
        coluna_marca.addWidget(subtitulo)

        cabecalho_layout.addWidget(marca_icone)
        cabecalho_layout.addLayout(coluna_marca)
        menu_layout.addWidget(cabecalho_marca)

        botao_dashboard = QPushButton("Dashboard")
        botao_frota = QPushButton("Frota")
        botao_fretes = QPushButton("Fretes")
        botao_simulador = QPushButton("Simulador de Frete")
        botao_motoristas = QPushButton("Motoristas")
        botao_documentos = QPushButton("Documentos")
        botao_manutencao = QPushButton("Manutenção")
        botao_abastecimento = QPushButton("Abastecimento")
        botao_custos = QPushButton("Custos")

        menu_layout.addWidget(botao_dashboard)
        menu_layout.addWidget(botao_frota)
        menu_layout.addWidget(botao_fretes)
        menu_layout.addWidget(botao_simulador)
        menu_layout.addWidget(botao_motoristas)
        menu_layout.addWidget(botao_documentos)
        menu_layout.addWidget(botao_manutencao)
        menu_layout.addWidget(botao_abastecimento)
        menu_layout.addWidget(botao_custos)

        menu_layout.addStretch()

        botao_configuracoes = QPushButton("Configurações")
        menu_layout.addWidget(botao_configuracoes)
        self.botoes_navegacao = [
            botao_dashboard,
            botao_frota,
            botao_fretes,
            botao_simulador,
            botao_motoristas,
            botao_documentos,
            botao_abastecimento,
        ]

        botao_dashboard.clicked.connect(
            lambda checked=False: self.ir_para_tela(
                self.tela_dashboard, botao_dashboard
            )
        )

        botao_frota.clicked.connect(
            lambda checked=False: self.ir_para_tela(self.tela_frota, botao_frota)
        )

        botao_fretes.clicked.connect(
            lambda checked=False: self.ir_para_tela(self.tela_fretes, botao_fretes)
        )

        botao_simulador.clicked.connect(
            lambda checked=False: self.ir_para_tela(
                self.tela_simulador, botao_simulador
            )
        )

        botao_motoristas.clicked.connect(
            lambda checked=False: self.ir_para_tela(
                self.tela_motoristas, botao_motoristas
            )
        )

        botao_documentos.clicked.connect(
            lambda checked=False: self.ir_para_tela(
                self.tela_documentos, botao_documentos
            )
        )

        botao_abastecimento.clicked.connect(
            lambda checked=False: self.ir_para_tela(
                self.tela_abastecimento, botao_abastecimento
            )
        )

        # ÁREA PRINCIPAL
        conteudo = QWidget()
        conteudo_layout = QVBoxLayout(conteudo)

        self.stack = QStackedWidget()

        self.tela_dashboard = Dashboard()
        self.tela_frota = Frota()
        self.tela_fretes = Fretes()
        self.tela_simulador = SimuladorFretes()

        self.tela_motoristas = Motoristas()
        self.tela_documentos = Documentos()
        self.tela_abastecimento = TelaAbastecimento()

        self.stack.addWidget(self.tela_dashboard)
        self.stack.addWidget(self.tela_frota)
        self.stack.addWidget(self.tela_fretes)
        self.stack.addWidget(self.tela_simulador)
        self.stack.addWidget(self.tela_motoristas)
        self.stack.addWidget(self.tela_documentos)
        self.stack.addWidget(self.tela_abastecimento)

        conteudo_layout.addWidget(self.stack)

        # JUNTANDO MENU + CONTEÚDO
        layout_principal.addWidget(menu)
        layout_principal.addWidget(conteudo)
        self.ir_para_tela(self.tela_dashboard, botao_dashboard)

    def ir_para_tela(self, tela, botao_ativo):
        self.stack.setCurrentWidget(tela)

        for botao in self.botoes_navegacao:
            botao.setProperty("ativo", botao is botao_ativo)
            botao.style().unpolish(botao)
            botao.style().polish(botao)
            botao.update()
