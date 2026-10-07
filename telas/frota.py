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
    QHeaderView,
)
from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QColor

from banco.sessao import SessionLocal
from banco.modelos import Veiculo
from telas.formulario_veiculo import FormularioVeiculo


class Frota(QWidget):
    def __init__(self):
        super().__init__()

        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(14, 14, 14, 14)
        layout_principal.setSpacing(14)

        self.setStyleSheet("""
            Frota {
                background-color: #ffffff;
            }
        """)

        # ==================================
        # TÍTULO
        # ==================================

        titulo = QLabel("Frota de Veículos")
        titulo.setStyleSheet("""
            QLabel {
                color: #0f172a;
                font-size: 27px;
                font-weight: 800;
                padding-left: 10px;
                border-left: 5px solid #2563eb;
                background: transparent;
            }
        """)
        layout_principal.addWidget(titulo)

        # ==================================
        # BOTÕES DE AÇÃO
        # ==================================

        linha_botoes = QHBoxLayout()
        linha_botoes.setSpacing(10)

        botao_novo = QPushButton("Novo veículo")
        botao_editar = QPushButton("Editar veículo")
        botao_excluir = QPushButton("Excluir veículos")
        botao_atualizar = QPushButton("Atualizar")

        self._estilizar_botao(
            botao_novo,
            largura=150,
            fundo="#2563eb",
            texto="#ffffff",
            borda="#2563eb",
            hover="#1d4ed8",
            pressionado="#1e40af",
        )

        self._estilizar_botao(
            botao_editar,
            largura=155,
            fundo="#eff6ff",
            texto="#1d4ed8",
            borda="#93c5fd",
            hover="#dbeafe",
            pressionado="#bfdbfe",
        )

        self._estilizar_botao(
            botao_excluir,
            largura=165,
            fundo="#fef2f2",
            texto="#dc2626",
            borda="#fca5a5",
            hover="#fee2e2",
            pressionado="#fecaca",
        )

        self._estilizar_botao(
            botao_atualizar,
            largura=130,
            fundo="#f8fafc",
            texto="#334155",
            borda="#cbd5e1",
            hover="#f1f5f9",
            pressionado="#e2e8f0",
        )

        linha_botoes.addWidget(botao_novo)
        linha_botoes.addWidget(botao_editar)
        linha_botoes.addWidget(botao_excluir)
        linha_botoes.addWidget(botao_atualizar)
        linha_botoes.addStretch()

        layout_principal.addLayout(linha_botoes)

        # ==================================
        # FILTROS
        # ==================================

        linha_filtros = QHBoxLayout()
        linha_filtros.setSpacing(10)

        self.campo_pesquisa = QLineEdit()
        self.campo_pesquisa.setPlaceholderText(
            "Pesquisar por código, ID, placa, marca ou modelo..."
        )
        self.campo_pesquisa.setClearButtonEnabled(True)
        self.campo_pesquisa.setMinimumHeight(36)
        self.campo_pesquisa.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff;
                color: #1e293b;
                border: 1px solid #cbd5e1;
                border-radius: 7px;
                padding: 7px 12px;
                font-size: 13px;
                font-weight: 500;
            }

            QLineEdit:hover {
                border-color: #94a3b8;
            }

            QLineEdit:focus {
                border: 1px solid #60a5fa;
            }
        """)

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

        estilo_combo = """
            QComboBox {
                background-color: #ffffff;
                color: #1e293b;
                border: 1px solid #cbd5e1;
                border-radius: 7px;
                padding: 6px 10px;
                min-height: 36px;
                font-size: 13px;
                font-weight: 500;
            }

            QComboBox:hover {
                border-color: #94a3b8;
            }

            QComboBox:focus {
                border: 1px solid #60a5fa;
            }
        """

        for campo in (
            self.filtro_tipo,
            self.filtro_status,
            self.filtro_composicao,
        ):
            campo.setStyleSheet(estilo_combo)

        self.campo_pesquisa.setMinimumWidth(350)
        self.filtro_tipo.setMinimumWidth(120)
        self.filtro_status.setMinimumWidth(130)
        self.filtro_composicao.setMinimumWidth(155)

        botao_limpar_filtros = QPushButton("Limpar filtros")
        self._estilizar_botao(
            botao_limpar_filtros,
            largura=120,
            fundo="#f8fafc",
            texto="#334155",
            borda="#cbd5e1",
            hover="#f1f5f9",
            pressionado="#e2e8f0",
            altura=36,
            fonte=13,
        )

        linha_filtros.addWidget(self.campo_pesquisa, 1)
        linha_filtros.addWidget(self.filtro_tipo)
        linha_filtros.addWidget(self.filtro_status)
        linha_filtros.addWidget(self.filtro_composicao)
        linha_filtros.addWidget(botao_limpar_filtros)

        layout_principal.addLayout(linha_filtros)

        # ==================================
        # TABELA
        # ==================================

        self.tabela = QTableWidget()
        self.tabela.setSelectionMode(QTableWidget.SingleSelection)
        self.tabela.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabela.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabela.setFocusPolicy(Qt.StrongFocus)
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

        self.tabela.setAlternatingRowColors(True)
        self.tabela.setShowGrid(False)
        self.tabela.verticalHeader().setDefaultSectionSize(38)
        self.tabela.horizontalHeader().setMinimumHeight(40)

        self.tabela.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                alternate-background-color: #f8fafc;
                border: 1px solid #d9dee7;
                border-radius: 8px;
                color: #000000;
                font-size: 13px;
                font-weight: 600;
                selection-background-color: #eff6ff;
                selection-color: #000000;
            }

            QHeaderView::section {
                background-color: #edf2f7;
                color: #1f2937;
                border: none;
                border-bottom: 1px solid #d9dee7;
                padding: 8px 10px;
                font-size: 13px;
                font-weight: 700;
            }

            QHeaderView::section:hover {
                background-color: #e5e7eb;
            }
        """)

        cabecalho = self.tabela.horizontalHeader()

        cabecalho.setSectionResizeMode(0, QHeaderView.Stretch)
        cabecalho.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        cabecalho.setSectionResizeMode(2, QHeaderView.Stretch)
        cabecalho.setSectionResizeMode(3, QHeaderView.Stretch)
        cabecalho.setSectionResizeMode(4, QHeaderView.Stretch)
        cabecalho.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        cabecalho.setSectionResizeMode(6, QHeaderView.Stretch)
        cabecalho.setSectionResizeMode(7, QHeaderView.Stretch)

        layout_principal.addWidget(self.tabela, 1)

        # ==================================
        # EVENTOS
        # ==================================

        self.carregar_veiculos()

        botao_atualizar.clicked.connect(self.carregar_veiculos)
        botao_novo.clicked.connect(self.abrir_formulario)
        botao_editar.clicked.connect(self.editar_veiculo)
        botao_excluir.clicked.connect(self.excluir_veiculo)

        self.campo_pesquisa.textChanged.connect(self.filtrar_veiculos)
        self.filtro_tipo.currentIndexChanged.connect(self.filtrar_veiculos)
        self.filtro_status.currentIndexChanged.connect(self.filtrar_veiculos)
        self.filtro_composicao.currentIndexChanged.connect(self.filtrar_veiculos)
        botao_limpar_filtros.clicked.connect(self.limpar_filtros)

    def _estilizar_botao(
        self,
        botao,
        largura,
        fundo,
        texto,
        borda,
        hover,
        pressionado,
        altura=42,
        fonte=14,
    ):
        botao.setMinimumWidth(largura)
        botao.setMinimumHeight(altura)
        botao.setStyleSheet(f"""
            QPushButton {{
                background-color: {fundo};
                color: {texto};
                border: 1px solid {borda};
                border-radius: 7px;
                padding: 7px 14px;
                font-size: {fonte}px;
                font-weight: 700;
            }}

            QPushButton:hover {{
                background-color: {hover};
            }}

            QPushButton:pressed {{
                background-color: {pressionado};
            }}
        """)

    def carregar_veiculos(self):
        sessao = SessionLocal()

        try:
            veiculos = sessao.query(Veiculo).order_by(Veiculo.id.asc()).all()

            self.tabela.setRowCount(len(veiculos))

            for linha, veiculo in enumerate(veiculos):
                dados = [
                    veiculo.codigo_frota or "",
                    str(veiculo.id),
                    veiculo.placa or "",
                    veiculo.marca or "",
                    veiculo.modelo or "",
                    str(veiculo.ano or ""),
                    veiculo.tipo or "",
                    veiculo.status or "",
                ]

                for coluna, valor in enumerate(dados):
                    item = QTableWidgetItem(str(valor))

                    if coluna in [0, 1, 2, 3, 4, 5, 6, 7]:
                        item.setTextAlignment(Qt.AlignCenter)

                    if coluna == 0:
                        item.setData(Qt.UserRole, veiculo.id)

                    self.tabela.setItem(
                        linha,
                        coluna,
                        item,
                    )

                self._aplicar_status(linha, veiculo.status or "")

        finally:
            sessao.close()

        self.filtrar_veiculos()

    def _aplicar_status(self, linha, status):
        item_status = self.tabela.item(linha, 7)

        if not item_status:
            return

        status_normalizado = status.strip()

        if status_normalizado == "Ativo":
            fundo = "#dcfce7"
            texto = "#15803d"
            borda = "#bbf7d0"
        elif status_normalizado == "Em manutenção":
            fundo = "#fef3c7"
            texto = "#b45309"
            borda = "#fde68a"
        elif status_normalizado in ["Inativo", "Vendido"]:
            fundo = "#fee2e2"
            texto = "#dc2626"
            borda = "#fecaca"
        else:
            fundo = "#f1f5f9"
            texto = "#475569"
            borda = "#cbd5e1"

        etiqueta = QLabel(status_normalizado or "Não informado")
        etiqueta.setAlignment(Qt.AlignCenter)
        etiqueta.setStyleSheet(f"""
            QLabel {{
                background-color: {fundo};
                color: {texto};
                border: 1px solid {borda};
                border-radius: 10px;
                padding: 4px 12px;
                font-size: 12px;
                font-weight: 700;
            }}
        """)

        self.tabela.setCellWidget(linha, 7, etiqueta)

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

            # O filtro de composição continua reservado para quando
            # a estrutura de composição for implementada.
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

        item_codigo = self.tabela.item(
            linha,
            0,
        )

        if not item_codigo:
            return

        id_veiculo = item_codigo.data(Qt.UserRole)

        if not id_veiculo:
            return

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
                self.carregar_veiculos()

        finally:
            sessao.close()

    def excluir_veiculo(self):
        linha = self.tabela.currentRow()

        if linha < 0:
            QMessageBox.warning(
                self,
                "Nenhum veículo selecionado",
                "Selecione um veículo para excluir.",
            )
            return

        item_codigo = self.tabela.item(
            linha,
            0,
        )

        if not item_codigo:
            return

        id_veiculo = item_codigo.data(Qt.UserRole)

        if not id_veiculo:
            QMessageBox.warning(
                self,
                "Veículo inválido",
                "Não foi possível identificar o veículo selecionado.",
            )
            return

        item_placa = self.tabela.item(
            linha,
            2,
        )

        placa = item_placa.text() if item_placa else "não informada"

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

            self.carregar_veiculos()

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
