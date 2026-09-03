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
    QComboBox,
)
from PySide6.QtCore import QEvent, Qt
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

        # Filtros
        linha_filtros = QHBoxLayout()

        self.campo_pesquisa = QLineEdit()
        self.campo_pesquisa.setPlaceholderText(
            "Pesquisar por código, ID, placa, marca ou modelo..."
        )
        self.campo_pesquisa.setClearButtonEnabled(True)

        self.filtro_tipo = QComboBox()
        self.filtro_tipo.addItems(
            [
                "Todos os tipos",
                "Caminhão",
                "Carreta",
                "Van",
                "Carro",
                "Utilitário",
                "Outro",
            ]
        )

        self.filtro_status = QComboBox()
        self.filtro_status.addItems(
            [
                "Todos os status",
                "Ativo",
                "Em manutenção",
                "Inativo",
                "Vendido",
            ]
        )

        self.filtro_composicao = QComboBox()
        self.filtro_composicao.addItems(
            [
                "Todas as composições",
                "Com carreta",
                "Sem carreta",
                "Com Dolly",
                "Sem Dolly",
            ]
        )

        botao_limpar_filtros = QPushButton("Limpar filtros")

        linha_filtros.addWidget(self.campo_pesquisa)
        linha_filtros.addWidget(self.filtro_tipo)
        linha_filtros.addWidget(self.filtro_status)
        linha_filtros.addWidget(self.filtro_composicao)
        linha_filtros.addWidget(botao_limpar_filtros)

        layout_principal.addLayout(linha_filtros)

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

        # Botões
        botao_atualizar.clicked.connect(self.carregar_veiculos)
        botao_novo.clicked.connect(self.abrir_formulario)
        botao_editar.clicked.connect(self.editar_veiculo)
        botao_excluir.clicked.connect(self.excluir_veiculo)

        # Filtros
        self.campo_pesquisa.textChanged.connect(self.filtrar_veiculos)
        self.filtro_tipo.currentIndexChanged.connect(self.filtrar_veiculos)
        self.filtro_status.currentIndexChanged.connect(self.filtrar_veiculos)
        self.filtro_composicao.currentIndexChanged.connect(self.filtrar_veiculos)
        botao_limpar_filtros.clicked.connect(self.limpar_filtros)

    def carregar_veiculos(self):
        sessao = SessionLocal()

        try:
            veiculos = sessao.query(Veiculo).order_by(Veiculo.id.asc()).all()

            self.tabela.setRowCount(len(veiculos))

            for linha, veiculo in enumerate(veiculos):
                item_codigo = QTableWidgetItem(veiculo.codigo_frota)
                item_codigo.setData(Qt.UserRole, veiculo.id)

                self.tabela.setItem(
                    linha,
                    0,
                    item_codigo,
                )

                self.tabela.setItem(
                    linha,
                    1,
                    QTableWidgetItem(str(veiculo.id)),
                )

                self.tabela.setItem(
                    linha,
                    2,
                    QTableWidgetItem(veiculo.placa),
                )

                self.tabela.setItem(
                    linha,
                    3,
                    QTableWidgetItem(veiculo.marca),
                )

                self.tabela.setItem(
                    linha,
                    4,
                    QTableWidgetItem(veiculo.modelo),
                )

                self.tabela.setItem(
                    linha,
                    5,
                    QTableWidgetItem(str(veiculo.ano)),
                )

                self.tabela.setItem(
                    linha,
                    6,
                    QTableWidgetItem(veiculo.tipo),
                )

                self.tabela.setItem(
                    linha,
                    7,
                    QTableWidgetItem(veiculo.status),
                )

        finally:
            sessao.close()

    def filtrar_veiculos(self):
        texto = self.campo_pesquisa.text().lower().strip()
        tipo = self.filtro_tipo.currentText()
        status = self.filtro_status.currentText()
        composicao = self.filtro_composicao.currentText()

        for linha in range(self.tabela.rowCount()):
            encontrou_texto = True
            encontrou_tipo = True
            encontrou_status = True
            encontrou_composicao = True

            if texto:
                encontrou_texto = False

                for coluna in range(0, 8):
                    item = self.tabela.item(linha, coluna)

                    if item and texto in item.text().lower():
                        encontrou_texto = True
                        break

            if tipo != "Todos os tipos":
                item_tipo = self.tabela.item(linha, 6)

                if not item_tipo or item_tipo.text() != tipo:
                    encontrou_tipo = False

            if status != "Todos os status":
                item_status = self.tabela.item(linha, 7)

                if not item_status or item_status.text() != status:
                    encontrou_status = False

            # O filtro de composição será ligado à estrutura
            # de composição quando ela for implementada.
            if composicao != "Todas as composições":
                encontrou_composicao = True

            mostrar = (
                encontrou_texto
                and encontrou_tipo
                and encontrou_status
                and encontrou_composicao
            )

            self.tabela.setRowHidden(
                linha,
                not mostrar,
            )

    def limpar_filtros(self):
        self.campo_pesquisa.clear()
        self.filtro_tipo.setCurrentIndex(0)
        self.filtro_status.setCurrentIndex(0)
        self.filtro_composicao.setCurrentIndex(0)

        self.filtrar_veiculos()

    def abrir_formulario(self):
        formulario = FormularioVeiculo(parent=self)

        if formulario.exec():
            self.carregar_veiculos()

    def editar_veiculo(self):
        linha = self.tabela.currentRow()

        if linha < 0:
            return

        id_veiculo = self.tabela.item(
            linha,
            0,
        ).data(Qt.UserRole)

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
                self.tabela.setItem(
                    linha,
                    2,
                    QTableWidgetItem(veiculo.placa),
                )

                self.tabela.setItem(
                    linha,
                    3,
                    QTableWidgetItem(veiculo.marca),
                )

                self.tabela.setItem(
                    linha,
                    4,
                    QTableWidgetItem(veiculo.modelo),
                )

                self.tabela.setItem(
                    linha,
                    5,
                    QTableWidgetItem(str(veiculo.ano)),
                )

                self.tabela.setItem(
                    linha,
                    6,
                    QTableWidgetItem(veiculo.tipo),
                )

                self.tabela.setItem(
                    linha,
                    7,
                    QTableWidgetItem(veiculo.status),
                )

        finally:
            sessao.close()

    def excluir_veiculo(self):
        linha = self.tabela.currentRow()

        if (
            linha < 0
            or not self.tabela.item(
                linha,
                0,
            ).isSelected()
        ):
            QMessageBox.warning(
                self,
                "Nenhum veículo selecionado",
                "Selecione um veículo para excluir.",
            )
            return

        id_veiculo = self.tabela.item(
            linha,
            0,
        ).data(Qt.UserRole)

        placa = self.tabela.item(
            linha,
            2,
        ).text()

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

    def eventFilter(self, objeto, evento):
        if (
            objeto == self.tabela.viewport()
            and evento.type() == QEvent.MouseButtonPress
        ):
            indice = self.tabela.indexAt(evento.position().toPoint())

            if not indice.isValid():
                self.tabela.clearSelection()

        return super().eventFilter(objeto, evento)
