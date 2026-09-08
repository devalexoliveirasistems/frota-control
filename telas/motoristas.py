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
    QDialog,
    QFormLayout,
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

        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)

        self.tabela.setColumnWidth(0, 60)
        self.tabela.setColumnWidth(1, 300)
        self.tabela.setColumnWidth(2, 150)
        self.tabela.setColumnWidth(3, 150)
        self.tabela.setColumnWidth(4, 120)
        linha_acoes = QHBoxLayout()

        botao_detalhes = QPushButton("Ver detalhes")
        botao_editar = QPushButton("Editar")

        botao_detalhes.clicked.connect(self.ver_detalhes)
        botao_editar.clicked.connect(self.editar_motorista)

        linha_acoes.addWidget(botao_detalhes)
        linha_acoes.addWidget(botao_editar)
        linha_acoes.addStretch()

        layout_principal.addLayout(linha_acoes)

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
        cep = self.campo_cep.text().strip()
        logradouro = self.campo_logradouro.text().strip()
        numero = self.campo_numero.text().strip()
        complemento = self.campo_complemento.text().strip()
        bairro = self.campo_bairro.text().strip()
        cidade = self.campo_cidade.text().strip()
        estado = self.campo_estado.text().strip()

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
                cep=cep or None,
                logradouro=logradouro or None,
                numero=numero or None,
                complemento=complemento or None,
                bairro=bairro or None,
                cidade=cidade or None,
                estado=estado or None,
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

    def ver_detalhes(self):
        linha = self.tabela.currentRow()

        if linha < 0:
            QMessageBox.warning(
                self,
                "Nenhum motorista selecionado",
                "Selecione um motorista na tabela.",
            )
            return

        item_id = self.tabela.item(linha, 0)

        if not item_id:
            return

        motorista_id = int(item_id.text())

        sessao = SessionLocal()

        try:
            motorista = sessao.get(Motorista, motorista_id)

            if not motorista:
                QMessageBox.warning(
                    self,
                    "Motorista não encontrado",
                    "Não foi possível localizar o motorista.",
                )
                return

            dialogo = QDialog(self)
            dialogo.setWindowTitle("Detalhes do Motorista")
            dialogo.resize(850, 500)

            layout_principal = QVBoxLayout(dialogo)

            titulo = QLabel("Detalhes do Motorista")
            titulo.setStyleSheet("""
                font-size: 22px;
                font-weight: bold;
                margin-bottom: 10px;
            """)
            layout_principal.addWidget(titulo)

            subtitulo = QLabel(f"{motorista.nome}  •  CPF: {motorista.cpf}")
            subtitulo.setStyleSheet("""
                font-size: 14px;
                color: #666;
                margin-bottom: 15px;
            """)
            layout_principal.addWidget(subtitulo)

            grade = QGridLayout()

            # =========================
            # DADOS PESSOAIS
            # =========================

            card_pessoais = QGroupBox("Dados Pessoais")
            layout_pessoais = QFormLayout()

            layout_pessoais.addRow("Nome:", QLabel(motorista.nome or "Não informado"))

            layout_pessoais.addRow("CPF:", QLabel(motorista.cpf or "Não informado"))

            layout_pessoais.addRow(
                "Telefone:", QLabel(motorista.telefone or "Não informado")
            )

            layout_pessoais.addRow(
                "Status:", QLabel(motorista.status or "Não informado")
            )

            card_pessoais.setLayout(layout_pessoais)

            # =========================
            # HABILITAÇÃO
            # =========================

            card_habilitacao = QGroupBox("Habilitação")
            layout_habilitacao = QFormLayout()

            categoria = motorista.categoria_cnh or "Não informada"

            validade = (
                motorista.validade_cnh.strftime("%d/%m/%Y")
                if motorista.validade_cnh
                else "Não informada"
            )

            layout_habilitacao.addRow("Categoria:", QLabel(categoria))

            layout_habilitacao.addRow("Validade:", QLabel(validade))

            layout_habilitacao.addRow(
                "CNH:",
                QLabel(
                    "Documento anexado"
                    if getattr(self, "caminho_cnh", None)
                    else "Não anexada"
                ),
            )

            card_habilitacao.setLayout(layout_habilitacao)

            # =========================
            # ENDEREÇO
            # =========================

            card_endereco = QGroupBox("Endereço")
            layout_endereco = QFormLayout()

            layout_endereco.addRow("CEP:", QLabel(motorista.cep or "Não informado"))

            layout_endereco.addRow(
                "Logradouro:", QLabel(motorista.logradouro or "Não informado")
            )

            layout_endereco.addRow(
                "Número:", QLabel(motorista.numero or "Não informado")
            )

            layout_endereco.addRow(
                "Complemento:", QLabel(motorista.complemento or "Não informado")
            )

            layout_endereco.addRow(
                "Bairro:", QLabel(motorista.bairro or "Não informado")
            )

            layout_endereco.addRow(
                "Cidade:", QLabel(motorista.cidade or "Não informado")
            )

            layout_endereco.addRow(
                "Estado:", QLabel(motorista.estado or "Não informado")
            )

            card_endereco.setLayout(layout_endereco)

            # =========================
            # GRID
            # =========================

            grade.addWidget(card_pessoais, 0, 0)
            grade.addWidget(card_habilitacao, 0, 1)
            grade.addWidget(card_endereco, 0, 2)

            grade.setColumnStretch(0, 1)
            grade.setColumnStretch(1, 1)
            grade.setColumnStretch(2, 1)

            layout_principal.addLayout(grade)

            # =========================
            # BOTÃO FECHAR
            # =========================

            linha_botao = QHBoxLayout()
            linha_botao.addStretch()

            botao_fechar = QPushButton("Fechar")
            botao_fechar.setMinimumWidth(120)
            botao_fechar.clicked.connect(dialogo.accept)

            linha_botao.addWidget(botao_fechar)

            layout_principal.addLayout(linha_botao)

            dialogo.exec()

        finally:
            sessao.close()

    def editar_motorista(self):
        linha = self.tabela.currentRow()

        if linha < 0:
            QMessageBox.warning(
                self,
                "Nenhum motorista selecionado",
                "Selecione um motorista na tabela.",
            )
            return

        item_id = self.tabela.item(linha, 0)

        if not item_id:
            return

        motorista_id = int(item_id.text())

        sessao = SessionLocal()

        try:
            motorista = sessao.get(Motorista, motorista_id)

            if not motorista:
                QMessageBox.warning(
                    self,
                    "Motorista não encontrado",
                    "Não foi possível localizar o motorista.",
                )
                return

            dialogo = QDialog(self)
            dialogo.setWindowTitle("Editar Motorista")
            dialogo.resize(900, 550)

            layout_principal = QVBoxLayout(dialogo)

            titulo = QLabel("Editar Motorista")
            titulo.setStyleSheet("""
                font-size: 22px;
                font-weight: bold;
                margin-bottom: 10px;
            """)
            layout_principal.addWidget(titulo)

            grade = QGridLayout()

            # =========================
            # DADOS PESSOAIS
            # =========================

            card_pessoais = QGroupBox("Dados Pessoais")
            layout_pessoais = QFormLayout()

            campo_nome = QLineEdit(motorista.nome or "")
            campo_cpf = QLineEdit(motorista.cpf or "")
            campo_telefone = QLineEdit(motorista.telefone or "")

            campo_status = QComboBox()
            campo_status.addItems(["Ativo", "Inativo"])

            indice_status = campo_status.findText(motorista.status or "Ativo")
            if indice_status >= 0:
                campo_status.setCurrentIndex(indice_status)

            layout_pessoais.addRow("Nome:", campo_nome)
            layout_pessoais.addRow("CPF:", campo_cpf)
            layout_pessoais.addRow("Telefone:", campo_telefone)
            layout_pessoais.addRow("Status:", campo_status)

            card_pessoais.setLayout(layout_pessoais)

            # =========================
            # HABILITAÇÃO
            # =========================

            card_habilitacao = QGroupBox("Habilitação")
            layout_habilitacao = QFormLayout()

            campo_categoria = QComboBox()
            campo_categoria.addItems(
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

            indice_categoria = campo_categoria.findText(
                motorista.categoria_cnh or "Selecione"
            )

            if indice_categoria >= 0:
                campo_categoria.setCurrentIndex(indice_categoria)

            campo_validade = QDateEdit()
            campo_validade.setCalendarPopup(True)

            if motorista.validade_cnh:
                campo_validade.setDate(
                    QDate(
                        motorista.validade_cnh.year,
                        motorista.validade_cnh.month,
                        motorista.validade_cnh.day,
                    )
                )
            else:
                campo_validade.setDate(QDate.currentDate())

            layout_habilitacao.addRow("Categoria:", campo_categoria)
            layout_habilitacao.addRow("Validade:", campo_validade)

            card_habilitacao.setLayout(layout_habilitacao)

            # =========================
            # ENDEREÇO
            # =========================

            card_endereco = QGroupBox("Endereço")
            layout_endereco = QFormLayout()

            campo_cep = QLineEdit(motorista.cep or "")
            campo_logradouro = QLineEdit(motorista.logradouro or "")
            campo_numero = QLineEdit(motorista.numero or "")
            campo_complemento = QLineEdit(motorista.complemento or "")
            campo_bairro = QLineEdit(motorista.bairro or "")
            campo_cidade = QLineEdit(motorista.cidade or "")
            campo_estado = QLineEdit(motorista.estado or "")

            layout_endereco.addRow("CEP:", campo_cep)
            layout_endereco.addRow("Logradouro:", campo_logradouro)
            layout_endereco.addRow("Número:", campo_numero)
            layout_endereco.addRow("Complemento:", campo_complemento)
            layout_endereco.addRow("Bairro:", campo_bairro)
            layout_endereco.addRow("Cidade:", campo_cidade)
            layout_endereco.addRow("Estado:", campo_estado)

            card_endereco.setLayout(layout_endereco)

            # =========================
            # CARDS
            # =========================

            grade.addWidget(card_pessoais, 0, 0)
            grade.addWidget(card_habilitacao, 0, 1)
            grade.addWidget(card_endereco, 0, 2)

            grade.setColumnStretch(0, 1)
            grade.setColumnStretch(1, 1)
            grade.setColumnStretch(2, 1)

            layout_principal.addLayout(grade)

            # =========================
            # BOTÕES
            # =========================

            linha_botoes = QHBoxLayout()
            linha_botoes.addStretch()

            botao_cancelar = QPushButton("Cancelar")
            botao_salvar = QPushButton("Salvar alterações")

            botao_cancelar.clicked.connect(dialogo.reject)

            linha_botoes.addWidget(botao_cancelar)
            linha_botoes.addWidget(botao_salvar)

            layout_principal.addLayout(linha_botoes)

            def salvar_alteracoes():
                nome = campo_nome.text().strip()
                cpf = campo_cpf.text().strip()

                if not nome:
                    QMessageBox.warning(
                        dialogo,
                        "Campo obrigatório",
                        "Informe o nome do motorista.",
                    )
                    return

                if not cpf:
                    QMessageBox.warning(
                        dialogo,
                        "Campo obrigatório",
                        "Informe o CPF do motorista.",
                    )
                    return

                motorista.nome = nome
                motorista.cpf = cpf
                motorista.telefone = campo_telefone.text().strip() or None
                motorista.status = campo_status.currentText()

                motorista.categoria_cnh = (
                    None
                    if campo_categoria.currentText() == "Selecione"
                    else campo_categoria.currentText()
                )

                motorista.validade_cnh = campo_validade.date().toPython()

                motorista.cep = campo_cep.text().strip() or None
                motorista.logradouro = campo_logradouro.text().strip() or None
                motorista.numero = campo_numero.text().strip() or None
                motorista.complemento = campo_complemento.text().strip() or None
                motorista.bairro = campo_bairro.text().strip() or None
                motorista.cidade = campo_cidade.text().strip() or None
                motorista.estado = campo_estado.text().strip() or None

                try:
                    sessao.commit()
                    self.carregar_motoristas()
                    dialogo.accept()

                    QMessageBox.information(
                        self,
                        "Alteração concluída",
                        "Motorista atualizado com sucesso.",
                    )

                except Exception as erro:
                    sessao.rollback()

                    QMessageBox.critical(
                        dialogo,
                        "Erro",
                        f"Não foi possível salvar as alterações:\n\n{erro}",
                    )

            botao_salvar.clicked.connect(salvar_alteracoes)

            dialogo.exec()

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
