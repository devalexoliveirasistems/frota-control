import os
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
    QStyle,
    QHeaderView,
    QDialog,
    QFormLayout,
    QGroupBox,
    QScrollArea,
)
from PySide6.QtCore import QEvent, Qt, QSize, QUrl
from PySide6.QtGui import QColor, QIcon, QDesktopServices

from banco.sessao import SessionLocal
from banco.modelos import (
    Veiculo,
    Carreta,
    Dolly,
    Composicao,
    DocumentoVeiculo,
)
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
        botao_novo.setIcon(QIcon("recursos/icones/mais.svg"))
        botao_novo.setIconSize(QSize(20, 20))
        botao_editar = QPushButton("Editar veículo")
        botao_detalhes = QPushButton("Ver detalhes")
        botao_editar.setIcon(QIcon("recursos/icones/editar.svg"))
        botao_editar.setIconSize(QSize(22, 22))
        botao_excluir = QPushButton("Excluir veículos")
        botao_excluir.setIcon(QIcon("recursos/icones/lixeira.svg"))
        botao_excluir.setIconSize(QSize(20, 20))
        botao_atualizar = QPushButton("Atualizar")
        botao_atualizar.setIcon(QIcon("recursos/icones/atualizar.svg"))
        botao_atualizar.setIconSize(QSize(22, 22))

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
            botao_detalhes,
            largura=135,
            fundo="#eff6ff",
            texto="#1d4ed8",
            borda="#93c5fd",
            hover="#dbeafe",
            pressionado="#bfdbfe",
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
        linha_botoes.addWidget(botao_detalhes)
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
                font-size: 14px;
                font-weight: 600;
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

        estilo_combo = """
            QComboBox {
                background-color: #ffffff;
                color: #1e293b;
                border: 1px solid #cbd5e1;
                border-radius: 7px;
                padding: 6px 10px;
                min-height: 36px;
                font-size: 14px;
                font-weight: 600;
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
        ):
            campo.setStyleSheet(estilo_combo)

        self.campo_pesquisa.setMinimumWidth(350)
        self.filtro_tipo.setMinimumWidth(120)
        self.filtro_status.setMinimumWidth(130)

        botao_limpar_filtros = QPushButton("Limpar filtros")
        botao_limpar_filtros.setIcon(QIcon("recursos/icones/limpar_filtros.svg"))
        botao_limpar_filtros.setIconSize(QSize(18, 18))
        self._estilizar_botao(
            botao_limpar_filtros,
            largura=145,
            fundo="#ffffff",
            texto="#2563eb",
            borda="#bfdbfe",
            hover="#eff6ff",
            pressionado="#dbeafe",
            altura=38,
            fonte=13,
        )

        linha_filtros.addWidget(self.campo_pesquisa, 1)
        linha_filtros.addWidget(self.filtro_tipo)
        linha_filtros.addWidget(self.filtro_status)
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
                selection-background-color: #bfdbfe;
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
        botao_detalhes.clicked.connect(self.ver_detalhes_veiculo)
        botao_excluir.clicked.connect(self.excluir_veiculo)

        self.campo_pesquisa.textChanged.connect(self.filtrar_veiculos)
        self.filtro_tipo.currentIndexChanged.connect(self.filtrar_veiculos)
        self.filtro_status.currentIndexChanged.connect(self.filtrar_veiculos)
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

        container = QWidget()
        layout_status = QHBoxLayout(container)
        layout_status.setContentsMargins(0, 0, 0, 0)
        layout_status.setAlignment(Qt.AlignCenter)

        texto_status = (
            "Manutenção"
            if status_normalizado == "Em manutenção"
            else status_normalizado
        )
        etiqueta = QLabel(texto_status or "Não informado")
        etiqueta.setAlignment(Qt.AlignCenter)
        etiqueta.setFixedHeight(26)
        etiqueta.setMinimumWidth(88)

        etiqueta.setStyleSheet(f"""
            QLabel {{
                background-color: {fundo};
                color: {texto};
                border: 1px solid {borda};
                border-radius: 7px;
                padding: 2px 10px;
                font-size: 12px;
                font-weight: 700;
            }}
        """)

        layout_status.addWidget(etiqueta)

        self.tabela.setCellWidget(linha, 7, container)

    def filtrar_veiculos(self):
        texto = self.campo_pesquisa.text().lower().strip()
        tipo = self.filtro_tipo.currentText()
        status = self.filtro_status.currentText()

        for linha in range(self.tabela.rowCount()):
            encontrou_texto = True
            encontrou_tipo = True
            encontrou_status = True

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

            mostrar = encontrou_texto and encontrou_tipo and encontrou_status

            self.tabela.setRowHidden(
                linha,
                not mostrar,
            )

    def limpar_filtros(self):
        self.campo_pesquisa.clear()
        self.filtro_tipo.setCurrentIndex(0)
        self.filtro_status.setCurrentIndex(0)
        self.filtrar_veiculos()

    def abrir_formulario(self):
        formulario = FormularioVeiculo(parent=self)

        if formulario.exec():
            self.carregar_veiculos()

    def ver_detalhes_veiculo(self):
        linha = self.tabela.currentRow()

        if linha < 0:
            QMessageBox.warning(
                self,
                "Nenhum veículo selecionado",
                "Selecione um veículo para ver os detalhes.",
            )
            return

        item_codigo = self.tabela.item(linha, 0)

        if not item_codigo:
            return

        id_veiculo = item_codigo.data(Qt.UserRole)

        if not id_veiculo:
            return

        sessao = SessionLocal()

        try:
            veiculo = sessao.get(Veiculo, id_veiculo)

            if not veiculo:
                QMessageBox.warning(
                    self,
                    "Veículo não encontrado",
                    "Não foi possível localizar este veículo.",
                )
                return

            dialogo = QDialog(self)
            dialogo.setWindowTitle(f"Detalhes do veículo — {veiculo.placa}")
            dialogo.resize(680, 720)
            dialogo.setMinimumSize(560, 450)

            layout_dialogo = QVBoxLayout(dialogo)

            area_rolagem = QScrollArea()
            area_rolagem.setWidgetResizable(True)

            conteudo = QWidget()
            layout_conteudo = QVBoxLayout(conteudo)

            area_rolagem.setWidget(conteudo)
            layout_dialogo.addWidget(area_rolagem)

            def adicionar_unidade(titulo, unidade, campo_fk):
                grupo = QGroupBox(titulo)
                formulario = QFormLayout(grupo)

                if unidade is None:
                    formulario.addRow(QLabel("Nenhuma unidade vinculada."))
                    layout_conteudo.addWidget(grupo)
                    return

                if hasattr(unidade, "codigo_frota"):
                    formulario.addRow(
                        "Código da frota:",
                        QLabel(str(unidade.codigo_frota)),
                    )

                formulario.addRow(
                    "Placa:",
                    QLabel(str(unidade.placa)),
                )
                formulario.addRow(
                    "Marca:",
                    QLabel(str(unidade.marca)),
                )
                formulario.addRow(
                    "Modelo:",
                    QLabel(str(unidade.modelo)),
                )
                formulario.addRow(
                    "Ano:",
                    QLabel(str(unidade.ano)),
                )
                formulario.addRow(
                    "Tipo:",
                    QLabel(str(unidade.tipo)),
                )
                formulario.addRow(
                    "Status:",
                    QLabel(str(unidade.status)),
                )

                if hasattr(unidade, "configuracao"):
                    formulario.addRow(
                        "Configuração:",
                        QLabel(str(unidade.configuracao or "Sem composição")),
                    )

                documento = (
                    sessao.query(DocumentoVeiculo)
                    .filter(getattr(DocumentoVeiculo, campo_fk) == unidade.id)
                    .first()
                )

                if documento:
                    caminho = documento.caminho_arquivo

                    if os.path.isfile(caminho):
                        botao_abrir = QPushButton(
                            f"Abrir documento: {documento.nome_arquivo}"
                        )
                        botao_abrir.clicked.connect(
                            lambda checked=False, c=caminho: QDesktopServices.openUrl(
                                QUrl.fromLocalFile(c)
                            )
                        )
                        formulario.addRow("Documento:", botao_abrir)
                    else:
                        formulario.addRow(
                            "Documento:",
                            QLabel(
                                f"{documento.nome_arquivo} " "(arquivo não encontrado)"
                            ),
                        )
                else:
                    formulario.addRow(
                        "Documento:",
                        QLabel("Nenhum documento anexado."),
                    )

                layout_conteudo.addWidget(grupo)

            adicionar_unidade(
                "Cavalo mecânico",
                veiculo,
                "veiculo_id",
            )

            composicao = (
                sessao.query(Composicao)
                .filter(
                    Composicao.cavalo_id == veiculo.id,
                    Composicao.ativa.is_(True),
                )
                .first()
            )

            if composicao:
                grupo_configuracao = QGroupBox("Composição rodoviária")
                formulario_configuracao = QFormLayout(grupo_configuracao)
                formulario_configuracao.addRow(
                    "Configuração:",
                    QLabel(composicao.nome),
                )
                layout_conteudo.addWidget(grupo_configuracao)

                if composicao.carreta_1_id:
                    carreta_1 = sessao.get(
                        Carreta,
                        composicao.carreta_1_id,
                    )
                    adicionar_unidade(
                        "1ª carreta",
                        carreta_1,
                        "carreta_id",
                    )

                if composicao.dolly_id:
                    dolly = sessao.get(
                        Dolly,
                        composicao.dolly_id,
                    )
                    adicionar_unidade(
                        "Dolly",
                        dolly,
                        "dolly_id",
                    )

                if composicao.carreta_2_id:
                    carreta_2 = sessao.get(
                        Carreta,
                        composicao.carreta_2_id,
                    )
                    adicionar_unidade(
                        "2ª carreta",
                        carreta_2,
                        "carreta_id",
                    )
            else:
                layout_conteudo.addWidget(
                    QLabel("Este veículo não possui composição registrada.")
                )

            layout_conteudo.addStretch()

            botao_fechar = QPushButton("Fechar")
            botao_fechar.clicked.connect(dialogo.accept)
            layout_dialogo.addWidget(botao_fechar)

            dialogo.exec()

        except Exception as erro:
            QMessageBox.critical(
                self,
                "Erro ao carregar detalhes",
                f"Não foi possível carregar os detalhes.\n\n{erro}",
            )

        finally:
            sessao.close()

    def ver_detalhes_veiculo(self):
        linha = self.tabela.currentRow()

        if linha < 0:
            QMessageBox.warning(
                self,
                "Nenhum veículo selecionado",
                "Selecione um veículo para ver os detalhes.",
            )
            return

        item_codigo = self.tabela.item(linha, 0)

        if not item_codigo:
            return

        id_veiculo = item_codigo.data(Qt.UserRole)

        if not id_veiculo:
            return

        sessao = SessionLocal()

        try:
            veiculo = sessao.get(Veiculo, id_veiculo)

            if not veiculo:
                QMessageBox.warning(
                    self,
                    "Veículo não encontrado",
                    "Não foi possível localizar este veículo.",
                )
                return

            dialogo = QDialog(self)
            dialogo.setWindowTitle(f"Detalhes do veículo — {veiculo.placa}")
            dialogo.resize(680, 720)
            dialogo.setMinimumSize(560, 450)

            layout_dialogo = QVBoxLayout(dialogo)

            area_rolagem = QScrollArea()
            area_rolagem.setWidgetResizable(True)

            conteudo = QWidget()
            layout_conteudo = QVBoxLayout(conteudo)

            area_rolagem.setWidget(conteudo)
            layout_dialogo.addWidget(area_rolagem)

            def adicionar_unidade(titulo, unidade, campo_fk):
                grupo = QGroupBox(titulo)
                formulario = QFormLayout(grupo)

                if unidade is None:
                    formulario.addRow(QLabel("Nenhuma unidade vinculada."))
                    layout_conteudo.addWidget(grupo)
                    return

                if hasattr(unidade, "codigo_frota"):
                    formulario.addRow(
                        "Código da frota:",
                        QLabel(str(unidade.codigo_frota)),
                    )

                formulario.addRow(
                    "Placa:",
                    QLabel(str(unidade.placa)),
                )
                formulario.addRow(
                    "Marca:",
                    QLabel(str(unidade.marca)),
                )
                formulario.addRow(
                    "Modelo:",
                    QLabel(str(unidade.modelo)),
                )
                formulario.addRow(
                    "Ano:",
                    QLabel(str(unidade.ano)),
                )
                formulario.addRow(
                    "Tipo:",
                    QLabel(str(unidade.tipo)),
                )
                formulario.addRow(
                    "Status:",
                    QLabel(str(unidade.status)),
                )

                if hasattr(unidade, "configuracao"):
                    formulario.addRow(
                        "Configuração:",
                        QLabel(str(unidade.configuracao or "Sem composição")),
                    )

                documento = (
                    sessao.query(DocumentoVeiculo)
                    .filter(getattr(DocumentoVeiculo, campo_fk) == unidade.id)
                    .first()
                )

                if documento:
                    caminho = documento.caminho_arquivo

                    if os.path.isfile(caminho):
                        botao_abrir = QPushButton(
                            f"Abrir documento: {documento.nome_arquivo}"
                        )
                        botao_abrir.clicked.connect(
                            lambda checked=False, c=caminho: QDesktopServices.openUrl(
                                QUrl.fromLocalFile(c)
                            )
                        )
                        formulario.addRow("Documento:", botao_abrir)
                    else:
                        formulario.addRow(
                            "Documento:",
                            QLabel(
                                f"{documento.nome_arquivo} " "(arquivo não encontrado)"
                            ),
                        )
                else:
                    formulario.addRow(
                        "Documento:",
                        QLabel("Nenhum documento anexado."),
                    )

                layout_conteudo.addWidget(grupo)

            adicionar_unidade(
                "Cavalo mecânico",
                veiculo,
                "veiculo_id",
            )

            composicao = (
                sessao.query(Composicao)
                .filter(
                    Composicao.cavalo_id == veiculo.id,
                    Composicao.ativa.is_(True),
                )
                .first()
            )

            if composicao:
                grupo_configuracao = QGroupBox("Composição rodoviária")
                formulario_configuracao = QFormLayout(grupo_configuracao)
                formulario_configuracao.addRow(
                    "Configuração:",
                    QLabel(composicao.nome),
                )
                layout_conteudo.addWidget(grupo_configuracao)

                if composicao.carreta_1_id:
                    carreta_1 = sessao.get(
                        Carreta,
                        composicao.carreta_1_id,
                    )
                    adicionar_unidade(
                        "1ª carreta",
                        carreta_1,
                        "carreta_id",
                    )

                if composicao.dolly_id:
                    dolly = sessao.get(
                        Dolly,
                        composicao.dolly_id,
                    )
                    adicionar_unidade(
                        "Dolly",
                        dolly,
                        "dolly_id",
                    )

                if composicao.carreta_2_id:
                    carreta_2 = sessao.get(
                        Carreta,
                        composicao.carreta_2_id,
                    )
                    adicionar_unidade(
                        "2ª carreta",
                        carreta_2,
                        "carreta_id",
                    )
            else:
                layout_conteudo.addWidget(
                    QLabel("Este veículo não possui composição registrada.")
                )

            layout_conteudo.addStretch()

            botao_fechar = QPushButton("Fechar")
            botao_fechar.clicked.connect(dialogo.accept)
            layout_dialogo.addWidget(botao_fechar)

            dialogo.exec()

        except Exception as erro:
            QMessageBox.critical(
                self,
                "Erro ao carregar detalhes",
                f"Não foi possível carregar os detalhes.\n\n{erro}",
            )

        finally:
            sessao.close()

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
