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
    QMessageBox,
    QHeaderView,
    QGroupBox,
    QFileDialog,
    QGridLayout,
)

from banco.sessao import SessionLocal
from banco.modelos import Motorista
from PySide6.QtCore import QDate


class Motoristas(QWidget):
    def __init__(self):
        super().__init__()

        layout_principal = QVBoxLayout()

        titulo = QLabel("Motoristas")
        titulo.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            """)

        layout_principal.addWidget(titulo)

        # =========================
        # CADASTRO
        # =========================

        card_cadastro = QGroupBox("Cadastro de Motorista")
        layout_cadastro = QVBoxLayout()

        grade_cards = QGridLayout()

        card_pessoais = QGroupBox("Dados Pessoais")
        layout_pessoais = QVBoxLayout()

        self.campo_nome = QLineEdit()
        self.campo_nome.setPlaceholderText("Nome do motorista")

        self.campo_cpf = QLineEdit()
        self.campo_cpf.setPlaceholderText("CPF")

        self.campo_telefone = QLineEdit()
        self.campo_telefone.setPlaceholderText("Telefone")

        self.campo_status = QComboBox()
        self.campo_status.addItems(
            [
                "Ativo",
                "Inativo",
            ]
        )

        botao_novo = QPushButton("Cadastrar motorista")

        layout_pessoais.addWidget(QLabel("Nome"))

        layout_pessoais.addWidget(self.campo_nome)

        layout_pessoais.addWidget(QLabel("CPF"))

        layout_pessoais.addWidget(self.campo_cpf)

        layout_pessoais.addWidget(QLabel("Telefone"))

        layout_pessoais.addWidget(self.campo_telefone)

        layout_pessoais.addWidget(QLabel("Status"))

        layout_pessoais.addWidget(self.campo_status)

        card_pessoais.setLayout(layout_pessoais)

        grade_cards.addWidget(
            card_pessoais,
            0,
            0,
        )

        # =========================
        # ENDEREÇO
        # =========================

        card_endereco = QGroupBox("Endereço")
        layout_endereco = QVBoxLayout()

        self.campo_cep = QLineEdit()
        self.campo_cep.setPlaceholderText("CEP")

        self.campo_logradouro = QLineEdit()
        self.campo_logradouro.setPlaceholderText("Logradouro")

        self.campo_numero = QLineEdit()
        self.campo_numero.setPlaceholderText("Número")

        self.campo_complemento = QLineEdit()
        self.campo_complemento.setPlaceholderText("Complemento")

        self.campo_bairro = QLineEdit()
        self.campo_bairro.setPlaceholderText("Bairro")

        self.campo_cidade = QLineEdit()
        self.campo_cidade.setPlaceholderText("Cidade")

        self.campo_estado = QLineEdit()
        self.campo_estado.setPlaceholderText("Estado")

        # Primeira linha
        linha_endereco_1 = QHBoxLayout()

        linha_endereco_1.addWidget(self.campo_cep)

        linha_endereco_1.addWidget(
            self.campo_logradouro,
            2,
        )

        linha_endereco_1.addWidget(self.campo_numero)

        layout_endereco.addLayout(linha_endereco_1)

        # Segunda linha
        linha_endereco_2 = QHBoxLayout()

        linha_endereco_2.addWidget(self.campo_complemento)

        linha_endereco_2.addWidget(self.campo_bairro)

        linha_endereco_2.addWidget(
            self.campo_cidade,
            2,
        )

        layout_endereco.addLayout(linha_endereco_2)

        # Terceira linha
        linha_endereco_3 = QHBoxLayout()

        linha_endereco_3.addWidget(self.campo_estado)

        linha_endereco_3.addStretch()

        layout_endereco.addLayout(linha_endereco_3)

        card_endereco.setLayout(layout_endereco)

        grade_cards.addWidget(
            card_endereco,
            0,
            2,
        )

        layout_cadastro.addLayout(grade_cards)

        # =========================
        # HABILITAÇÃO

        # =========================

        card_habilitacao = QGroupBox("Habilitação")
        layout_habilitacao = QVBoxLayout()

        self.campo_categoria_cnh = QComboBox()

        self.campo_categoria_cnh.addItems(
            [
                "Selecione",
                "ACC",
                "A",
                "B",
                "AB",
                "C",
                "AC",
                "D",
                "AD",
                "E",
                "AE",
            ]
        )

        self.campo_validade_cnh = QDateEdit()
        self.campo_validade_cnh.setCalendarPopup(True)
        self.campo_validade_cnh.setDate(QDate.currentDate())

        self.campo_arquivo_cnh = QLineEdit()
        self.campo_arquivo_cnh.setPlaceholderText("Arquivo da CNH")
        self.campo_arquivo_cnh.setReadOnly(True)

        botao_cnh = QPushButton("Adicionar arquivo")

        botao_cnh.clicked.connect(self.adicionar_cnh)

        linha_habilitacao = QHBoxLayout()

        linha_habilitacao = QHBoxLayout()

        linha_habilitacao.addWidget(QLabel("Categoria CNH"))

        linha_habilitacao.addWidget(self.campo_categoria_cnh)

        linha_habilitacao.addWidget(QLabel("Validade"))

        linha_habilitacao.addWidget(self.campo_validade_cnh)

        layout_habilitacao.addLayout(linha_habilitacao)

        linha_documento = QHBoxLayout()

        linha_documento.addWidget(QLabel("CNH"))

        linha_documento.addWidget(
            self.campo_arquivo_cnh,
            2,
        )

        linha_documento.addWidget(botao_cnh)

        layout_habilitacao.addLayout(linha_documento)

        card_habilitacao.setLayout(layout_habilitacao)

        grade_cards.addWidget(
            card_habilitacao,
            0,
            1,
        )

        linha_botao = QHBoxLayout()

        linha_botao.addStretch()

        botao_novo.setMinimumWidth(180)

        linha_botao.addWidget(botao_novo)

        layout_cadastro.addLayout(linha_botao)

        card_cadastro.setLayout(layout_cadastro)
        layout_principal.addWidget(card_cadastro)

        # =========================
        # TABELA
        # =========================

        self.tabela = QTableWidget()

        self.tabela.setColumnCount(5)

        self.tabela.setHorizontalHeaderLabels(
            [
                "ID",
                "Nome",
                "CPF",
                "Telefone",
                "Status",
            ]
        )

        self.tabela.setSelectionMode(QTableWidget.SingleSelection)

        self.tabela.setSelectionBehavior(QTableWidget.SelectRows)

        self.tabela.setEditTriggers(QTableWidget.NoEditTriggers)

        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout_principal.addWidget(self.tabela)

        self.setLayout(layout_principal)

        # =========================
        # EVENTOS
        # =========================

        botao_novo.clicked.connect(self.cadastrar_motorista)

        self.carregar_motoristas()

    def adicionar_cnh(self):
        arquivo, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar CNH",
            "",
            "Arquivos PDF e imagens (*.pdf *.jpg *.jpeg *.png)",
        )

        if arquivo:
            self.caminho_cnh = arquivo
            self.campo_arquivo_cnh.setText(arquivo)

    def cadastrar_motorista(self):
        nome = self.campo_nome.text().strip()
        cpf = self.campo_cpf.text().strip()
        telefone = self.campo_telefone.text().strip()
        status = self.campo_status.currentText()

        if not nome:
            QMessageBox.warning(
                self,
                "Campo obrigatório",
                "Informe o nome do motorista.",
            )
            return

        if not cpf:
            QMessageBox.warning(
                self,
                "Campo obrigatório",
                "Informe o CPF do motorista.",
            )
            return

        sessao = SessionLocal()

        try:
            motorista = Motorista(
                nome=nome,
                cpf=cpf,
                telefone=telefone or None,
                categoria_cnh=(
                    None
                    if self.campo_categoria_cnh.currentText() == "Selecione"
                    else self.campo_categoria_cnh.currentText()
                ),
                validade_cnh=(self.campo_validade_cnh.date().toPython()),
                status=status,
            )

            sessao.add(motorista)
            sessao.commit()

            self.carregar_motoristas()

            self.campo_nome.clear()
            self.campo_cpf.clear()
            self.campo_telefone.clear()

            self.campo_categoria_cnh.setCurrentIndex(0)

            self.campo_validade_cnh.setDate(QDate.currentDate())

            self.campo_arquivo_cnh.clear()

            self.campo_status.setCurrentIndex(0)

            QMessageBox.information(
                self,
                "Cadastro concluído",
                "Motorista cadastrado com sucesso.",
            )

        except Exception as erro:
            sessao.rollback()

            QMessageBox.critical(
                self,
                "Erro",
                f"Não foi possível cadastrar o motorista:\n\n{erro}",
            )

        finally:
            sessao.close()

    def carregar_motoristas(self):
        sessao = SessionLocal()

        try:
            motoristas = sessao.query(Motorista).order_by(Motorista.id.asc()).all()

            self.tabela.setRowCount(len(motoristas))

            for linha, motorista in enumerate(motoristas):
                dados = [
                    motorista.id,
                    motorista.nome,
                    motorista.cpf,
                    motorista.telefone or "",
                    motorista.status,
                ]

                for coluna, valor in enumerate(dados):
                    self.tabela.setItem(
                        linha,
                        coluna,
                        QTableWidgetItem(str(valor)),
                    )

        finally:
            sessao.close()
