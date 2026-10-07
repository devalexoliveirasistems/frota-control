import os
import shutil

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QFileDialog,
    QHeaderView,
)

from PySide6.QtCore import Qt

from banco.sessao import SessionLocal
from banco.modelos import Motorista, DocumentoMotorista


class Documentos(QWidget):
    def __init__(self):
        super().__init__()

        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(16, 16, 16, 16)
        layout_principal.setSpacing(14)

        titulo = QLabel("Documentos")
        titulo.setStyleSheet("""
            QLabel {
                color: #0f172a;
                font-size: 26px;
                font-weight: 700;
            }
        """)

        descricao = QLabel(
            "Consulte os documentos cadastrados dos motoristas e acesse seus arquivos."
        )
        descricao.setStyleSheet("""
            QLabel {
                color: #334155;
                font-size: 15px;
                font-weight: 500;
            }
        """)

        layout_principal.addWidget(titulo)
        layout_principal.addWidget(descricao)

        linha_acoes = QHBoxLayout()
        linha_acoes.setSpacing(8)

        botao_abrir = QPushButton("Abrir arquivo")
        botao_abrir.setMinimumWidth(130)
        botao_abrir.setMinimumHeight(38)

        botao_abrir.setStyleSheet("""
            QPushButton {
                background-color: #eff6ff;
                color: #1d4ed8;
                border: 1px solid #bfdbfe;
                border-radius: 8px;
                padding: 7px 16px;
                font-size: 14px;
                font-weight: 700;
            }

            QPushButton:hover {
                background-color: #dbeafe;
            }

            QPushButton:pressed {
                background-color: #bfdbfe;
            }
        """)

        botao_salvar = QPushButton("Salvar cópia")
        botao_salvar.setMinimumWidth(130)
        botao_salvar.setMinimumHeight(38)

        botao_salvar.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9;
                color: #374151;
                border: 1px solid #cbd5e1;
                border-radius: 8px;
                padding: 7px 16px;
                font-size: 14px;
                font-weight: 700;
            }

            QPushButton:hover {
                background-color: #e2e8f0;
            }

            QPushButton:pressed {
                background-color: #cbd5e1;
            }
        """)

        linha_acoes.addWidget(botao_abrir)
        linha_acoes.addWidget(botao_salvar)
        linha_acoes.addStretch()

        layout_principal.addLayout(linha_acoes)

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(4)

        self.tabela.setHorizontalHeaderLabels(
            [
                "Motorista",
                "Documento",
                "Arquivo",
                "Validade",
            ]
        )

        self.tabela.setSelectionMode(QTableWidget.SingleSelection)
        self.tabela.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabela.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabela.setShowGrid(False)
        self.tabela.setAlternatingRowColors(True)

        self.tabela.verticalHeader().setDefaultSectionSize(40)

        self.tabela.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                alternate-background-color: #f8fafc;
                border: 1px solid #d9dee7;
                border-radius: 10px;
                color: #000000;
                font-size: 14px;
                font-weight: 600;
                selection-background-color: #eff6ff;
                selection-color: #000000;
            }

            QHeaderView::section {
                background-color: #f1f5f9;
                color: #374151;
                border: none;
                border-bottom: 1px solid #d9dee7;
                padding: 9px 10px;
                font-size: 13px;
                font-weight: 700;
            }
        """)

        cabecalho = self.tabela.horizontalHeader()
        cabecalho.setSectionResizeMode(QHeaderView.Interactive)

        cabecalho.setSectionResizeMode(
            0,
            QHeaderView.Stretch,
        )

        cabecalho.setSectionResizeMode(
            2,
            QHeaderView.Stretch,
        )

        self.tabela.setColumnWidth(1, 160)
        self.tabela.setColumnWidth(3, 120)

        layout_principal.addWidget(self.tabela)

        botao_abrir.clicked.connect(self.abrir_documento)
        botao_salvar.clicked.connect(self.salvar_copia)

        self.carregar_documentos()

    def carregar_documentos(self):
        sessao = SessionLocal()

        try:
            registros = (
                sessao.query(DocumentoMotorista, Motorista)
                .join(
                    Motorista,
                    DocumentoMotorista.motorista_id == Motorista.id,
                )
                .order_by(
                    Motorista.nome.asc(),
                    DocumentoMotorista.tipo_documento.asc(),
                )
                .all()
            )

            self.tabela.setRowCount(len(registros))

            for linha, (documento, motorista) in enumerate(registros):
                validade = (
                    documento.validade.strftime("%d/%m/%Y")
                    if documento.validade
                    else "Não informada"
                )

                dados = [
                    motorista.nome,
                    documento.tipo_documento,
                    documento.nome_arquivo,
                    validade,
                ]

                for coluna, valor in enumerate(dados):
                    item = QTableWidgetItem(str(valor))

                    if coluna == 3:
                        item.setTextAlignment(Qt.AlignCenter)

                    self.tabela.setItem(
                        linha,
                        coluna,
                        item,
                    )

                self.tabela.item(
                    linha,
                    0,
                ).setData(
                    Qt.UserRole,
                    documento.id,
                )

        finally:
            sessao.close()

    def obter_documento_selecionado(self):
        linha = self.tabela.currentRow()

        if linha < 0:
            QMessageBox.warning(
                self,
                "Nenhum documento selecionado",
                "Selecione um documento na tabela.",
            )
            return None

        item = self.tabela.item(linha, 0)

        if not item:
            return None

        documento_id = item.data(Qt.UserRole)

        sessao = SessionLocal()

        try:
            return sessao.get(
                DocumentoMotorista,
                documento_id,
            )
        finally:
            sessao.close()

    def abrir_documento(self):
        documento = self.obter_documento_selecionado()

        if not documento:
            return

        caminho = documento.caminho_arquivo

        if not os.path.isfile(caminho):
            QMessageBox.warning(
                self,
                "Arquivo não encontrado",
                "O arquivo deste documento não foi encontrado no computador.",
            )
            return

        try:
            os.startfile(caminho)
        except Exception as erro:
            QMessageBox.critical(
                self,
                "Erro ao abrir arquivo",
                f"Não foi possível abrir o arquivo.\n\n{erro}",
            )

    def salvar_copia(self):
        documento = self.obter_documento_selecionado()

        if not documento:
            return

        caminho_origem = documento.caminho_arquivo

        if not os.path.isfile(caminho_origem):
            QMessageBox.warning(
                self,
                "Arquivo não encontrado",
                "O arquivo deste documento não foi encontrado no computador.",
            )
            return

        caminho_destino, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar cópia do documento",
            documento.nome_arquivo,
            "Todos os arquivos (*.*)",
        )

        if not caminho_destino:
            return

        try:
            shutil.copy2(
                caminho_origem,
                caminho_destino,
            )

            QMessageBox.information(
                self,
                "Cópia salva",
                "A cópia do documento foi salva com sucesso.",
            )

        except Exception as erro:
            QMessageBox.critical(
                self,
                "Erro ao salvar cópia",
                f"Não foi possível salvar a cópia.\n\n{erro}",
            )
