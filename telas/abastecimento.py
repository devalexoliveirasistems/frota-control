from decimal import Decimal

from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QGroupBox,
    QTabWidget,
    QLabel,
    QComboBox,
    QLineEdit,
    QDateEdit,
    QAbstractSpinBox,
    QSpinBox,
    QDoubleSpinBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
)

from banco.sessao import SessionLocal
from banco.modelos import Abastecimento, Veiculo, Motorista


class TelaAbastecimento(QWidget):
    def __init__(self):
        super().__init__()

        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(16, 16, 16, 16)
        layout_principal.setSpacing(14)

        titulo = QLabel("Abastecimento")
        titulo.setStyleSheet("""
            QLabel {
                color: #0f172a;
                font-size: 26px;
                font-weight: 700;
                padding: 0 0 8px 10px;
                border-left: 5px solid #2563eb;
            }
        """)

        descricao = QLabel(
            "Registre abastecimentos e acompanhe os gastos com combustível da frota."
        )
        descricao.setStyleSheet("""
            QLabel {
                color: #334155;
                font-size: 14px;
            }
        """)

        layout_principal.addWidget(titulo)
        layout_principal.addWidget(descricao)

        # ABAS DO MODULO
        self.abas = QTabWidget()
        self.abas.setStyleSheet("""
            QTabWidget::pane {
                background-color: #ffffff;
                border: 1px solid #d9dee7;
                border-radius: 8px;
                top: -1px;
            }

            QTabBar::tab {
                background-color: #f1f5f9;
                color: #475569;
                border: 1px solid #d9dee7;
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                padding: 12px 26px;
                margin-right: 5px;
                font-size: 15px;
                font-weight: 600;
                min-width: 110px;
            }

            QTabBar::tab:hover {
                background-color: #dbeafe;
                color: #1d4ed8;
            }

            QTabBar::tab:selected {
                background-color: #ffffff;
                color: #1d4ed8;
                border-top: 3px solid #2563eb;
                font-weight: 700;
            }
        """)

        self.aba_lancamento = QWidget()
        self.layout_lancamento = QVBoxLayout(self.aba_lancamento)
        self.layout_lancamento.setContentsMargins(10, 10, 10, 10)
        self.layout_lancamento.setSpacing(14)

        self.aba_historico = QWidget()
        self.layout_historico = QVBoxLayout(self.aba_historico)
        self.layout_historico.setContentsMargins(10, 10, 10, 10)
        self.layout_historico.setSpacing(14)

        self.abas.addTab(
            self.aba_lancamento,
            "Lançamento",
        )
        self.abas.addTab(
            self.aba_historico,
            "Histórico",
        )

        layout_principal.addWidget(self.abas, 1)

        # FORMULARIO
        grupo = QGroupBox("Dados do abastecimento")
        grade = QGridLayout(grupo)
        grade.setContentsMargins(14, 18, 14, 14)
        grade.setHorizontalSpacing(12)
        grade.setVerticalSpacing(10)

        self.campo_data = QDateEdit()
        self.campo_data.setDate(QDate.currentDate())
        self.campo_data.setCalendarPopup(True)
        self.campo_data.setDisplayFormat("dd/MM/yyyy")

        self.campo_veiculo = QComboBox()
        self.campo_motorista = QComboBox()

        self.campo_combustivel = QComboBox()
        self.campo_combustivel.addItems(
            [
                "Diesel S-10",
                "Diesel S-500",
                "Gasolina comum",
                "Gasolina aditivada",
                "Etanol",
                "GNV",
                "Biodiesel",
                "Outro",
            ]
        )

        self.campo_posto = QLineEdit()
        self.campo_posto.setPlaceholderText("Nome do posto")

        self.campo_cidade = QLineEdit()
        self.campo_cidade.setPlaceholderText("Cidade")

        self.campo_km = QDoubleSpinBox()
        self.campo_km.setRange(0, 999999999)
        self.campo_km.setDecimals(1)
        self.campo_km.setSingleStep(1.0)
        self.campo_km.setGroupSeparatorShown(False)
        self.campo_km.setSuffix(" km")

        self.campo_litros = QDoubleSpinBox()
        self.campo_litros.setRange(0, 999999.999)
        self.campo_litros.setDecimals(3)
        self.campo_litros.setSingleStep(10)
        self.campo_litros.setSuffix(" L")

        self.campo_valor_litro = QDoubleSpinBox()
        self.campo_valor_litro.setButtonSymbols(
            QAbstractSpinBox.ButtonSymbols.UpDownArrows
        )
        self.campo_valor_litro.setRange(0, 999999.999)
        self.campo_valor_litro.setDecimals(3)
        self.campo_valor_litro.setPrefix("R$ ")
        self.campo_valor_litro.setSingleStep(0.01)

        self.rotulo_total = QLabel("R$ 0,00")
        self.rotulo_total.setStyleSheet("""
            QLabel {
                color: #166534;
                font-size: 19px;
                font-weight: 700;
                padding: 5px;
            }
        """)

        self.campo_observacao = QLineEdit()
        self.campo_observacao.setPlaceholderText("Observações opcionais")

        campos = [
            self.campo_data,
            self.campo_veiculo,
            self.campo_motorista,
            self.campo_combustivel,
            self.campo_posto,
            self.campo_cidade,
            self.campo_km,
            self.campo_litros,
            self.campo_valor_litro,
            self.campo_observacao,
        ]

        for campo in campos:
            campo.setMinimumHeight(36)

        def adicionar_campo(linha, coluna, texto, campo):
            rotulo = QLabel(texto)
            rotulo.setStyleSheet("color: #334155; font-size: 15px; font-weight: 700;")
            grade.addWidget(rotulo, linha, coluna)
            grade.addWidget(campo, linha, coluna + 1)

        adicionar_campo(0, 0, "Data", self.campo_data)
        adicionar_campo(0, 2, "Veículo", self.campo_veiculo)
        adicionar_campo(0, 4, "Motorista", self.campo_motorista)

        adicionar_campo(1, 0, "Combustível", self.campo_combustivel)
        adicionar_campo(1, 2, "Posto", self.campo_posto)
        adicionar_campo(1, 4, "Cidade", self.campo_cidade)

        def criar_controle_com_setas(campo, incremento):
            controle = QWidget()
            layout_controle = QHBoxLayout(controle)
            layout_controle.setContentsMargins(0, 0, 0, 0)
            layout_controle.setSpacing(4)
            controle.setFixedHeight(36)

            campo.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
            layout_controle.addWidget(campo, 1)

            layout_setas = QVBoxLayout()
            layout_setas.setContentsMargins(0, 0, 0, 0)
            layout_setas.setSpacing(0)

            botao_cima = QPushButton("▲")
            botao_baixo = QPushButton("▼")

            for botao in (botao_cima, botao_baixo):
                botao.setFixedSize(28, 17)
                botao.setStyleSheet("""
                    QPushButton {
                        background-color: #eff6ff;
                        color: #1d4ed8;
                        border: 1px solid #bfdbfe;
                        border-radius: 4px;
                        padding: 0;
                        font-size: 9px;
                        font-weight: 700;
                    }
                    QPushButton:hover {
                        background-color: #dbeafe;
                    }
                    QPushButton:pressed {
                        background-color: #bfdbfe;
                    }
                """)

            botao_cima.clicked.connect(
                lambda: campo.setValue(campo.value() + incremento)
            )

            botao_baixo.clicked.connect(
                lambda: campo.setValue(max(campo.minimum(), campo.value() - incremento))
            )

            layout_setas.addWidget(botao_cima)
            layout_setas.addWidget(botao_baixo)
            layout_controle.addLayout(layout_setas)

            return controle

        controles_km = criar_controle_com_setas(self.campo_km, 1.0)
        controles_litros = criar_controle_com_setas(self.campo_litros, 1.0)

        adicionar_campo(2, 0, "Quilometragem", controles_km)
        adicionar_campo(2, 2, "Litros", controles_litros)
        controles_valor_litro = QWidget()
        layout_valor_litro = QHBoxLayout(controles_valor_litro)
        layout_valor_litro.setContentsMargins(0, 0, 0, 0)
        layout_valor_litro.setSpacing(4)

        self.campo_valor_litro.setButtonSymbols(
            QAbstractSpinBox.ButtonSymbols.NoButtons
        )
        layout_valor_litro.addWidget(self.campo_valor_litro, 1)

        botoes_setas_valor = QVBoxLayout()
        botoes_setas_valor.setContentsMargins(0, 0, 0, 0)
        botoes_setas_valor.setSpacing(2)

        botao_aumentar_valor = QPushButton("▲")
        botao_diminuir_valor = QPushButton("▼")

        for botao in (botao_aumentar_valor, botao_diminuir_valor):
            botao.setFixedSize(28, 17)
            botao.setStyleSheet("""
                QPushButton {
                    background-color: #eff6ff;
                    color: #1d4ed8;
                    border: 1px solid #bfdbfe;
                    border-radius: 4px;
                    padding: 0;
                    font-size: 9px;
                    font-weight: 700;
                }
                QPushButton:hover {
                    background-color: #dbeafe;
                }
                QPushButton:pressed {
                    background-color: #bfdbfe;
                }
            """)

        botoes_setas_valor.addWidget(botao_aumentar_valor)
        botoes_setas_valor.addWidget(botao_diminuir_valor)
        layout_valor_litro.addLayout(botoes_setas_valor)

        botao_aumentar_valor.clicked.connect(
            lambda: self.campo_valor_litro.setValue(
                self.campo_valor_litro.value() + 0.01
            )
        )

        botao_diminuir_valor.clicked.connect(
            lambda: self.campo_valor_litro.setValue(
                max(0.0, self.campo_valor_litro.value() - 0.01)
            )
        )

        adicionar_campo(2, 4, "Valor por litro", controles_valor_litro)

        rotulo_total = QLabel("Valor total:")
        rotulo_total.setStyleSheet("color: #334155; font-weight: 700;")
        grade.addWidget(rotulo_total, 3, 0)
        grade.addWidget(self.rotulo_total, 3, 1)

        adicionar_campo(3, 2, "Observações", self.campo_observacao)
        grade.setColumnStretch(1, 1)
        grade.setColumnStretch(3, 1)
        grade.setColumnStretch(5, 1)

        grupo.setStyleSheet("""
            QGroupBox {
                color: #0f172a;
                font-size: 14px;
                font-weight: 700;
                border: 1px solid #d9dee7;
                border-radius: 9px;
                margin-top: 10px;
                padding-top: 8px;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 5px;
            }

            QLineEdit, QComboBox, QDateEdit,
            QSpinBox, QDoubleSpinBox {
                background-color: #ffffff;
                color: #0f172a;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                padding: 5px 7px;
                font-size: 13px;
            }

            QLineEdit:focus, QComboBox:focus,
            QDateEdit:focus, QSpinBox:focus,
            QDoubleSpinBox:focus {
                border: 1px solid #2563eb;
            }
        """)

        self.layout_lancamento.addWidget(grupo)

        # BOTOES
        linha_botoes = QHBoxLayout()
        linha_botoes.addStretch()

        botao_limpar = QPushButton("Limpar")
        botao_salvar = QPushButton("Registrar abastecimento")

        botao_limpar.setMinimumHeight(40)
        botao_salvar.setMinimumHeight(40)

        botao_limpar.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9;
                color: #334155;
                border: 1px solid #cbd5e1;
                border-radius: 7px;
                padding: 8px 16px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
            }
        """)

        botao_salvar.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: #ffffff;
                border: none;
                border-radius: 7px;
                padding: 8px 18px;
                font-weight: 700;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
        """)

        linha_botoes.addWidget(botao_limpar)
        linha_botoes.addWidget(botao_salvar)
        self.layout_lancamento.addLayout(linha_botoes)

        # HISTORICO
        titulo_historico = QLabel("Histórico de abastecimentos")
        titulo_historico.setStyleSheet("""
            QLabel {
                color: #0f172a;
                font-size: 18px;
                font-weight: 700;
                padding-top: 5px;
            }
        """)
        self.layout_historico.addWidget(titulo_historico)

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(10)
        self.tabela.setHorizontalHeaderLabels(
            [
                "Data",
                "Placa",
                "Motorista",
                "Combustível",
                "Posto",
                "Cidade",
                "Km",
                "Litros",
                "Valor/L",
                "Total",
            ]
        )

        self.tabela.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabela.setSelectionMode(QTableWidget.SingleSelection)
        self.tabela.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabela.setAlternatingRowColors(True)
        self.tabela.setShowGrid(False)
        self.tabela.verticalHeader().setDefaultSectionSize(36)

        self.tabela.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                alternate-background-color: #f8fafc;
                border: 1px solid #d9dee7;
                border-radius: 8px;
                gridline-color: #d9dee7;
                color: #000000;
                font-size: 12px;
                font-weight: 600;
                selection-background-color: #bfdbfe;
                selection-color: #000000;
            }

            QTableWidget::item {
                padding: 5px;
                border: none;
            }

            QTableWidget::item:hover {
                background-color: #bfdbfe;
                color: #000000;
            }

            QTableWidget::item:selected {
                background-color: #bfdbfe;
                color: #000000;
            }

            QHeaderView::section {
                background-color: #edf2f7;
                color: #334155;
                border: none;
                border-bottom: 1px solid #d9dee7;
                padding: 8px 6px;
                font-size: 12px;
                font-weight: 700;
            }
        """)

        cabecalho = self.tabela.horizontalHeader()

        # ALINHAMENTO DOS TITULOS DAS COLUNAS
        for coluna in (2, 3, 4, 5):
            self.tabela.horizontalHeaderItem(coluna).setTextAlignment(
                Qt.AlignLeft | Qt.AlignVCenter
            )

        for coluna in (0, 1, 6):
            self.tabela.horizontalHeaderItem(coluna).setTextAlignment(Qt.AlignCenter)

        for coluna in (7, 8, 9):
            self.tabela.horizontalHeaderItem(coluna).setTextAlignment(
                Qt.AlignRight | Qt.AlignVCenter
            )
        cabecalho.setSectionResizeMode(QHeaderView.Interactive)

        self.tabela.setColumnWidth(0, 100)  # Data
        self.tabela.setColumnWidth(1, 90)  # Placa
        self.tabela.setColumnWidth(3, 130)  # Combustível
        self.tabela.setColumnWidth(6, 110)  # Km
        self.tabela.setColumnWidth(7, 100)  # Litros
        self.tabela.setColumnWidth(8, 110)  # Valor por litro
        self.tabela.setColumnWidth(9, 110)  # Total

        cabecalho.setSectionResizeMode(2, QHeaderView.Stretch)
        cabecalho.setSectionResizeMode(4, QHeaderView.Stretch)
        cabecalho.setSectionResizeMode(5, QHeaderView.Stretch)
        cabecalho.setStretchLastSection(True)

        self.layout_historico.addWidget(self.tabela, 1)

        # EVENTOS
        self.campo_litros.valueChanged.connect(self.atualizar_total)
        self.campo_valor_litro.valueChanged.connect(self.atualizar_total)

        botao_limpar.clicked.connect(self.limpar_formulario)
        botao_salvar.clicked.connect(self.registrar_abastecimento)

        self.carregar_opcoes()
        self.carregar_abastecimentos()

    @staticmethod
    def formatar_moeda(valor):
        valor = Decimal(str(valor))
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def atualizar_total(self, *_):
        litros = Decimal(str(self.campo_litros.value()))
        valor_litro = Decimal(str(self.campo_valor_litro.value()))
        total = litros * valor_litro
        self.rotulo_total.setText(self.formatar_moeda(total))

    def carregar_opcoes(self):
        sessao = SessionLocal()

        try:
            veiculos = sessao.query(Veiculo).order_by(Veiculo.placa.asc()).all()

            motoristas = sessao.query(Motorista).order_by(Motorista.nome.asc()).all()

            self.campo_veiculo.clear()
            for veiculo in veiculos:
                identificacao = (
                    f"{veiculo.placa} — " f"{veiculo.codigo_frota or 'Sem código'}"
                )
                self.campo_veiculo.addItem(identificacao, veiculo.id)

            self.campo_motorista.clear()
            self.campo_motorista.addItem("Não informado", None)

            for motorista in motoristas:
                self.campo_motorista.addItem(motorista.nome, motorista.id)

        except Exception as erro:
            QMessageBox.critical(
                self,
                "Erro ao carregar opções",
                f"Não foi possível carregar veículos e motoristas.\n\n{erro}",
            )
        finally:
            sessao.close()

    def registrar_abastecimento(self):
        veiculo_id = self.campo_veiculo.currentData()
        motorista_id = self.campo_motorista.currentData()
        posto = self.campo_posto.text().strip()
        cidade = self.campo_cidade.text().strip()
        litros = Decimal(str(self.campo_litros.value()))
        valor_litro = Decimal(str(self.campo_valor_litro.value()))

        if veiculo_id is None:
            QMessageBox.warning(
                self,
                "Veículo obrigatório",
                "Cadastre um veículo antes de registrar o abastecimento.",
            )
            return

        if not posto or not cidade:
            QMessageBox.warning(
                self,
                "Dados obrigatórios",
                "Preencha o nome e a cidade do posto.",
            )
            return

        if litros <= 0 or valor_litro <= 0:
            QMessageBox.warning(
                self,
                "Valores inválidos",
                "Informe uma quantidade de litros e um valor por litro maiores que zero.",
            )
            return

        total = (litros * valor_litro).quantize(Decimal("0.01"))

        registro = Abastecimento(
            data=self.campo_data.date().toPython(),
            veiculo_id=veiculo_id,
            motorista_id=motorista_id,
            combustivel=self.campo_combustivel.currentText(),
            posto=posto,
            cidade_posto=cidade,
            quilometragem=self.campo_km.value(),
            litros=litros,
            valor_litro=valor_litro,
            valor_total=total,
            observacao=(self.campo_observacao.text().strip() or None),
        )

        sessao = SessionLocal()

        try:
            sessao.add(registro)
            sessao.commit()
        except Exception as erro:
            sessao.rollback()
            QMessageBox.critical(
                self,
                "Erro ao registrar abastecimento",
                f"Não foi possível salvar o abastecimento.\n\n{erro}",
            )
            return
        finally:
            sessao.close()

        QMessageBox.information(
            self,
            "Abastecimento registrado",
            "O abastecimento foi registrado com sucesso.",
        )

        self.limpar_formulario()
        self.carregar_abastecimentos()

    def carregar_abastecimentos(self):
        sessao = SessionLocal()

        try:
            registros = (
                sessao.query(Abastecimento, Veiculo, Motorista)
                .join(
                    Veiculo,
                    Abastecimento.veiculo_id == Veiculo.id,
                )
                .outerjoin(
                    Motorista,
                    Abastecimento.motorista_id == Motorista.id,
                )
                .order_by(
                    Abastecimento.data.desc(),
                    Abastecimento.id.desc(),
                )
                .all()
            )

            self.tabela.setRowCount(len(registros))

            for linha, (abastecimento, veiculo, motorista) in enumerate(registros):
                dados = [
                    abastecimento.data.strftime("%d/%m/%Y"),
                    veiculo.placa,
                    motorista.nome if motorista else "Não informado",
                    abastecimento.combustivel,
                    abastecimento.posto,
                    abastecimento.cidade_posto,
                    (
                        f"{abastecimento.quilometragem:.0f} km"
                        if Decimal(str(abastecimento.quilometragem)) % 1 == 0
                        else f"{abastecimento.quilometragem:.1f}".replace(".", ",")
                        + " km"
                    ),
                    f"{abastecimento.litros:.3f}".replace(".", ","),
                    self.formatar_moeda(abastecimento.valor_litro),
                    self.formatar_moeda(abastecimento.valor_total),
                ]

                for coluna, valor in enumerate(dados):
                    item = QTableWidgetItem(str(valor))

                    if coluna in (0, 1, 6):
                        item.setTextAlignment(Qt.AlignCenter)

                    if coluna in (7, 8, 9):
                        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

                    self.tabela.setItem(linha, coluna, item)

                self.tabela.item(linha, 0).setData(Qt.UserRole, abastecimento.id)

        except Exception as erro:
            QMessageBox.critical(
                self,
                "Erro ao carregar histórico",
                f"Não foi possível carregar os abastecimentos.\n\n{erro}",
            )
        finally:
            sessao.close()

    def limpar_formulario(self):
        self.campo_data.setDate(QDate.currentDate())
        self.campo_veiculo.setCurrentIndex(0)
        self.campo_motorista.setCurrentIndex(0)
        self.campo_combustivel.setCurrentIndex(0)
        self.campo_posto.clear()
        self.campo_cidade.clear()
        self.campo_km.setValue(0)
        self.campo_litros.setValue(0)
        self.campo_valor_litro.setValue(0)
        self.campo_observacao.clear()
