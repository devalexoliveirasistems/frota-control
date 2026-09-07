from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView,
    QGroupBox,
)

from banco.sessao import SessionLocal
from banco.modelos import Motorista


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
        layout_cadastro = QHBoxLayout()

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

        layout_cadastro.addWidget(self.campo_nome, 2)
        layout_cadastro.addWidget(self.campo_cpf)
        layout_cadastro.addWidget(self.campo_telefone)
        layout_cadastro.addWidget(self.campo_status)
        layout_cadastro.addWidget(botao_novo)

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
                status=status,
            )

            sessao.add(motorista)
            sessao.commit()

            self.carregar_motoristas()

            self.campo_nome.clear()
            self.campo_cpf.clear()
            self.campo_telefone.clear()
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
