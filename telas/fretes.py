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
)

from PySide6.QtCore import QDate, Qt
from PySide6.QtGui import QKeyEvent

from banco.sessao import SessionLocal
from banco.modelos import Frete, Veiculo


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

        self.campo_placa = QComboBox()
        self.campo_placa.addItem(
            "Selecione a placa",
            None,
        )

        self.carregar_placas()

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
        self.campo_saldo.setPlaceholderText("Saldo recebido após descarga")

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

        # Deixa o fluxo mais natural para lançamento inicial.
        self.campo_status.setCurrentText("Aguardando saldo")

        linha_3.addWidget(QLabel("Frete"))
        linha_3.addWidget(self.campo_frete)

        linha_3.addWidget(QLabel("Pedágio"))
        linha_3.addWidget(self.campo_pedagio)

        linha_3.addWidget(QLabel("Adiantamento"))
        linha_3.addWidget(self.campo_adiantamento)

        linha_3.addWidget(QLabel("Saldo"))
        linha_3.addWidget(self.campo_saldo)

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
        self.tabela_fretes.setColumnWidth(10, 190)

        layout_fretes.addWidget(self.tabela_fretes)

        caixa_fretes.setLayout(layout_fretes)

        layout_principal.addWidget(
            caixa_fretes,
            1,
        )

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

        layout_principal.addWidget(
            caixa_comissoes,
            1,
        )

        self.setLayout(layout_principal)

        # ==================================
        # EVENTOS
        # ==================================

        botao_lancar.clicked.connect(self.lancar_frete)

        # ==================================
        # CARREGAMENTO INICIAL
        # ==================================

        self.carregar_fretes()

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
    # LANÇAR FRETE
    # ======================================

    def lancar_frete(self):
        try:
            ordem_servico = self.campo_os.text().strip()

            transportadora = self.campo_transportadora.text().strip()

            embarque = self.campo_embarque.text().strip()

            destino = self.campo_destino.text().strip()

            veiculo_id = self.campo_placa.currentData()

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
                    valor_frete=valor_frete,
                    pedagio=pedagio,
                    adiantamento=adiantamento,
                    saldo=saldo,
                    status=self.campo_status.currentText(),
                )

                sessao.add(frete)
                sessao.commit()

            except Exception:
                sessao.rollback()
                raise

            finally:
                sessao.close()

            self.carregar_fretes()
            self.limpar_lancamento()

            QMessageBox.information(
                self,
                "Frete lançado",
                "Frete lançado com sucesso.",
            )

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
                sessao.query(Frete, Veiculo.placa)
                .join(
                    Veiculo,
                    Frete.veiculo_id == Veiculo.id,
                )
                .order_by(Frete.id.asc())
                .all()
            )

            self.tabela_fretes.setRowCount(len(fretes))

            for linha, resultado in enumerate(fretes):
                frete, placa = resultado

                dados = [
                    frete.dia.strftime("%d/%m/%Y"),
                    frete.ordem_servico,
                    frete.transportadora,
                    frete.embarque,
                    frete.destino,
                    placa,
                    self.formatar_moeda(frete.valor_frete),
                    self.formatar_moeda(frete.pedagio),
                    self.formatar_moeda(frete.adiantamento),
                    ("" if frete.saldo is None else self.formatar_moeda(frete.saldo)),
                    frete.status,
                ]

                for coluna, valor in enumerate(dados):
                    item = QTableWidgetItem(str(valor))

                    self.tabela_fretes.setItem(
                        linha,
                        coluna,
                        item,
                    )

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

        self.campo_frete.clear()
        self.campo_pedagio.clear()
        self.campo_adiantamento.clear()
        self.campo_saldo.clear()

        self.campo_status.setCurrentText("Aguardando saldo")
