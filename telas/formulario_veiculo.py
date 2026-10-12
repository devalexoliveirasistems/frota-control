from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QLineEdit,
    QSpinBox,
    QComboBox,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QGroupBox,
    QScrollArea,
    QWidget,
    QMessageBox,
    QFileDialog,
)

import shutil
from pathlib import Path
from banco.sessao import SessionLocal
from banco.modelos import (
    Veiculo,
    Carreta,
    Dolly,
    Composicao,
    DocumentoVeiculo,
)
from banco.repositorios.veiculo import cadastrar_veiculo, atualizar_veiculo
from PySide6.QtCore import Qt


class FormularioVeiculo(QDialog):
    def __init__(self, veiculo=None, parent=None):
        super().__init__(parent)

        self.veiculo = veiculo

        if self.veiculo:
            self.setWindowTitle("Editar veículo")
        else:
            self.setWindowTitle("Novo veículo")

        self.setMinimumSize(650, 500)
        self.resize(760, 680)

        layout = QFormLayout()
        self.layout_formulario = layout
        layout.setContentsMargins(24, 24, 24, 22)
        layout.setHorizontalSpacing(16)
        layout.setVerticalSpacing(14)

        self.campo_placa = QLineEdit()
        self.campo_placa_carreta_1 = QLineEdit()
        self.campo_placa_dolly = QLineEdit()
        self.campo_placa_carreta_2 = QLineEdit()

        self.campo_marca = QLineEdit()
        self.campo_modelo = QLineEdit()

        self.campo_ano = QSpinBox()
        self.campo_ano.setRange(1900, 2100)
        self.campo_ano.setValue(2026)

        self.campo_tipo = QComboBox()
        self.campo_tipo.addItems(
            [
                "Caminhão",
                "Caminhão-trator",
                "Carreta simples",
                "Bitrem",
                "Rodotrem",
                "Toco",
                "Truck",
                "Bitruck",
                "Caminhão leve (VUC / 3/4)",
                "Van",
                "Micro-ônibus",
                "Ônibus",
                "Carro",
                "Motocicleta",
                "Caminhonete / Pickup",
                "Utilitário",
                "Furgão",
                "Outro",
            ]
        )

        self.campo_configuracao = QComboBox()
        self.campo_configuracao.addItems(
            [
                "Sem composição",
                "Carreta simples",
                "Bitrem",
                "Rodotrem",
            ]
        )

        self.campo_status = QComboBox()
        self.campo_status.addItems(
            [
                "Ativo",
                "Em manutenção",
                "Inativo",
                "Vendido",
            ]
        )

        self.campo_documento = QLineEdit()
        self.campo_documento.setReadOnly(True)
        self.campo_documento.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff;
                color: #1e293b;
                border: 1px solid #60a5fa;
                border-radius: 7px;
                padding: 7px 10px;
                min-height: 24px;
                font-size: 14px;
            }
        """)

        botao_documento_veiculo = QPushButton("Selecionar arquivo")
        botao_documento_veiculo.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #1e293b;
                border: 1px solid #60a5fa;
                border-radius: 7px;
                padding: 7px 12px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #eff6ff;
                border-color: #2563eb;
            }
        """)
        botao_documento_veiculo.clicked.connect(
            lambda checked=False: self.selecionar_documento(self.campo_documento)
        )

        self.linha_documento_veiculo = QHBoxLayout()
        self.linha_documento_veiculo.addWidget(self.campo_documento, 1)
        self.linha_documento_veiculo.addWidget(botao_documento_veiculo)

        self.grupo_carreta_1, self.campos_carreta_1 = self.criar_grupo_unidade(
            "1ª carreta"
        )
        self.grupo_dolly, self.campos_dolly = self.criar_grupo_unidade("Dolly")
        self.grupo_carreta_2, self.campos_carreta_2 = self.criar_grupo_unidade(
            "2ª carreta"
        )

        self.setStyleSheet("""
            QDialog {
                background-color: #f8fafc;
            }

            QLabel {
                color: #334155;
                font-size: 14px;
                font-weight: 700;
            }

            QLineEdit, QSpinBox, QComboBox {
                background-color: #ffffff;
                color: #1e293b;
                border: 1px solid #cbd5e1;
                border-radius: 7px;
                padding: 7px 10px;
                min-height: 24px;
                font-size: 14px;
            }

            QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
                border: 1px solid #60a5fa;
            }
        """)

        if self.veiculo:
            self.campo_placa.setText(self.veiculo.placa)
            self.campo_marca.setText(self.veiculo.marca)
            self.campo_modelo.setText(self.veiculo.modelo)
            self.campo_ano.setValue(self.veiculo.ano)

            indice_status = self.campo_status.findText(self.veiculo.status)

            if indice_status >= 0:
                self.campo_status.setCurrentIndex(indice_status)

            tipo_para_edicao = self.veiculo.tipo

            if self.veiculo.configuracao in (
                "Carreta simples",
                "Bitrem",
                "Rodotrem",
            ):
                tipo_para_edicao = self.veiculo.configuracao
            elif self.veiculo.configuracao == "Cavalo":
                tipo_para_edicao = "Caminhão-trator"

            indice = self.campo_tipo.findText(tipo_para_edicao)

            if indice >= 0:
                self.campo_tipo.setCurrentIndex(indice)

        layout.addRow("Tipo:", self.campo_tipo)
        layout.addRow("Placa:", self.campo_placa)
        layout.addRow("Marca:", self.campo_marca)
        layout.addRow("Modelo:", self.campo_modelo)
        layout.addRow("Ano:", self.campo_ano)
        layout.addRow("Status:", self.campo_status)
        layout.addRow("Documento:", self.linha_documento_veiculo)

        self.grupo_carreta_1.setVisible(False)
        self.grupo_dolly.setVisible(False)
        self.grupo_carreta_2.setVisible(False)

        layout.addRow(self.grupo_carreta_1)
        layout.addRow(self.grupo_dolly)
        layout.addRow(self.grupo_carreta_2)

        linha_botoes = QHBoxLayout()

        botao_cancelar = QPushButton("Cancelar")
        botao_salvar = QPushButton("Salvar")

        botao_cancelar.setMinimumHeight(40)
        botao_cancelar.setCursor(Qt.CursorShape.PointingHandCursor)
        botao_cancelar.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #475569;
                border: 1px solid #cbd5e1;
                border-radius: 7px;
                padding: 8px 18px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #f1f5f9;
            }
        """)

        botao_salvar.setMinimumHeight(40)
        botao_salvar.setCursor(Qt.CursorShape.PointingHandCursor)
        botao_salvar.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: #ffffff;
                border: 1px solid #2563eb;
                border-radius: 7px;
                padding: 8px 18px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
                border-color: #1d4ed8;
            }
        """)

        linha_botoes.addWidget(botao_cancelar)
        linha_botoes.addWidget(botao_salvar)

        conteudo = QWidget()
        conteudo.setLayout(layout)

        area_rolagem = QScrollArea()
        area_rolagem.setWidgetResizable(True)
        area_rolagem.setWidget(conteudo)

        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(16, 16, 16, 16)
        layout_principal.setSpacing(12)
        layout_principal.addWidget(area_rolagem)
        layout_principal.addLayout(linha_botoes)

        self.setLayout(layout_principal)

        for campo in (
            self.campo_placa_carreta_1,
            self.campo_placa_dolly,
            self.campo_placa_carreta_2,
        ):
            campo.setVisible(False)
            rotulo = layout.labelForField(campo)
            if rotulo:
                rotulo.setVisible(False)

        botao_cancelar.clicked.connect(self.reject)
        botao_salvar.clicked.connect(self.salvar)

        self.campo_tipo.currentTextChanged.connect(self.atualizar_campos_composicao)
        self.atualizar_campos_composicao()
        self.carregar_composicao_existente()

    def atualizar_campos_composicao(self):
        tipo = self.campo_tipo.currentText()

        mostrar_carreta_1 = tipo in (
            "Carreta simples",
            "Bitrem",
            "Rodotrem",
        )

        mostrar_dolly = tipo == "Rodotrem"
        mostrar_carreta_2 = tipo in ("Bitrem", "Rodotrem")

        self.grupo_carreta_1.setVisible(mostrar_carreta_1)
        self.grupo_dolly.setVisible(mostrar_dolly)
        self.grupo_carreta_2.setVisible(mostrar_carreta_2)

        rotulo_placa = self.layout_formulario.labelForField(self.campo_placa)

        if rotulo_placa:
            if tipo in (
                "Caminhão-trator",
                "Carreta simples",
                "Bitrem",
                "Rodotrem",
            ):
                rotulo_placa.setText("Placa do cavalo:")
            else:
                rotulo_placa.setText("Placa:")

    def criar_grupo_unidade(self, titulo):
        grupo = QGroupBox(titulo)
        layout = QFormLayout(grupo)

        layout.setHorizontalSpacing(12)
        layout.setVerticalSpacing(8)

        campos = {
            "placa": QLineEdit(),
            "marca": QLineEdit(),
            "modelo": QLineEdit(),
            "ano": QSpinBox(),
            "status": QComboBox(),
            "documento": QLineEdit(),
        }

        campos["ano"].setRange(1900, 2100)
        campos["ano"].setValue(2026)

        campos["status"].addItems(
            [
                "Ativo",
                "Em manutenção",
                "Inativo",
                "Vendido",
            ]
        )

        campos["documento"].setReadOnly(True)
        campos["documento"].setStyleSheet("""
            QLineEdit {
                background-color: #ffffff;
                color: #1e293b;
                border: 1px solid #60a5fa;
                border-radius: 7px;
                padding: 7px 10px;
                min-height: 24px;
                font-size: 14px;
            }
        """)

        botao_documento = QPushButton("Selecionar arquivo")
        botao_documento.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #1e293b;
                border: 1px solid #60a5fa;
                border-radius: 7px;
                padding: 7px 12px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #eff6ff;
                border-color: #2563eb;
            }
        """)
        botao_documento.clicked.connect(
            lambda checked=False, campo=campos["documento"]: self.selecionar_documento(
                campo
            )
        )

        linha_documento = QHBoxLayout()
        linha_documento.addWidget(campos["documento"], 1)
        linha_documento.addWidget(botao_documento)

        layout.addRow("Placa:", campos["placa"])
        layout.addRow("Marca:", campos["marca"])
        layout.addRow("Modelo:", campos["modelo"])
        layout.addRow("Ano:", campos["ano"])
        layout.addRow("Status:", campos["status"])
        layout.addRow("Documento:", linha_documento)

        return grupo, campos

    def selecionar_documento(self, campo):
        caminho, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar documento",
            "",
            "Documentos e imagens (*.pdf *.png *.jpg *.jpeg);;Todos os arquivos (*.*)",
        )

        if caminho:
            campo.setText(caminho)
            campo.setToolTip(caminho)

    def obter_dados_unidade(self, campos, titulo):
        placa = campos["placa"].text().strip().upper().replace("-", "").replace(" ", "")
        marca = campos["marca"].text().strip()
        modelo = campos["modelo"].text().strip()

        if len(placa) != 7 or not placa.isalnum():
            QMessageBox.warning(
                self,
                "Placa inválida",
                f"Informe uma placa válida para {titulo}, com 7 caracteres.",
            )
            return None

        if not marca:
            QMessageBox.warning(
                self,
                "Marca obrigatória",
                f"Informe a marca de {titulo}.",
            )
            return None

        if not modelo:
            QMessageBox.warning(
                self,
                "Modelo obrigatório",
                f"Informe o modelo de {titulo}.",
            )
            return None

        return {
            "placa": placa,
            "marca": marca,
            "modelo": modelo,
            "ano": campos["ano"].value(),
            "status": campos["status"].currentText(),
        }

    def salvar_unidade_composicao(
        self,
        sessao,
        classe_unidade,
        dados,
        unidade_id=None,
        tipo_unidade="Carreta",
    ):
        if dados is None:
            return None

        unidade = (
            sessao.get(classe_unidade, unidade_id) if unidade_id is not None else None
        )

        if unidade is None:
            unidade = classe_unidade(
                placa=dados["placa"],
                marca=dados["marca"],
                modelo=dados["modelo"],
                ano=dados["ano"],
                tipo=tipo_unidade,
                status=dados["status"],
            )
            sessao.add(unidade)
        else:
            unidade.placa = dados["placa"]
            unidade.marca = dados["marca"]
            unidade.modelo = dados["modelo"]
            unidade.ano = dados["ano"]
            unidade.tipo = tipo_unidade
            unidade.status = dados["status"]

        sessao.flush()
        return unidade

    def salvar_composicao(
        self,
        sessao,
        veiculo,
        configuracao,
        dados_carreta_1,
        dados_carreta_2,
        dados_dolly,
    ):
        composicao = (
            sessao.query(Composicao)
            .filter(
                Composicao.cavalo_id == veiculo.id,
                Composicao.ativa.is_(True),
            )
            .first()
        )

        configuracoes_validas = (
            "Carreta simples",
            "Bitrem",
            "Rodotrem",
        )

        if configuracao not in configuracoes_validas:
            if composicao:
                composicao.ativa = False
            return

        if composicao is None:
            composicao = Composicao(
                nome=configuracao,
                cavalo_id=veiculo.id,
                ativa=True,
            )
            sessao.add(composicao)
            sessao.flush()

        carreta_1 = self.salvar_unidade_composicao(
            sessao,
            Carreta,
            dados_carreta_1,
            composicao.carreta_1_id,
            "Carreta",
        )

        carreta_2 = self.salvar_unidade_composicao(
            sessao,
            Carreta,
            dados_carreta_2,
            composicao.carreta_2_id,
            "Carreta",
        )

        dolly = self.salvar_unidade_composicao(
            sessao,
            Dolly,
            dados_dolly,
            composicao.dolly_id,
            "Dolly",
        )

        if carreta_1:
            self.salvar_documento_unidade(
                sessao=sessao,
                campo=self.campos_carreta_1["documento"],
                campo_fk="carreta_id",
                unidade_id=carreta_1.id,
            )

        if carreta_2:
            self.salvar_documento_unidade(
                sessao=sessao,
                campo=self.campos_carreta_2["documento"],
                campo_fk="carreta_id",
                unidade_id=carreta_2.id,
            )

        if dolly:
            self.salvar_documento_unidade(
                sessao=sessao,
                campo=self.campos_dolly["documento"],
                campo_fk="dolly_id",
                unidade_id=dolly.id,
            )

        composicao.nome = configuracao
        composicao.carreta_1_id = carreta_1.id if carreta_1 else None
        composicao.carreta_2_id = carreta_2.id if carreta_2 else None
        composicao.dolly_id = dolly.id if dolly else None
        composicao.ativa = True

        sessao.flush()

    def validar_placas_no_banco(
        self,
        sessao,
        placa_principal,
        dados_carreta_1,
        dados_carreta_2,
        dados_dolly,
    ):
        composicao_atual = None

        if self.veiculo:
            composicao_atual = (
                sessao.query(Composicao)
                .filter(
                    Composicao.cavalo_id == self.veiculo.id,
                    Composicao.ativa.is_(True),
                )
                .first()
            )

        id_carreta_1 = composicao_atual.carreta_1_id if composicao_atual else None
        id_carreta_2 = composicao_atual.carreta_2_id if composicao_atual else None
        id_dolly = composicao_atual.dolly_id if composicao_atual else None

        unidades = [
            (
                placa_principal,
                Veiculo,
                self.veiculo.id if self.veiculo else None,
                "cavalo",
            ),
        ]

        if dados_carreta_1:
            unidades.append(
                (dados_carreta_1["placa"], Carreta, id_carreta_1, "1ª carreta")
            )

        if dados_carreta_2:
            unidades.append(
                (dados_carreta_2["placa"], Carreta, id_carreta_2, "2ª carreta")
            )

        if dados_dolly:
            unidades.append((dados_dolly["placa"], Dolly, id_dolly, "Dolly"))

        for placa, classe_esperada, id_permitido, titulo in unidades:
            for classe in (Veiculo, Carreta, Dolly):
                existente = sessao.query(classe).filter(classe.placa == placa).first()

                if existente is None:
                    continue

                if classe is classe_esperada and existente.id == id_permitido:
                    continue

                QMessageBox.warning(
                    self,
                    "Placa já cadastrada",
                    f"A placa {placa} informada para {titulo} "
                    "já pertence a outra unidade da frota.",
                )
                return False

        return True

    def salvar_documento_unidade(
        self,
        sessao,
        campo,
        campo_fk,
        unidade_id,
    ):
        caminho_selecionado = campo.text().strip()

        if not caminho_selecionado:
            return

        origem = Path(caminho_selecionado)

        if not origem.is_file():
            raise FileNotFoundError(
                f"O documento selecionado não foi encontrado: {origem}"
            )

        nome_pasta = campo_fk.replace("_id", "")
        pasta_destino = (
            Path(__file__).resolve().parents[1]
            / "documentos"
            / "veiculos"
            / nome_pasta
            / str(unidade_id)
        )

        pasta_destino.mkdir(parents=True, exist_ok=True)
        destino = pasta_destino / origem.name

        if origem.resolve() != destino.resolve():
            shutil.copy2(origem, destino)

        documento = (
            sessao.query(DocumentoVeiculo)
            .filter(getattr(DocumentoVeiculo, campo_fk) == unidade_id)
            .first()
        )

        if documento is None:
            documento = DocumentoVeiculo(
                nome_arquivo=origem.name,
                caminho_arquivo=str(destino),
                **{campo_fk: unidade_id},
            )
            sessao.add(documento)
        else:
            documento.nome_arquivo = origem.name
            documento.caminho_arquivo = str(destino)

        campo.setText(str(destino))
        campo.setToolTip(str(destino))

    def carregar_composicao_existente(self):
        if not self.veiculo:
            return

        sessao = SessionLocal()

        try:
            veiculo = sessao.get(Veiculo, self.veiculo.id)

            if not veiculo:
                return

            documento = (
                sessao.query(DocumentoVeiculo).filter_by(veiculo_id=veiculo.id).first()
            )

            if documento:
                self.campo_documento.setText(documento.caminho_arquivo)

            composicao = (
                sessao.query(Composicao)
                .filter(
                    Composicao.cavalo_id == veiculo.id,
                    Composicao.ativa.is_(True),
                )
                .first()
            )

            if not composicao:
                return

            indice = self.campo_tipo.findText(composicao.nome)

            if indice >= 0:
                self.campo_tipo.setCurrentIndex(indice)

            unidades = [
                (
                    composicao.carreta_1_id,
                    Carreta,
                    self.campos_carreta_1,
                    "carreta_id",
                ),
                (
                    composicao.dolly_id,
                    Dolly,
                    self.campos_dolly,
                    "dolly_id",
                ),
                (
                    composicao.carreta_2_id,
                    Carreta,
                    self.campos_carreta_2,
                    "carreta_id",
                ),
            ]

            for unidade_id, classe, campos, campo_fk in unidades:
                if unidade_id is None:
                    continue

                unidade = sessao.get(classe, unidade_id)

                if not unidade:
                    continue

                campos["placa"].setText(unidade.placa)
                campos["marca"].setText(unidade.marca)
                campos["modelo"].setText(unidade.modelo)
                campos["ano"].setValue(unidade.ano)

                indice_status = campos["status"].findText(unidade.status)

                if indice_status >= 0:
                    campos["status"].setCurrentIndex(indice_status)

                documento = (
                    sessao.query(DocumentoVeiculo)
                    .filter(getattr(DocumentoVeiculo, campo_fk) == unidade_id)
                    .first()
                )

                if documento:
                    campos["documento"].setText(documento.caminho_arquivo)

        finally:
            sessao.close()

    def salvar(self):
        placa = (
            self.campo_placa.text().strip().upper().replace("-", "").replace(" ", "")
        )
        if len(placa) != 7 or not placa.isalnum():
            QMessageBox.warning(
                self,
                "Placa inválida",
                "Informe uma placa válida com 7 caracteres.",
            )
            return
        marca = self.campo_marca.text().strip()
        modelo = self.campo_modelo.text().strip()
        ano = self.campo_ano.value()

        tipo_selecionado = self.campo_tipo.currentText()

        if tipo_selecionado in (
            "Caminhão-trator",
            "Carreta simples",
            "Bitrem",
            "Rodotrem",
        ):
            tipo = "Caminhão-trator"

            if tipo_selecionado == "Caminhão-trator":
                configuracao = "Cavalo"
            else:
                configuracao = tipo_selecionado
        else:
            tipo = tipo_selecionado
            configuracao = "Sem composição"

        status = self.campo_status.currentText()

        if not placa:
            QMessageBox.warning(
                self,
                "Placa obrigatória",
                "Informe a placa do veículo.",
            )
            return

        if not marca:
            QMessageBox.warning(
                self,
                "Marca obrigatória",
                "Informe a marca do veículo.",
            )
            return

        if not modelo:
            QMessageBox.warning(
                self,
                "Modelo obrigatório",
                "Informe o modelo do veículo.",
            )
            return

        dados_carreta_1 = None
        dados_carreta_2 = None
        dados_dolly = None

        if configuracao in ("Carreta simples", "Bitrem", "Rodotrem"):
            dados_carreta_1 = self.obter_dados_unidade(
                self.campos_carreta_1,
                "1ª carreta",
            )
            if dados_carreta_1 is None:
                return

        if configuracao in ("Bitrem", "Rodotrem"):
            dados_carreta_2 = self.obter_dados_unidade(
                self.campos_carreta_2,
                "2ª carreta",
            )
            if dados_carreta_2 is None:
                return

        if configuracao == "Rodotrem":
            dados_dolly = self.obter_dados_unidade(
                self.campos_dolly,
                "Dolly",
            )
            if dados_dolly is None:
                return

        placas_informadas = [placa]

        for dados in (
            dados_carreta_1,
            dados_carreta_2,
            dados_dolly,
        ):
            if dados is not None:
                placas_informadas.append(dados["placa"])

        if len(placas_informadas) != len(set(placas_informadas)):
            QMessageBox.warning(
                self,
                "Placas repetidas",
                "Cada veículo ou implemento deve ter uma placa diferente.",
            )
            return

        sessao = SessionLocal()

        veiculo_existente = sessao.query(Veiculo).filter(Veiculo.placa == placa).first()

        if veiculo_existente and (
            not self.veiculo or veiculo_existente.id != self.veiculo.id
        ):
            QMessageBox.warning(
                self,
                "Placa já cadastrada",
                f"A placa {placa} já está cadastrada em outro veículo.",
            )
            sessao.close()
            return

        try:
            if not self.validar_placas_no_banco(
                sessao=sessao,
                placa_principal=placa,
                dados_carreta_1=dados_carreta_1,
                dados_carreta_2=dados_carreta_2,
                dados_dolly=dados_dolly,
            ):
                return

            if self.veiculo:
                veiculo = (
                    sessao.query(Veiculo).filter(Veiculo.id == self.veiculo.id).first()
                )

                if not veiculo:
                    return

                atualizar_veiculo(
                    sessao=sessao,
                    veiculo=veiculo,
                    placa=placa,
                    marca=marca,
                    modelo=modelo,
                    ano=ano,
                    tipo=tipo,
                    status=status,
                    configuracao=configuracao,
                    commit=False,
                )

            else:
                veiculo = cadastrar_veiculo(
                    sessao=sessao,
                    placa=placa,
                    marca=marca,
                    modelo=modelo,
                    ano=ano,
                    tipo=tipo,
                    status=status,
                    configuracao=configuracao,
                    commit=False,
                )

            self.salvar_composicao(
                sessao=sessao,
                veiculo=veiculo,
                configuracao=configuracao,
                dados_carreta_1=dados_carreta_1,
                dados_carreta_2=dados_carreta_2,
                dados_dolly=dados_dolly,
            )

            self.salvar_documento_unidade(
                sessao=sessao,
                campo=self.campo_documento,
                campo_fk="veiculo_id",
                unidade_id=veiculo.id,
            )

            sessao.commit()
            self.accept()

        except Exception as erro:
            sessao.rollback()
            QMessageBox.critical(
                self,
                "Erro ao salvar",
                f"Não foi possível salvar o veículo e a composição.\n\n"
                f"Detalhes: {erro}",
            )

        finally:
            sessao.close()
