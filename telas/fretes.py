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

        self.campo_saldo = QLineEdit()
        self.campo_saldo.setPlaceholderText("Saldo recebido após descarga")

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

        # ==================================
        # CARD 1 — DADOS DA VIAGEM
        # ==================================

        card_dados = QGroupBox("Dados da viagem")
        layout_dados = QVBoxLayout()
        layout_dados.setSpacing(8)

        layout_dados.addWidget(QLabel("Nº Contrato"))
        layout_dados.addWidget(self.campo_os)

        layout_dados.addWidget(QLabel("Data"))
        layout_dados.addWidget(self.campo_dia)

        layout_dados.addWidget(QLabel("Placa"))
        layout_dados.addWidget(self.campo_placa)

        layout_dados.addWidget(QLabel("Motorista"))
        layout_dados.addWidget(self.campo_motorista)

        card_dados.setLayout(layout_dados)

        # ==================================
        # CARD 2 — CARGA
        # ==================================

        card_carga = QGroupBox("Carga")
        layout_carga = QVBoxLayout()
        layout_carga.setSpacing(8)

        layout_carga.addWidget(QLabel("Embarque"))
        layout_carga.addWidget(self.campo_embarque)

        layout_carga.addWidget(QLabel("Destino"))
        layout_carga.addWidget(self.campo_destino)

        layout_carga.addWidget(QLabel("Transportadora"))
        layout_carga.addWidget(self.campo_transportadora)

        card_carga.setLayout(layout_carga)

        # ==================================
        # CARD 3 — VALORES
        # ==================================

        card_valores = QGroupBox("Valores")
        layout_valores = QVBoxLayout()
        layout_valores.setSpacing(8)

        layout_valores.addWidget(QLabel("Frete"))
        layout_valores.addWidget(self.campo_frete)

        layout_valores.addWidget(QLabel("Pedágio"))
        layout_valores.addWidget(self.campo_pedagio)

        layout_valores.addWidget(QLabel("Adiantamento"))
        layout_valores.addWidget(self.campo_adiantamento)

        layout_valores.addWidget(QLabel("Saldo"))
        layout_valores.addWidget(self.campo_saldo)

        layout_valores.addWidget(QLabel("Status"))
        layout_valores.addWidget(self.campo_status)

        card_valores.setLayout(layout_valores)

        # ==================================
        # 3 CARDS DENTRO DO CARD MAIOR
        # ==================================

        linha_cards = QHBoxLayout()
        linha_cards.setSpacing(12)

        linha_cards.addWidget(card_dados, 1)
        linha_cards.addWidget(card_carga, 1)
        linha_cards.addWidget(card_valores, 1)

        layout_lancamento.addLayout(linha_cards)

        # ==================================
        # BOTÕES
        # ==================================

        linha_botao = QHBoxLayout()
        linha_botao.addStretch()

        botao_lancar = QPushButton("Lançar frete")
        botao_lancar.setMinimumWidth(140)

        linha_botao.addWidget(botao_lancar)

        botao_editar = QPushButton("Editar frete")
        botao_editar.setMinimumWidth(140)

        layout_lancamento.addLayout(linha_botao)

        caixa_lancamento.setLayout(layout_lancamento)

        # ==================================
        # ABAS PRINCIPAIS
        # ==================================

        abas_principais = QTabWidget()

        # ==================================
        # ABA — LANÇAR FRETE
        # ==================================

        aba_lancamento = QWidget()
        layout_aba_lancamento = QVBoxLayout(aba_lancamento)
        layout_aba_lancamento.setContentsMargins(5, 5, 5, 5)
        layout_aba_lancamento.addWidget(caixa_lancamento)

        abas_principais.addTab(aba_lancamento, "Lançar Frete")

        # ==================================
        # ABA — GESTÃO DE FRETES
        # ==================================

        aba_gestao = QWidget()
        layout_aba_gestao = QVBoxLayout(aba_gestao)
        layout_aba_gestao.setContentsMargins(5, 5, 5, 5)

        abas = QTabWidget()

        # ==================================
        # ABA — FRETES LANÇADOS
        # ==================================

        aba_fretes = QWidget()
        layout_aba_fretes = QVBoxLayout(aba_fretes)

        layout_aba_fretes.setContentsMargins(0, 0, 0, 0)

        caixa_fretes = QGroupBox("Fretes Lançados")
        layout_fretes = QVBoxLayout()

        # ==================================
        # FILTROS — MOTORISTA E PLACA
        # ==================================

        linha_filtros = QHBoxLayout()

        linha_filtros.addWidget(QLabel("Motorista:"))

        self.filtro_motorista = QComboBox()
        self.filtro_motorista.addItem("Todos", None)
        self.filtro_motorista.currentIndexChanged.connect(self.aplicar_filtros_fretes)
        linha_filtros.addWidget(self.filtro_motorista, 1)

        linha_filtros.addWidget(QLabel("Placa:"))

        self.filtro_placa = QComboBox()
        self.filtro_placa.addItem("Todas", None)
        self.filtro_placa.currentIndexChanged.connect(self.aplicar_filtros_fretes)
        linha_filtros.addWidget(self.filtro_placa, 1)

        layout_fretes.addLayout(linha_filtros)
        layout_fretes.addWidget(botao_editar)
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
        self.tabela_fretes.setColumnWidth(6, 130)
        self.tabela_fretes.setColumnWidth(7, 120)
        self.tabela_fretes.setColumnWidth(8, 150)
        self.tabela_fretes.setColumnWidth(9, 130)
        self.tabela_fretes.setColumnWidth(10, 130)
        self.tabela_fretes.setColumnWidth(11, 190)

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

        label_resumo = QLabel("Resumo dos fretes")

        layout_resumo.addWidget(label_resumo)
        layout_resumo.addStretch()

        caixa_resumo.setLayout(layout_resumo)

        layout_aba_resumo.addWidget(caixa_resumo)

        abas.addTab(aba_resumo, "Resumo")

        layout_aba_gestao.addWidget(abas)

        abas_principais.addTab(aba_gestao, "Gestão de Fretes")
        layout_principal.addWidget(abas_principais, 1)
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
        self.carregar_comissoes()

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

    # ======================================
    # LANÇAR FRETE
    # ======================================

    def lancar_frete(self):
        try:
            ordem_servico = self.campo_os.text().strip()

            transportadora = self.campo_transportadora.text().strip()

            embarque = self.campo_embarque.text().strip()

            destino = self.campo_destino.text().strip()

            veiculo_id = self.campo_placa.currentData()

            motorista_id = self.campo_motorista.currentData()

            valor_frete = self.converter_valor(self.campo_frete.text())

            pedagio = self.converter_valor(self.campo_pedagio.text())

            adiantamento = self.converter_valor(self.campo_adiantamento.text())

            saldo_texto = self.campo_saldo.text().strip()

            if saldo_texto:
                saldo = self.converter_valor(saldo_texto)
            else:
                saldo = None

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

            sessao = SessionLocal()

            try:
                frete = Frete(
                    dia=self.campo_dia.date().toPython(),
                    ordem_servico=ordem_servico,
                    transportadora=transportadora,
                    embarque=embarque,
                    destino=destino,
                    veiculo_id=veiculo_id,
                    motorista_id=motorista_id,
                    valor_frete=valor_frete,
                    pedagio=pedagio,
                    adiantamento=adiantamento,
                    saldo=saldo,
                    status=self.campo_status.currentText(),
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

            self.carregar_fretes()
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
            veiculos = (
                SessionLocal()
                .query(Veiculo)
                .filter(Veiculo.status == "Ativo")
                .order_by(Veiculo.placa.asc())
                .all()
            )

            for veiculo in veiculos:
                self.filtro_placa.addItem(veiculo.placa, veiculo.id)

            # Puxa diretamente do cadastro de motoristas e veículos ativos.
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

                self.tabela_fretes.item(5 and linha, 5).setData(
                    Qt.UserRole + 1, frete.veiculo_id
                )
                self.tabela_fretes.item(linha, 6).setData(
                    Qt.UserRole + 1, frete.motorista_id
                )

        finally:
            sessao.close()

    def aplicar_filtros_fretes(self):
        motorista_id = self.filtro_motorista.currentData()
        veiculo_id = self.filtro_placa.currentData()

        for linha in range(self.tabela_fretes.rowCount()):
            item_placa = self.tabela_fretes.item(linha, 5)
            item_motorista = self.tabela_fretes.item(linha, 6)

            if not item_placa or not item_motorista:
                continue

            linha_veiculo_id = item_placa.data(Qt.UserRole + 1)
            linha_motorista_id = item_motorista.data(Qt.UserRole + 1)

            mostrar = (motorista_id is None or linha_motorista_id == motorista_id) and (
                veiculo_id is None or linha_veiculo_id == veiculo_id
            )

            self.tabela_fretes.setRowHidden(linha, not mostrar)

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

        self.campo_status.setCurrentText("Aguardando saldo")
