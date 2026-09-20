from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QDateEdit,
    QTableWidget,
    QTableWidgetItem,
    QGroupBox,
    QHeaderView,
    QMessageBox,
    QTabWidget,
)

from PySide6.QtCore import QDate, Qt
from PySide6.QtGui import QKeyEvent

from banco.sessao import SessionLocal
from banco.modelos import Frete, Veiculo, Motorista
from telas.edicao_frete import EdicaoFrete
from decimal import Decimal


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
        layout_principal.setContentsMargins(10, 5, 10, 5)
        layout_principal.setSpacing(10)

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
        caixa_lancamento.setStyleSheet("""
            QGroupBox {
                border: 1px solid #d9dee7;
                border-radius: 10px;
                margin-top: 12px;
                padding: 14px;
                background-color: #ffffff;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 6px;
                color: #111827;
                font-size: 15px;
                font-weight: bold;
            }
        """)
        layout_lancamento = QVBoxLayout()
        layout_lancamento.setSpacing(15)

        # ==================================
        # CAMPOS DO FRETE
        # ==================================

        self.campo_dia = QDateEdit()
        self.campo_dia.setCalendarPopup(True)
        self.campo_dia.setDate(QDate.currentDate())

        self.campo_os = QLineEdit()
        self.campo_os.setPlaceholderText("N° Contrato")

        self.campo_transportadora = QLineEdit()
        self.campo_transportadora.setPlaceholderText("Transportadora")

        self.campo_peso = QLineEdit()
        self.campo_peso.setPlaceholderText("Peso da carga (kg)")

        self.campo_embarque = QLineEdit()
        self.campo_embarque.setPlaceholderText("Local de embarque")

        self.campo_destino = QLineEdit()
        self.campo_destino.setPlaceholderText("Local destino da carga")

        self.campo_placa = QComboBox()
        self.campo_placa.addItem(
            "Selecione a placa",
            None,
        )

        self.campo_motorista = QComboBox()
        self.campo_motorista.addItem(
            "Selecione o motorista",
            None,
        )

        self.carregar_motoristas()

        self.carregar_placas()

        self.campo_frete = QLineEdit()
        self.campo_frete.setPlaceholderText("Valor total do frete")

        self.campo_frete.editingFinished.connect(
            lambda: self.campo_frete.setText(
                self.formatar_entrada_moeda(self.campo_frete.text())
            )
        )

        self.campo_frete.editingFinished.connect(self.calcular_saldo)

        self.campo_pedagio = QLineEdit()
        self.campo_pedagio.setPlaceholderText("Valor do pedágio")

        self.campo_pedagio.editingFinished.connect(
            lambda: self.campo_pedagio.setText(
                self.formatar_entrada_moeda(self.campo_pedagio.text())
            )
        )

        self.campo_adiantamento = QLineEdit()
        self.campo_adiantamento.setPlaceholderText("Valor do adiantamento")

        self.campo_adiantamento.editingFinished.connect(
            lambda: self.campo_adiantamento.setText(
                self.formatar_entrada_moeda(self.campo_adiantamento.text())
            )
        )

        self.campo_adiantamento.editingFinished.connect(self.calcular_saldo)

        self.campo_saldo = QLineEdit()
        self.campo_saldo.setPlaceholderText("Saldo recebido após descarga")
        self.campo_saldo.setReadOnly(True)

        self.campo_saldo.editingFinished.connect(
            lambda: self.campo_saldo.setText(
                self.formatar_entrada_moeda(self.campo_saldo.text())
            )
        )

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

        self.campo_status.setCurrentText("Aguardando saldo")

        self.campo_observacao = QLineEdit()
        self.campo_observacao.setPlaceholderText("Observação")

        # ==================================
        # CARD 1 — DADOS DA VIAGEM
        # ==================================
        card_dados = QGroupBox("1. Dados da viagem")
        layout_dados = QGridLayout()
        layout_dados.setHorizontalSpacing(10)
        layout_dados.setVerticalSpacing(8)

        layout_dados.addWidget(QLabel("N° Contrato"), 0, 0)
        layout_dados.addWidget(QLabel("Data"), 0, 1)
        layout_dados.addWidget(self.campo_os, 1, 0)
        layout_dados.addWidget(self.campo_dia, 1, 1)

        layout_dados.addWidget(QLabel("Placa"), 2, 0)
        layout_dados.addWidget(QLabel("Motorista"), 2, 1)
        layout_dados.addWidget(self.campo_placa, 3, 0)
        layout_dados.addWidget(self.campo_motorista, 3, 1)

        layout_dados.addWidget(QLabel("Observação"), 4, 0, 1, 2)
        layout_dados.addWidget(self.campo_observacao, 5, 0, 1, 2)

        layout_dados.setColumnStretch(0, 1)
        layout_dados.setColumnStretch(1, 1)

        card_dados.setLayout(layout_dados)

        # ==================================
        # CARD 2 — CARGA
        # ==================================

        card_carga = QGroupBox("2. Carga")
        layout_carga = QGridLayout()
        layout_carga.setHorizontalSpacing(10)
        layout_carga.setVerticalSpacing(8)

        layout_carga.addWidget(QLabel("Origem"), 0, 0)
        layout_carga.addWidget(QLabel("Destino"), 0, 1)
        layout_carga.addWidget(self.campo_embarque, 1, 0)
        layout_carga.addWidget(self.campo_destino, 1, 1)

        layout_carga.addWidget(QLabel("Transportadora"), 2, 0)
        layout_carga.addWidget(QLabel("Peso da carga (kg)"), 2, 1)
        layout_carga.addWidget(self.campo_transportadora, 3, 0)
        layout_carga.addWidget(self.campo_peso, 3, 1)

        layout_carga.setColumnStretch(0, 1)
        layout_carga.setColumnStretch(1, 1)

        card_carga.setLayout(layout_carga)

        # ==================================
        # CARD 3 — VALORES
        # ==================================

        card_valores = QGroupBox("3. Valores")
        layout_valores = QGridLayout()
        layout_valores.setHorizontalSpacing(10)
        layout_valores.setVerticalSpacing(8)

        layout_valores.addWidget(QLabel("Frete"), 0, 0)
        layout_valores.addWidget(QLabel("Pedágio"), 0, 1)
        layout_valores.addWidget(self.campo_frete, 1, 0)
        layout_valores.addWidget(self.campo_pedagio, 1, 1)

        layout_valores.addWidget(QLabel("Adiantamento"), 2, 0)
        layout_valores.addWidget(QLabel("Saldo"), 2, 1)
        layout_valores.addWidget(self.campo_adiantamento, 3, 0)
        layout_valores.addWidget(self.campo_saldo, 3, 1)

        layout_valores.addWidget(QLabel("Status"), 4, 0, 1, 2)
        layout_valores.addWidget(self.campo_status, 5, 0, 1, 2)

        layout_valores.setColumnStretch(0, 1)
        layout_valores.setColumnStretch(1, 1)

        card_valores.setLayout(layout_valores)

        for card in (card_dados, card_carga, card_valores):
            card.setStyleSheet("""
                QGroupBox {
                    background-color: #ffffff;
                    border: 1px solid #d9dee7;
                    border-radius: 8px;
                    margin-top: 10px;
                    padding: 10px;
                    font-weight: bold;
                }

                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px;
                    color: #1f2937;
                }
            """)

        # ==================================
        # 3 CARDS DENTRO DO CARD MAIOR
        # ==================================

        linha_cards = QHBoxLayout()
        linha_cards.setSpacing(12)
        linha_cards.setContentsMargins(0, 0, 0, 0)

        linha_cards.addWidget(card_dados, 3)
        linha_cards.addWidget(card_carga, 4)
        linha_cards.addWidget(card_valores, 3)

        layout_lancamento.addLayout(linha_cards)

        # ==================================
        # BOTÕES
        # ==================================

        linha_botao = QHBoxLayout()
        linha_botao.addStretch()

        botao_lancar = QPushButton("Lançar frete")
        botao_lancar.setMinimumWidth(140)
        botao_lancar.setMinimumHeight(36)
        botao_lancar.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 7px;
                padding: 8px 18px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #1d4ed8;
            }
        """)

        linha_botao.addWidget(botao_lancar)

        botao_editar = QPushButton("Editar frete")
        botao_editar.setMinimumWidth(140)
        botao_editar.setMinimumHeight(34)
        botao_editar.setStyleSheet("""
            QPushButton {
                background-color: #f3f4f6;
                color: #374151;
                border: 1px solid #d1d5db;
                border-radius: 7px;
                padding: 7px 16px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #e5e7eb;
            }
        """)

        botao_excluir = QPushButton("Excluir frete")
        botao_excluir.setMinimumWidth(140)
        botao_excluir.setMinimumHeight(34)
        botao_excluir.setStyleSheet("""
            QPushButton {
                background-color: #fee2e2;
                color: #b91c1c;
                border: 1px solid #fecaca;
                border-radius: 7px;
                padding: 7px 16px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #fecaca;
            }
        """)

        botao_excluir.clicked.connect(self.excluir_frete)

        layout_lancamento.addLayout(linha_botao)

        caixa_lancamento.setLayout(layout_lancamento)

        # ==================================
        # ABA — GESTÃO DE FRETES
        # ==================================

        aba_gestao = QWidget()
        layout_aba_gestao = QVBoxLayout(aba_gestao)
        layout_aba_gestao.setContentsMargins(5, 5, 5, 5)
        layout_aba_gestao.setSpacing(10)

        layout_aba_gestao.addWidget(caixa_lancamento)

        abas = QTabWidget()

        abas.setDocumentMode(True)
        abas.setUsesScrollButtons(False)
        abas.setMinimumHeight(300)

        abas.setStyleSheet("""
            QTabBar::tab {
                min-width: 180px;
                min-height: 36px;
                padding: 8px 20px;
                font-weight: bold;
            }

            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid #2563eb;
            }

            QTabWidget::pane {
                border: 1px solid #dfe3e8;
                border-radius: 8px;
                background: white;
            }
        """)

        caixa_lancamento.setMaximumHeight(330)

        # ==================================
        # ABA — FRETES LANÇADOS
        # ==================================

        aba_fretes = QWidget()
        layout_aba_fretes = QVBoxLayout(aba_fretes)

        layout_aba_fretes.setContentsMargins(0, 0, 0, 0)

        caixa_fretes = QGroupBox("Fretes Lançados")
        layout_fretes = QVBoxLayout()

        # FILTROS

        linha_filtros = QHBoxLayout()
        linha_filtros.setSpacing(10)

        linha_filtros.addWidget(QLabel("Motorista:"))

        self.filtro_motorista = QComboBox()
        self.filtro_motorista.addItem("Todos", None)
        self.filtro_motorista.currentIndexChanged.connect(self.aplicar_filtros_fretes)
        linha_filtros.addWidget(self.filtro_motorista)

        linha_filtros.addWidget(QLabel("Placa:"))

        self.filtro_placa = QComboBox()
        self.filtro_placa.addItem("Todas", None)
        self.filtro_placa.currentIndexChanged.connect(self.aplicar_filtros_fretes)
        linha_filtros.addWidget(self.filtro_placa)

        linha_filtros.addWidget(QLabel("Data inicial:"))

        self.filtro_fretes_data_inicial = QDateEdit()
        self.filtro_fretes_data_inicial.setCalendarPopup(True)
        self.filtro_fretes_data_inicial.setDate(QDate.currentDate().addDays(-30))
        self.filtro_fretes_data_inicial.dateChanged.connect(self.aplicar_filtros_fretes)
        linha_filtros.addWidget(self.filtro_fretes_data_inicial)

        linha_filtros.addWidget(QLabel("Data final:"))

        self.filtro_fretes_data_final = QDateEdit()
        self.filtro_fretes_data_final.setCalendarPopup(True)
        self.filtro_fretes_data_final.setDate(QDate.currentDate())
        self.filtro_fretes_data_final.dateChanged.connect(self.aplicar_filtros_fretes)
        linha_filtros.addWidget(self.filtro_fretes_data_final)

        botao_limpar_filtros = QPushButton("Limpar filtros")
        botao_limpar_filtros.clicked.connect(self.limpar_filtros_fretes)
        linha_filtros.addWidget(botao_limpar_filtros)
        self.valor_fretes_filtrados = QLabel("Fretes: 0")
        linha_filtros.addWidget(self.valor_fretes_filtrados)

        self.valor_valor_fretes_filtrados = QLabel("Total: R$ 0,00")
        linha_filtros.addWidget(self.valor_valor_fretes_filtrados)

        layout_fretes.addLayout(linha_filtros)

        linha_acoes = QHBoxLayout()
        linha_acoes.addStretch()

        linha_acoes.addWidget(botao_editar)
        linha_acoes.addWidget(botao_excluir)

        layout_fretes.addLayout(linha_acoes)

        # ==================================
        # FILTRO — PERÍODO
        # ==================================

        sessao = SessionLocal()

        try:
            veiculos = (
                sessao.query(Veiculo)
                .filter(Veiculo.status == "Ativo")
                .order_by(Veiculo.placa.asc())
                .all()
            )

            for veiculo in veiculos:
                self.filtro_placa.addItem(veiculo.placa, veiculo.id)

        finally:
            sessao.close()

        self.tabela_fretes = TabelaFretes()
        self.tabela_fretes.setEditTriggers(QTableWidget.NoEditTriggers)

        self.tabela_fretes.setColumnCount(13)

        self.tabela_fretes.setHorizontalHeaderLabels(
            [
                "Dia",
                "N° Contrato",
                "Transportadora",
                "Embarque",
                "Destino",
                "Peso (kg)",
                "Placa",
                "Motorista",
                "Frete",
                "Pedágio",
                "Adiantamento",
                "Saldo",
                "Status",
            ]
        )

        self.tabela_fretes.setAlternatingRowColors(True)

        self.tabela_fretes.setSelectionBehavior(QTableWidget.SelectRows)

        self.tabela_fretes.setSelectionMode(QTableWidget.SingleSelection)

        self.tabela_fretes.setFocusPolicy(Qt.StrongFocus)

        cabecalho = self.tabela_fretes.horizontalHeader()

        cabecalho.setSectionResizeMode(QHeaderView.Interactive)

        self.tabela_fretes.setColumnWidth(0, 100)
        self.tabela_fretes.setColumnWidth(1, 130)
        self.tabela_fretes.setColumnWidth(2, 220)
        self.tabela_fretes.setColumnWidth(3, 180)
        self.tabela_fretes.setColumnWidth(4, 180)
        self.tabela_fretes.setColumnWidth(5, 110)
        self.tabela_fretes.setColumnWidth(6, 110)
        self.tabela_fretes.setColumnWidth(7, 140)
        self.tabela_fretes.setColumnWidth(8, 130)
        self.tabela_fretes.setColumnWidth(9, 120)
        self.tabela_fretes.setColumnWidth(10, 140)
        self.tabela_fretes.setColumnWidth(11, 130)
        self.tabela_fretes.setColumnWidth(12, 180)

        layout_fretes.addWidget(self.tabela_fretes)

        caixa_fretes.setLayout(layout_fretes)

        layout_aba_fretes.addWidget(caixa_fretes)

        abas.addTab(aba_fretes, "Fretes Lançados")

        # ==================================
        # ABA — COMISSÕES
        # ==================================

        aba_comissoes = QWidget()
        layout_aba_comissoes = QVBoxLayout(aba_comissoes)

        layout_aba_comissoes.setContentsMargins(0, 0, 0, 0)

        caixa_comissoes = QGroupBox()

        layout_comissoes = QVBoxLayout()
        layout_comissoes.setContentsMargins(20, 20, 20, 20)
        layout_comissoes.setSpacing(12)

        titulo_comissoes = QLabel("Comissões dos Motoristas")
        titulo_comissoes.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
        """)

        descricao_comissoes = QLabel("Acompanhe as comissões geradas por cada viagem.")
        descricao_comissoes.setStyleSheet("""
            font-size: 13px;
        """)

        layout_comissoes.addWidget(titulo_comissoes)
        layout_comissoes.addWidget(descricao_comissoes)

        linha_filtro_comissao = QHBoxLayout()
        linha_filtro_comissao.setSpacing(10)

        label_filtro_motorista = QLabel("Motorista")
        label_filtro_motorista.setStyleSheet("""
            font-weight: bold;
        """)

        linha_filtro_comissao.addWidget(label_filtro_motorista)

        self.filtro_comissao_motorista = QComboBox()
        self.filtro_comissao_motorista.setMinimumHeight(36)
        self.filtro_comissao_motorista.setMinimumWidth(260)
        self.filtro_comissao_motorista.setStyleSheet("""
            QComboBox {
                border: 1px solid #d6dbe1;
                border-radius: 8px;
                padding: 6px 12px;
                background-color: white;
                font-size: 13px;
            }

            QComboBox:hover {
                border: 1px solid #9aa4b2;
            }

            QComboBox:focus {
                border: 1px solid #6b7280;
            }

            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
        """)
        self.filtro_comissao_motorista.addItem("Todos", None)

        sessao = SessionLocal()
        try:
            motoristas = (
                sessao.query(Motorista)
                .filter(Motorista.status == "Ativo")
                .order_by(Motorista.nome.asc())
                .all()
            )

            for motorista in motoristas:
                self.filtro_comissao_motorista.addItem(motorista.nome, motorista.id)

        finally:
            sessao.close()

        self.filtro_comissao_motorista.currentIndexChanged.connect(
            self.carregar_comissoes
        )

        linha_filtro_comissao.addWidget(self.filtro_comissao_motorista, 1)
        botao_limpar_comissao = QPushButton("Limpar")
        botao_limpar_comissao.setMinimumHeight(36)
        botao_limpar_comissao.setMinimumWidth(100)

        linha_filtro_comissao.addWidget(botao_limpar_comissao)

        layout_comissoes.addLayout(linha_filtro_comissao)
        botao_limpar_comissao.clicked.connect(
            lambda: self.filtro_comissao_motorista.setCurrentIndex(0)
        )

        self.tabela_comissoes = QTableWidget()
        self.tabela_comissoes.setObjectName("tabelaComissoes")
        self.tabela_comissoes.setEditTriggers(QTableWidget.NoEditTriggers)

        self.tabela_comissoes.setColumnCount(7)

        self.tabela_comissoes.setHorizontalHeaderLabels(
            [
                "Dia",
                "N° Contrato",
                "Motorista",
                "Placa",
                "Viagem",
                "Comissão",
                "Observação",
            ]
        )

        self.tabela_comissoes.setAlternatingRowColors(True)
        self.tabela_comissoes.horizontalHeader().setMinimumHeight(40)
        self.tabela_comissoes.verticalHeader().setDefaultSectionSize(36)
        self.tabela_comissoes.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabela_comissoes.setFocusPolicy(Qt.NoFocus)
        self.tabela_comissoes.horizontalHeader().setStretchLastSection(True)
        self.tabela_comissoes.setColumnWidth(0, 100)
        self.tabela_comissoes.setColumnWidth(1, 130)
        self.tabela_comissoes.setColumnWidth(2, 220)
        self.tabela_comissoes.setColumnWidth(3, 110)
        self.tabela_comissoes.setColumnWidth(4, 140)
        self.tabela_comissoes.setColumnWidth(5, 130)
        self.tabela_comissoes.setColumnWidth(6, 250)
        self.tabela_comissoes.setStyleSheet("""
            QTableWidget {
                border: 1px solid #dfe3e8;
                border-radius: 8px;
                gridline-color: #e6e9ed;
                background-color: white;
                alternate-background-color: #f8fafc;
                font-size: 13px;
            }

            QTableWidget::item {
                padding: 6px;
            }

            QTableWidget::item:selected {
                background-color: #e8f0fe;
                color: #1f2937;
            }

            QHeaderView::section {
                background-color: #f1f5f9;
                color: #374151;
                font-weight: bold;
                font-size: 12px;
                padding: 10px;
                border: none;
                border-bottom: 1px solid #dfe3e8;
            }
        """)

        layout_comissoes.addWidget(self.tabela_comissoes)

        caixa_comissoes.setLayout(layout_comissoes)

        layout_aba_comissoes.addWidget(caixa_comissoes)

        abas.addTab(aba_comissoes, "Comissões")

        # ==================================
        # ABA — RESUMO
        # ==================================

        aba_resumo = QWidget()
        layout_aba_resumo = QVBoxLayout(aba_resumo)

        layout_aba_resumo.setContentsMargins(0, 0, 0, 0)

        caixa_resumo = QGroupBox("Resumo dos Fretes")
        layout_resumo = QVBoxLayout()
        layout_resumo.setSpacing(15)

        # ==================================
        # CARDS DO RESUMO
        # ==================================

        linha_cards_resumo = QHBoxLayout()
        linha_cards_resumo.setSpacing(12)

        # TOTAL DE FRETES
        card_total_fretes = QGroupBox()
        layout_card_total_fretes = QVBoxLayout()

        label_total_fretes = QLabel("Total de fretes")
        label_total_fretes.setObjectName("labelResumoTitulo")

        self.valor_total_fretes = QLabel("0")
        self.valor_total_fretes.setObjectName("valorResumo")

        layout_card_total_fretes.addWidget(label_total_fretes)
        layout_card_total_fretes.addWidget(self.valor_total_fretes)

        card_total_fretes.setLayout(layout_card_total_fretes)

        # VALOR TOTAL
        card_total_valor = QGroupBox()
        layout_card_total_valor = QVBoxLayout()

        label_total_valor = QLabel("Valor total dos fretes")
        label_total_valor.setObjectName("labelResumoTitulo")

        self.valor_total_valor = QLabel("R$ 0,00")
        self.valor_total_valor.setObjectName("valorResumo")

        layout_card_total_valor.addWidget(label_total_valor)
        layout_card_total_valor.addWidget(self.valor_total_valor)

        card_total_valor.setLayout(layout_card_total_valor)

        # TOTAL DE PEDÁGIOS
        card_total_pedagio = QGroupBox()
        layout_card_total_pedagio = QVBoxLayout()

        label_total_pedagio = QLabel("Total de pedágios")
        label_total_pedagio.setObjectName("labelResumoTitulo")

        self.valor_total_pedagio = QLabel("R$ 0,00")
        self.valor_total_pedagio.setObjectName("valorResumo")

        layout_card_total_pedagio.addWidget(label_total_pedagio)
        layout_card_total_pedagio.addWidget(self.valor_total_pedagio)

        card_total_pedagio.setLayout(layout_card_total_pedagio)

        linha_cards_resumo.addWidget(card_total_fretes)

        linha_cards_resumo.addWidget(card_total_valor)

        linha_cards_resumo.addWidget(card_total_pedagio)

        # TOTAL DE COMISSÕES

        card_total_comissao = QGroupBox()
        layout_card_total_comissao = QVBoxLayout()

        label_total_comissao = QLabel("Total de comissões")
        label_total_comissao.setObjectName("labelResumoTitulo")

        self.valor_total_comissao = QLabel("R$ 0,00")
        self.valor_total_comissao.setObjectName("valorResumo")

        layout_card_total_comissao.addWidget(label_total_comissao)
        layout_card_total_comissao.addWidget(self.valor_total_comissao)

        card_total_comissao.setLayout(layout_card_total_comissao)

        linha_cards_resumo.addWidget(card_total_comissao)

        layout_resumo.addLayout(linha_cards_resumo)

        # ==================================
        # FILTRO DE PERÍODO
        # ==================================

        linha_periodo = QHBoxLayout()

        linha_periodo.addWidget(QLabel("Data inicial"))

        self.filtro_data_inicial = QDateEdit()
        self.filtro_data_inicial.setCalendarPopup(True)
        self.filtro_data_inicial.setDate(QDate.currentDate().addDays(-30))

        linha_periodo.addWidget(self.filtro_data_inicial)

        linha_periodo.addWidget(QLabel("Data final"))

        self.filtro_data_final = QDateEdit()
        self.filtro_data_final.setCalendarPopup(True)
        self.filtro_data_final.setDate(QDate.currentDate())

        linha_periodo.addWidget(self.filtro_data_final)

        botao_limpar_filtro = QPushButton("Limpar filtros")
        botao_limpar_filtro.clicked.connect(self.limpar_filtro_resumo)

        linha_periodo.addWidget(botao_limpar_filtro)

        layout_resumo.insertLayout(0, linha_periodo)

        caixa_resumo.setLayout(layout_resumo)

        layout_aba_resumo.addWidget(caixa_resumo)

        abas.addTab(aba_resumo, "Resumo")

        layout_aba_gestao.addWidget(abas)

        layout_aba_gestao.setStretch(0, 0)
        layout_aba_gestao.setStretch(1, 1)

        layout_principal.addWidget(aba_gestao, 1)
        self.setLayout(layout_principal)

        # ==================================
        # EVENTOS
        # ==================================

        botao_lancar.clicked.connect(self.lancar_frete)

        botao_editar.clicked.connect(self.editar_frete)

        # ==================================
        # CARREGAMENTO INICIAL
        # ==================================

        self.carregar_fretes()
        self.aplicar_filtros_fretes()
        self.carregar_comissoes()
        self.carregar_resumo()
        self.filtro_data_inicial.dateChanged.connect(self.carregar_resumo)
        self.filtro_data_final.dateChanged.connect(self.carregar_resumo)

    # ======================================
    # PLACAS
    # ======================================

    def carregar_placas(self):
        sessao = SessionLocal()

        try:
            veiculos = (
                sessao.query(Veiculo)
                .filter(Veiculo.status == "Ativo")
                .order_by(Veiculo.placa.asc())
                .all()
            )

            for veiculo in veiculos:
                self.campo_placa.addItem(
                    veiculo.placa,
                    veiculo.id,
                )

        finally:
            sessao.close()

    # ======================================
    # MOTORISTAS
    # ======================================

    def carregar_motoristas(self):
        sessao = SessionLocal()

        try:
            motoristas = (
                sessao.query(Motorista)
                .filter(Motorista.status == "Ativo")
                .order_by(Motorista.nome.asc())
                .all()
            )

            for motorista in motoristas:
                self.campo_motorista.addItem(
                    motorista.nome,
                    motorista.id,
                )

        finally:
            sessao.close()

    # ======================================
    # CONVERTER VALOR
    # ======================================

    def converter_valor(self, texto):
        texto = texto.strip()

        if not texto:
            return 0.0

        texto = texto.replace(
            "R$",
            "",
        ).strip()

        texto = texto.replace(
            ".",
            "",
        )

        texto = texto.replace(
            ",",
            ".",
        )

        return float(texto)

    # ======================================
    # FORMATAR ENTRADA DE MOEDA
    # ======================================

    def formatar_entrada_moeda(self, texto):
        texto = texto.replace("R$", "").strip()

        if not texto:
            return ""

        try:
            valor = float(texto.replace(".", "").replace(",", "."))
        except ValueError:
            return texto

        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def calcular_saldo(self):
        try:
            valor_frete = self.converter_valor(self.campo_frete.text())
            adiantamento = self.converter_valor(self.campo_adiantamento.text())

            saldo = valor_frete - adiantamento

            if saldo < 0:
                saldo = 0

            self.campo_saldo.setText(self.formatar_moeda(saldo))

        except ValueError:
            self.campo_saldo.clear()

    # ======================================
    # LANÇAR FRETE
    # ======================================

    def lancar_frete(self):
        try:
            ordem_servico = self.campo_os.text().strip()

            transportadora = self.campo_transportadora.text().strip()

            embarque = self.campo_embarque.text().strip()

            destino = self.campo_destino.text().strip()

            peso = None

            texto_peso = self.campo_peso.text().strip()

            if texto_peso:
                texto_peso = texto_peso.replace(".", "").replace(",", ".")
                peso = Decimal(texto_peso)

                if peso <= 0:
                    QMessageBox.warning(
                        self,
                        "Peso inválido",
                        "Informe um peso maior que zero.",
                    )
                    return

            veiculo_id = self.campo_placa.currentData()

            motorista_id = self.campo_motorista.currentData()

            valor_frete = self.converter_valor(self.campo_frete.text())

            pedagio = self.converter_valor(self.campo_pedagio.text())

            if pedagio > valor_frete:
                QMessageBox.warning(
                    self,
                    "Valor inválido",
                    "O pedágio não pode ser maior que o valor do frete.",
                )
                return

            adiantamento = self.converter_valor(self.campo_adiantamento.text())

            if adiantamento > valor_frete:
                QMessageBox.warning(
                    self,
                    "Valor inválido",
                    "O adiantamento não pode ser maior que o valor do frete.",
                )
                return

            saldo = valor_frete - adiantamento

            if saldo < 0:
                saldo = 0

            if not ordem_servico:
                QMessageBox.warning(
                    self,
                    "Campo obrigatório",
                    "Informe o número da OS.",
                )
                return

            if not transportadora:
                QMessageBox.warning(
                    self,
                    "Campo obrigatório",
                    "Informe a transportadora.",
                )
                return

            if not embarque:
                QMessageBox.warning(
                    self,
                    "Campo obrigatório",
                    "Informe o local de embarque.",
                )
                return

            if not destino:
                QMessageBox.warning(
                    self,
                    "Campo obrigatório",
                    "Informe o local de destino.",
                )
                return

            if veiculo_id is None:
                QMessageBox.warning(
                    self,
                    "Campo obrigatório",
                    "Selecione a placa do caminhão.",
                )
                return

            if motorista_id is None:
                QMessageBox.warning(
                    self,
                    "Campo obrigatório",
                    "Selecione o motorista.",
                )
                return

            if valor_frete <= 0:
                QMessageBox.warning(
                    self,
                    "Valor inválido",
                    "Informe um valor de frete maior que zero.",
                )
                return

            confirmacao = QMessageBox.question(
                self,
                "Confirmar lançamento",
                "Deseja realmente lançar este frete?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )

            if confirmacao == QMessageBox.No:
                return

            sessao = SessionLocal()

            try:
                frete = Frete(
                    dia=self.campo_dia.date().toPython(),
                    ordem_servico=ordem_servico,
                    transportadora=transportadora,
                    embarque=embarque,
                    destino=destino,
                    peso=peso,
                    veiculo_id=veiculo_id,
                    motorista_id=motorista_id,
                    valor_frete=valor_frete,
                    pedagio=pedagio,
                    adiantamento=adiantamento,
                    saldo=saldo,
                    status=self.campo_status.currentText(),
                    observacao=self.campo_observacao.text().strip(),
                )

                sessao.add(frete)
                sessao.commit()
                sessao.refresh(frete)
                sessao.expunge(frete)

            except Exception:
                sessao.rollback()
                raise

            finally:
                sessao.close()

            QMessageBox.information(
                self,
                "Frete lançado",
                "Frete lançado com sucesso!",
            )

            self.carregar_fretes()
            self.carregar_comissoes()
            self.carregar_resumo()
            self.limpar_lancamento()

        except ValueError:
            QMessageBox.warning(
                self,
                "Valor inválido",
                "Confira os valores de frete, pedágio, adiantamento e saldo.",
            )

        except Exception as erro:
            QMessageBox.critical(
                self,
                "Erro ao lançar frete",
                f"Não foi possível lançar o frete:\n\n{erro}",
            )

    # ======================================
    # CARREGAR FRETES
    # ======================================

    def carregar_fretes(self):
        sessao = SessionLocal()

        try:
            fretes = (
                sessao.query(Frete, Veiculo.placa, Motorista.nome)
                .join(
                    Veiculo,
                    Frete.veiculo_id == Veiculo.id,
                )
                .join(
                    Motorista,
                    Frete.motorista_id == Motorista.id,
                )
                .order_by(Frete.id.asc())
                .all()
            )

            self.tabela_fretes.setRowCount(len(fretes))

            # Guarda a seleção atual antes de reconstruir os filtros.
            motorista_atual = self.filtro_motorista.currentData()
            placa_atual = self.filtro_placa.currentData()

            self.filtro_motorista.blockSignals(True)
            self.filtro_placa.blockSignals(True)

            self.filtro_motorista.clear()
            self.filtro_motorista.addItem("Todos", None)

            self.filtro_placa.clear()
            self.filtro_placa.addItem("Todas", None)
            motoristas = (
                sessao.query(Motorista)
                .filter(Motorista.status == "Ativo")
                .order_by(Motorista.nome.asc())
                .all()
            )

            placas = (
                sessao.query(Veiculo)
                .filter(Veiculo.status == "Ativo")
                .order_by(Veiculo.placa.asc())
                .all()
            )

            for motorista in motoristas:
                self.filtro_motorista.addItem(motorista.nome, motorista.id)

            for veiculo in placas:
                self.filtro_placa.addItem(veiculo.placa, veiculo.id)

            if motorista_atual is not None:
                indice = self.filtro_motorista.findData(motorista_atual)
                if indice >= 0:
                    self.filtro_motorista.setCurrentIndex(indice)

            if placa_atual is not None:
                indice = self.filtro_placa.findData(placa_atual)
                if indice >= 0:
                    self.filtro_placa.setCurrentIndex(indice)

            self.filtro_motorista.blockSignals(False)
            self.filtro_placa.blockSignals(False)

            for linha, resultado in enumerate(fretes):
                frete, placa, motorista = resultado

                dados = [
                    frete.dia.strftime("%d/%m/%Y"),
                    frete.ordem_servico,
                    frete.transportadora,
                    frete.embarque,
                    frete.destino,
                    (
                        ""
                        if frete.peso is None
                        else f"{float(frete.peso):,.2f}".replace(",", "X")
                        .replace(".", ",")
                        .replace("X", ".")
                    ),
                    placa,
                    motorista,
                    self.formatar_moeda(frete.valor_frete),
                    self.formatar_moeda(frete.pedagio),
                    self.formatar_moeda(frete.adiantamento),
                    ("" if frete.saldo is None else self.formatar_moeda(frete.saldo)),
                    frete.status,
                ]

                for coluna, valor in enumerate(dados):
                    item = QTableWidgetItem(str(valor))

                    if coluna == 0:
                        item.setData(
                            Qt.UserRole,
                            frete.id,
                        )

                    self.tabela_fretes.setItem(
                        linha,
                        coluna,
                        item,
                    )

                self.tabela_fretes.item(linha, 6).setData(
                    Qt.UserRole + 1, frete.veiculo_id
                )
                self.tabela_fretes.item(linha, 7).setData(
                    Qt.UserRole + 1, frete.motorista_id
                )

        finally:
            sessao.close()

    def limpar_filtros_fretes(self):
        self.filtro_motorista.setCurrentIndex(0)
        self.filtro_placa.setCurrentIndex(0)
        self.filtro_fretes_data_inicial.setDate(QDate.currentDate().addDays(-30))
        self.filtro_fretes_data_final.setDate(QDate.currentDate())

        self.aplicar_filtros_fretes()

    def aplicar_filtros_fretes(self):
        motorista_id = self.filtro_motorista.currentData()
        veiculo_id = self.filtro_placa.currentData()

        data_inicial = self.filtro_fretes_data_inicial.date().toPython()
        data_final = self.filtro_fretes_data_final.date().toPython()

        total_visiveis = 0
        total_filtrado = Decimal("0")

        for linha in range(self.tabela_fretes.rowCount()):
            item_data = self.tabela_fretes.item(linha, 0)
            item_placa = self.tabela_fretes.item(linha, 6)
            item_motorista = self.tabela_fretes.item(linha, 7)
            item_frete = self.tabela_fretes.item(linha, 8)

            if not item_data or not item_placa or not item_motorista:
                continue

            linha_veiculo_id = item_placa.data(Qt.UserRole + 1)
            linha_motorista_id = item_motorista.data(Qt.UserRole + 1)

            data_linha = QDate.fromString(
                item_data.text(),
                "dd/MM/yyyy",
            ).toPython()

            mostrar = (
                (motorista_id is None or linha_motorista_id == motorista_id)
                and (veiculo_id is None or linha_veiculo_id == veiculo_id)
                and (data_inicial <= data_linha <= data_final)
            )

            self.tabela_fretes.setRowHidden(
                linha,
                not mostrar,
            )

            if mostrar:
                total_visiveis += 1

                if item_frete:
                    valor = (
                        item_frete.text()
                        .replace("R$", "")
                        .replace(".", "")
                        .replace(",", ".")
                        .strip()
                    )

                    try:
                        total_filtrado += Decimal(valor)
                    except Exception:
                        pass

        self.valor_fretes_filtrados.setText(f"Fretes: {total_visiveis}")

        self.valor_valor_fretes_filtrados.setText(
            f"Total: {self.formatar_moeda(total_filtrado)}"
        )

    def limpar_filtro_resumo(self):
        self.filtro_data_inicial.setDate(QDate.currentDate().addDays(-30))
        self.filtro_data_final.setDate(QDate.currentDate())
        self.carregar_resumo()

    def carregar_resumo(self):
        sessao = SessionLocal()

        try:
            fretes = (
                sessao.query(Frete)
                .filter(
                    Frete.dia >= self.filtro_data_inicial.date().toPython(),
                    Frete.dia <= self.filtro_data_final.date().toPython(),
                )
                .all()
            )

            total_fretes = len(fretes)

            total_valor = sum((frete.valor_frete or Decimal("0")) for frete in fretes)

            total_pedagio = sum((frete.pedagio or Decimal("0")) for frete in fretes)

            total_comissao = sum(
                ((frete.valor_frete or Decimal("0")) - (frete.pedagio or Decimal("0")))
                * Decimal("0.11")
                for frete in fretes
            )

            self.valor_total_fretes.setText(str(total_fretes))

            self.valor_total_valor.setText(self.formatar_moeda(total_valor))

            self.valor_total_pedagio.setText(self.formatar_moeda(total_pedagio))

            self.valor_total_comissao.setText(self.formatar_moeda(total_comissao))

        finally:
            sessao.close()

    def carregar_comissoes(self):
        motorista_id = self.filtro_comissao_motorista.currentData()
        sessao = SessionLocal()

        try:
            fretes = (
                sessao.query(Frete, Veiculo.placa, Motorista.nome)
                .join(Veiculo, Frete.veiculo_id == Veiculo.id)
                .join(Motorista, Frete.motorista_id == Motorista.id)
            )

            if motorista_id is not None:
                fretes = fretes.filter(Frete.motorista_id == motorista_id)

            fretes = fretes.order_by(Frete.id.asc()).all()

            self.tabela_comissoes.setRowCount(len(fretes))

            for linha, resultado in enumerate(fretes):
                frete, placa, motorista = resultado
                valor_viagem = f"{frete.embarque} → {frete.destino}"
                valor_base_comissao = frete.valor_frete - frete.pedagio
                valor_comissao = valor_base_comissao * Decimal("0.11")

                dados = [
                    frete.dia.strftime("%d/%m/%Y"),
                    frete.ordem_servico,
                    motorista,
                    placa,
                    valor_viagem,
                    valor_comissao,
                    frete.observacao or "",
                ]

                for coluna, valor in enumerate(dados):
                    if coluna == 5:
                        valor = self.formatar_moeda(valor)

                    item = QTableWidgetItem(str(valor))

                    if coluna in [0, 1, 3]:
                        item.setTextAlignment(Qt.AlignCenter)

                    elif coluna == 5:
                        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

                    self.tabela_comissoes.setItem(linha, coluna, item)

        finally:
            sessao.close()

    def excluir_frete(self):
        linha = self.tabela_fretes.currentRow()

        if linha < 0:
            QMessageBox.warning(
                self,
                "Nenhum frete selecionado",
                "Selecione um frete para excluir.",
            )
            return

        item = self.tabela_fretes.item(linha, 0)

        if not item:
            return

        id_frete = item.data(Qt.UserRole)

        confirmacao = QMessageBox.question(
            self,
            "Confirmar exclusão",
            "Deseja realmente excluir este frete?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if confirmacao == QMessageBox.No:
            return

        sessao = SessionLocal()

        try:
            frete = sessao.query(Frete).filter(Frete.id == id_frete).first()

            if not frete:
                QMessageBox.warning(
                    self,
                    "Frete não encontrado",
                    "O frete selecionado não foi encontrado no banco.",
                )
                return

            sessao.delete(frete)
            sessao.commit()

        finally:
            sessao.close()

        QMessageBox.information(
            self,
            "Frete excluído",
            "Frete excluído com sucesso!",
        )

        self.carregar_fretes()
        self.carregar_comissoes()
        self.carregar_resumo()

    def editar_frete(self):
        linha = self.tabela_fretes.currentRow()

        if linha < 0:
            QMessageBox.warning(
                self,
                "Nenhum frete selecionado",
                "Selecione um frete para editar.",
            )
            return

        item = self.tabela_fretes.item(
            linha,
            0,
        )

        if not item:
            return

        id_frete = item.data(Qt.UserRole)

        sessao = SessionLocal()

        try:
            frete = sessao.query(Frete).filter(Frete.id == id_frete).first()

            if not frete:
                QMessageBox.warning(
                    self,
                    "Frete não encontrado",
                    "O frete selecionado não foi encontrado no banco.",
                )
                return

            janela = EdicaoFrete(
                frete=frete,
                parent=self,
            )

            if janela.exec():
                self.carregar_fretes()
                self.carregar_comissoes()
                self.carregar_resumo()

        finally:
            sessao.close()

    # ======================================
    # FORMATAR MOEDA
    # ======================================

    def formatar_moeda(self, valor):
        return (
            f"R$ {float(valor):,.2f}".replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

    # ======================================
    # LIMPAR LANÇAMENTO
    # ======================================

    def limpar_lancamento(self):
        self.campo_os.clear()
        self.campo_transportadora.clear()
        self.campo_embarque.clear()
        self.campo_destino.clear()

        self.campo_placa.setCurrentIndex(0)
        self.campo_motorista.setCurrentIndex(0)

        self.campo_frete.clear()
        self.campo_pedagio.clear()
        self.campo_adiantamento.clear()
        self.campo_saldo.clear()
        self.campo_observacao.clear()

        self.campo_status.setCurrentText("Aguardando saldo")
