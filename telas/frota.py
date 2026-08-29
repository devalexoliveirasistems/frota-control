from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QLineEdit,
)

from PySide6.QtCore import QEvent
from banco.sessao import SessionLocal
from banco.modelos import Veiculo
from telas.formulario_veiculo import FormularioVeiculo


class Frota(QWidget):
    def __init__(self):
        super().__init__()

        layout_principal = QVBoxLayout()

        # Título
        titulo = QLabel("Frota de Veículos")
        layout_principal.addWidget(titulo)

        # Área dos botões
        linha_botoes = QHBoxLayout()

        botao_novo = QPushButton("Novo veículo")
        botao_atualizar = QPushButton("Atualizar")
        botao_editar = QPushButton("Editar veículo")
        botao_excluir = QPushButton("Excluir veículo")

        linha_botoes.addWidget(botao_novo)
        linha_botoes.addWidget(botao_editar)
        linha_botoes.addWidget(botao_excluir)
        linha_botoes.addWidget(botao_atualizar)
        linha_botoes.addStretch()

        layout_principal.addLayout(linha_botoes)

        self.campo_pesquisa = QLineEdit()
        self.campo_pesquisa.setPlaceholderText(
            "Pesquisar por placa, marca, modelo ou tipo..."
        )
        layout_principal.addWidget(self.campo_pesquisa)

        # Tabela
        self.tabela = QTableWidget()
        self.tabela.setSelectionMode(QTableWidget.SingleSelection)
        self.tabela.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabela.viewport().installEventFilter(self)
        self.tabela.setColumnCount(8)

        self.tabela.setHorizontalHeaderLabels(
            [
                "Código",
                "ID",
                "Placa",
                "Marca",
                "Modelo",
                "Ano",
                "Tipo",
                "Status",
            ]
        )

        layout_principal.addWidget(self.tabela)

        self.setLayout(layout_principal)

        # Carregar veículos
        self.carregar_veiculos()

        # Atualizar tabela
        botao_atualizar.clicked.connect(self.carregar_veiculos)
        botao_novo.clicked.connect(self.abrir_formulario)
        botao_editar.clicked.connect(self.editar_veiculo)
        botao_excluir.clicked.connect(self.excluir_veiculo)
        self.campo_pesquisa.textChanged.connect(self.filtrar_veiculos)

    def carregar_veiculos(self):
        sessao = SessionLocal()
        try:
            veiculos = sessao.query(Veiculo).order_by(Veiculo.id.asc()).all()
            self.tabela.setRowCount(len(veiculos))

            for linha, veiculo in enumerate(veiculos):
                self.tabela.setItem(
                    linha, 0, QTableWidgetItem(str(veiculo.codigo_frota))
                )
                self.tabela.setItem(linha, 1, QTableWidgetItem(str(veiculo.id)))
                self.tabela.setItem(linha, 2, QTableWidgetItem(veiculo.placa))
                self.tabela.setItem(linha, 3, QTableWidgetItem(veiculo.marca))
                self.tabela.setItem(linha, 4, QTableWidgetItem(veiculo.modelo))
                self.tabela.setItem(linha, 5, QTableWidgetItem(str(veiculo.ano)))
                self.tabela.setItem(linha, 6, QTableWidgetItem(veiculo.tipo))
                self.tabela.setItem(linha, 7, QTableWidgetItem(veiculo.status))
        finally:
            sessao.close()

    def filtrar_veiculos(self, texto):
        texto = texto.lower().strip()

        for linha in range(self.tabela.rowCount()):
            encontrou = False

            for coluna in range(1, 7):
                item = self.tabela.item(linha, coluna)

                if item and texto in item.text().lower():
                    encontrou = True
                    break

            self.tabela.setRowHidden(linha, not encontrou)

    def abrir_formulario(self):
        formulario = FormularioVeiculo(parent=self)

        if formulario.exec():
            self.carregar_veiculos()

    def editar_veiculo(self):
        linha = self.tabela.currentRow()

        if linha < 0:
            return

        id_veiculo = int(self.tabela.item(linha, 0).text())

        sessao = SessionLocal()

        try:
            veiculo = sessao.query(Veiculo).filter(Veiculo.id == id_veiculo).first()

            if not veiculo:
                return

            formulario = FormularioVeiculo(
                veiculo=veiculo,
                parent=self,
            )

            if formulario.exec():
                self.tabela.setItem(linha, 1, QTableWidgetItem(veiculo.placa))
                self.tabela.setItem(linha, 2, QTableWidgetItem(veiculo.marca))
                self.tabela.setItem(linha, 3, QTableWidgetItem(veiculo.modelo))
                self.tabela.setItem(linha, 4, QTableWidgetItem(str(veiculo.ano)))
                self.tabela.setItem(linha, 5, QTableWidgetItem(veiculo.tipo))
                self.tabela.setItem(linha, 6, QTableWidgetItem(veiculo.status))

        finally:
            sessao.close()

    def excluir_veiculo(self):
        linha = self.tabela.currentRow()

        if linha < 0 or not self.tabela.item(linha, 0).isSelected():
            QMessageBox.warning(
                self,
                "Nenhum veículo selecionado",
                "Selecione um veículo para excluir.",
            )
            return

        id_veiculo = int(self.tabela.item(linha, 0).text())
        placa = self.tabela.item(linha, 1).text()

        resposta = QMessageBox.question(
            self,
            "Confirmar exclusão",
            f"Tem certeza que deseja excluir o veículo de placa {placa}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if resposta != QMessageBox.Yes:
            return

        sessao = SessionLocal()

        try:
            veiculo = sessao.query(Veiculo).filter(Veiculo.id == id_veiculo).first()

            if not veiculo:
                QMessageBox.warning(
                    self,
                    "Veículo não encontrado",
                    "O veículo não foi encontrado no banco de dados.",
                )
                return

            sessao.delete(veiculo)
            sessao.commit()

            self.tabela.removeRow(linha)

            QMessageBox.information(
                self,
                "Exclusão concluída",
                "Veículo excluído com sucesso.",
            )

        except Exception as erro:
            sessao.rollback()

            QMessageBox.critical(
                self,
                "Erro",
                f"Não foi possível excluir o veículo:\n{erro}",
            )

        finally:
            sessao.close()

    def atualizar_linha(self, linha, veiculo):
        self.tabela.setItem(linha, 0, QTableWidgetItem(str(veiculo.id)))
        self.tabela.setItem(linha, 1, QTableWidgetItem(veiculo.placa))
        self.tabela.setItem(linha, 2, QTableWidgetItem(veiculo.marca))
        self.tabela.setItem(linha, 3, QTableWidgetItem(veiculo.modelo))
        self.tabela.setItem(linha, 4, QTableWidgetItem(str(veiculo.ano)))
        self.tabela.setItem(linha, 5, QTableWidgetItem(veiculo.tipo))
        self.tabela.setItem(linha, 6, QTableWidgetItem(veiculo.status))

    def eventFilter(self, objeto, evento):
        if (
            objeto == self.tabela.viewport()
            and evento.type() == QEvent.MouseButtonPress
        ):
            indice = self.tabela.indexAt(evento.position().toPoint())

            if not indice.isValid():
                self.tabela.clearSelection()

        return super().eventFilter(objeto, evento)
