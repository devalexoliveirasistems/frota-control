from PySide6.QtCore import QEvent, QLocale, QTimer, Qt
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QAbstractSpinBox,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QGroupBox,
    QLabel,
    QDoubleSpinBox,
    QPushButton,
    QFrame,
    QScrollArea,
)

from datetime import datetime

from PySide6.QtGui import (
    QColor,
    QFont,
    QPainter,
    QPdfWriter,
    QPageSize,
)

from PySide6.QtWidgets import QFileDialog, QMessageBox


class CampoNumerico(QDoubleSpinBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._ja_digitou = False
        self._duplo_clique = False

        self.setKeyboardTracking(False)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.UpDownArrows)

        self.lineEdit().installEventFilter(self)
        self.lineEdit().textEdited.connect(self.marcar_como_editado)

    def marcar_como_editado(self, texto):
        self._ja_digitou = True

    def limites_numericos(self):
        editor = self.lineEdit()
        texto = editor.text()

        inicio = (
            len(self.prefix())
            if self.prefix() and texto.startswith(self.prefix())
            else 0
        )

        fim = (
            len(texto) - len(self.suffix())
            if self.suffix() and texto.endswith(self.suffix())
            else len(texto)
        )

        return inicio, max(inicio, fim)

    def selecionar_numero(self):
        inicio, fim = self.limites_numericos()

        if fim > inicio:
            self.lineEdit().setSelection(inicio, fim - inicio)

    def posicionar_cursor(self, posicao):
        inicio, fim = self.limites_numericos()
        posicao = max(inicio, min(posicao, fim))

        editor = self.lineEdit()
        editor.deselect()
        editor.setCursorPosition(posicao)

    def eventFilter(self, objeto, evento):
        editor = self.lineEdit()

        if objeto is editor:

            if evento.type() == QEvent.Type.MouseButtonPress:
                self._duplo_clique = False
                return False

            if evento.type() == QEvent.Type.MouseButtonDblClick:
                self._duplo_clique = True
                QTimer.singleShot(0, self.selecionar_numero)
                return True

            if evento.type() == QEvent.Type.MouseButtonRelease:
                if self._duplo_clique:
                    QTimer.singleShot(0, self.selecionar_numero)
                    self._duplo_clique = False
                    return True

                if not self._ja_digitou:
                    QTimer.singleShot(0, self.selecionar_numero)
                else:
                    QTimer.singleShot(
                        0,
                        lambda: self.posicionar_cursor(editor.cursorPosition()),
                    )

                return False

            if evento.type() == QEvent.Type.KeyPress:
                texto = evento.text()
                separador = self.locale().decimalPoint()

                if (
                    not self._ja_digitou
                    and self.value() == 0
                    and texto in (separador, ".", ",")
                ):
                    inicio, _ = self.limites_numericos()

                    editor.setText(self.prefix() + "0" + separador + self.suffix())
                    editor.setCursorPosition(inicio + 2)
                    self._ja_digitou = True
                    return True

                if (
                    texto and (texto.isdigit() or texto in (separador, ".", ","))
                ) or evento.key() in (
                    Qt.Key.Key_Backspace,
                    Qt.Key.Key_Delete,
                ):
                    self._ja_digitou = True

        return super().eventFilter(objeto, evento)

    def resetar_edicao(self):
        self._ja_digitou = False
        self._duplo_clique = False


class SimuladorFretes(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("paginaSimulador")

        self.setStyleSheet("""
            QWidget#paginaSimulador {
                background-color: #f1f5f9;
            }

            QWidget#conteudoSimulador {
                background-color: #f1f5f9;
            }

            QFrame#cabecalho {
                background-color: #172554;
                border-radius: 12px;
            }

            QLabel#titulo {
                color: #ffffff;
                font-size: 26px;
                font-weight: 800;
                background: transparent;
            }

            QLabel#subtitulo {
                color: #cbd5e1;
                font-size: 14px;
                background: transparent;
            }

            QGroupBox {
                background-color: #ffffff;
                color: #172033;
                border: 1px solid #dbe2ea;
                border-radius: 10px;
                margin-top: 15px;
                padding: 18px 14px 14px 14px;
                font-size: 14px;
                font-weight: 700;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
                background-color: #ffffff;
                color: #1d4ed8;
                font-size: 15px;
                font-weight: 800;
            }

            QLabel#rotuloCampo {
                color: #0f172a;
                font-size: 14px;
                font-weight: 800;
                background-color: transparent;
                padding: 2px 0;
            }

            QDoubleSpinBox {
                background-color: #ffffff;
                color: #0b1220;
                border: 1px solid #94a3b8;
                border-radius: 7px;
                padding: 8px;
                min-height: 25px;
                font-size: 16px;
                font-weight: 800;
            }

            QDoubleSpinBox:focus {
                border: 1px solid #2563eb;
                background-color: #f8fbff;
            }

            QLabel#tituloSecao {
                color: #172033;
                font-size: 19px;
                font-weight: 800;
                background: transparent;
            }

            QFrame#cartaoResumo {
                background-color: #ffffff;
                border: 1px solid #dbe2ea;
                border-radius: 10px;
            }

            QFrame#cartaoFrete {
                background-color: #eff6ff;
                border: 1px solid #bfdbfe;
                border-radius: 10px;
            }

            QFrame#cartaoCusto {
                background-color: #fff7ed;
                border: 1px solid #fed7aa;
                border-radius: 10px;
            }

            QFrame#cartaoLucro {
                background-color: #ecfdf5;
                border: 1px solid #a7f3d0;
                border-radius: 10px;
            }

            QFrame#cartaoDetalhe {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 9px;
            }

            QLabel#rotuloResumo {
                color: #334155;
                font-size: 13px;
                font-weight: 800;
                background-color: transparent;
            }

            QLabel#rotuloResumoDestaque {
                color: #1e293b;
                font-size: 15px;
                font-weight: 800;
                background-color: transparent;
            }

            QLabel#valorResumo {
                color: #0f172a;
                font-size: 21px;
                font-weight: 800;
                background: transparent;
            }

            QLabel#valorFrete {
                color: #1d4ed8;
                font-size: 21px;
                font-weight: 800;
                background: transparent;
            }

            QLabel#valorCusto {
                color: #c2410c;
                font-size: 21px;
                font-weight: 800;
                background: transparent;
            }

            QLabel#valorLucro {
                color: #047857;
                font-size: 23px;
                font-weight: 800;
                background: transparent;
            }

            QLabel#valorDetalhe {
                color: #0f172a;
                font-size: 16px;
                font-weight: 800;
                background: transparent;
            }

            QLabel#aviso {
                color: #475569;
                font-size: 13px;
                background: transparent;
            }

            QPushButton#calcular {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 7px;
                padding: 11px 22px;
                font-size: 14px;
                font-weight: 700;
            }

            QPushButton#calcular:hover {
                background-color: #1d4ed8;
            }

            QPushButton#limpar {
                background-color: #e2e8f0;
                color: #334155;
                border: 1px solid #cbd5e1;
                border-radius: 7px;
                padding: 11px 20px;
                font-size: 14px;
                font-weight: 700;
            }

            QPushButton#limpar:hover {
                background-color: #cbd5e1;
            }

            QScrollArea {
                border: none;
                background-color: #f1f5f9;
            }
        """)

        layout_externo = QVBoxLayout(self)
        layout_externo.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(
            __import__(
                "PySide6.QtCore", fromlist=["Qt"]
            ).Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        conteudo = QWidget()
        conteudo.setObjectName("conteudoSimulador")

        principal = QVBoxLayout(conteudo)
        principal.setContentsMargins(24, 20, 24, 24)
        principal.setSpacing(14)

        # CABEÇALHO
        cabecalho = QFrame()
        cabecalho.setObjectName("cabecalho")
        layout_cabecalho = QVBoxLayout(cabecalho)
        layout_cabecalho.setContentsMargins(22, 20, 22, 20)
        layout_cabecalho.setSpacing(7)

        titulo = QLabel("Simulador de Lucro por Frete")
        titulo.setObjectName("titulo")

        subtitulo = QLabel("Analise os custos da viagem antes de aceitar o frete.")
        subtitulo.setObjectName("subtitulo")
        subtitulo.setWordWrap(True)

        layout_cabecalho.addWidget(titulo)
        layout_cabecalho.addWidget(subtitulo)
        principal.addWidget(cabecalho)

        # CAMPOS
        linha_grupos = QHBoxLayout()
        linha_grupos.setSpacing(14)

        grupo_vazio = QGroupBox("1. Deslocamento vazio até o embarque")
        grade_vazio = QGridLayout(grupo_vazio)
        grade_vazio.setContentsMargins(14, 22, 14, 16)
        grade_vazio.setHorizontalSpacing(14)
        grade_vazio.setVerticalSpacing(12)

        self.km_vazio = self.criar_campo(1, 10, sufixo=" km")
        self.consumo_vazio = self.criar_campo(2, 0.1, sufixo=" km/L")
        self.preco_diesel = self.criar_campo(3, 0.1, prefixo="R$ ")
        self.pedagios_vazio = self.criar_campo(2, 10, prefixo="R$ ")

        campos_vazios = [
            ("Distância até o embarque", self.km_vazio),
            ("Consumo médio vazio", self.consumo_vazio),
            ("Preço do diesel por litro", self.preco_diesel),
            ("Pedágios até o embarque", self.pedagios_vazio),
        ]

        for i, (nome, campo) in enumerate(campos_vazios):
            self.adicionar_campo(grade_vazio, i // 2, i % 2, nome, campo)

        grupo_frete = QGroupBox("2. Frete contratado")
        grade_frete = QGridLayout(grupo_frete)
        grade_frete.setContentsMargins(14, 22, 14, 16)
        grade_frete.setHorizontalSpacing(14)
        grade_frete.setVerticalSpacing(12)

        self.frete = self.criar_campo(2, 100, prefixo="R$ ")
        self.km_carregado = self.criar_campo(1, 10, sufixo=" km")
        self.consumo_carregado = self.criar_campo(2, 0.1, sufixo=" km/L")
        self.pedagios_frete = self.criar_campo(2, 10, prefixo="R$ ")
        self.outras_despesas = self.criar_campo(2, 10, prefixo="R$ ")
        self.comissao = self.criar_campo(2, 0.5, sufixo=" %")
        self.comissao.setValue(11)

        campos_frete = [
            ("Valor bruto do frete", self.frete),
            ("Distância do trajeto contratado", self.km_carregado),
            ("Consumo médio carregado", self.consumo_carregado),
            ("Pedágios do trajeto contratado", self.pedagios_frete),
            ("Outras despesas da operação", self.outras_despesas),
            ("Comissão do motorista", self.comissao),
        ]

        for i, (nome, campo) in enumerate(campos_frete):
            self.adicionar_campo(grade_frete, i // 2, i % 2, nome, campo)

        linha_grupos.addWidget(grupo_vazio, 1)
        linha_grupos.addWidget(grupo_frete, 1)
        principal.addLayout(linha_grupos)

        # RESUMO FINANCEIRO
        titulo_resumo = QLabel("Resumo financeiro")
        titulo_resumo.setObjectName("tituloSecao")
        principal.addWidget(titulo_resumo)

        grade_resumo = QGridLayout()
        grade_resumo.setSpacing(12)

        self.resumos = {}

        cartoes_resumo = [
            ("Frete bruto", "frete", "cartaoFrete", "valorFrete"),
            (
                "Custo total da operação",
                "custo_total",
                "cartaoCusto",
                "valorCusto",
            ),
            (
                "Lucro estimado da empresa",
                "lucro",
                "cartaoLucro",
                "valorLucro",
            ),
            (
                "Margem de lucro",
                "margem",
                "cartaoResumo",
                "valorResumo",
            ),
        ]

        for i, (nome, chave, estilo_cartao, estilo_valor) in enumerate(cartoes_resumo):
            cartao = QFrame()
            cartao.setObjectName(estilo_cartao)
            cartao.setMinimumHeight(112)

            layout_cartao = QVBoxLayout(cartao)
            layout_cartao.setContentsMargins(16, 15, 16, 15)
            layout_cartao.setSpacing(12)

            rotulo = QLabel(nome)
            rotulo.setObjectName("rotuloResumoDestaque")
            rotulo.setWordWrap(True)
            rotulo.setWordWrap(True)

            valor = QLabel("—")
            valor.setObjectName(estilo_valor)
            valor.setWordWrap(True)

            layout_cartao.addWidget(rotulo)
            layout_cartao.addWidget(valor)
            layout_cartao.addStretch()

            self.resumos[chave] = valor
            grade_resumo.addWidget(cartao, 0, i)

            if chave == "lucro":
                self.cartao_lucro = cartao

        for coluna in range(4):
            grade_resumo.setColumnStretch(coluna, 1)

        principal.addLayout(grade_resumo)

        # DETALHAMENTO DOS CUSTOS
        titulo_detalhes = QLabel("Detalhamento da operação")
        titulo_detalhes.setObjectName("tituloSecao")
        principal.addWidget(titulo_detalhes)

        grupo_detalhes = QGroupBox("Composição dos gastos")
        layout_detalhes = QVBoxLayout(grupo_detalhes)
        layout_detalhes.setContentsMargins(14, 22, 14, 16)
        layout_detalhes.setSpacing(10)

        self.resultados = {}

        def adicionar_grupo_detalhes(titulo, itens):
            titulo_grupo = QLabel(titulo)
            titulo_grupo.setStyleSheet("""
                color: #1d4ed8;
                font-size: 14px;
                font-weight: 800;
                background-color: transparent;
                border-bottom: 2px solid #bfdbfe;
                padding: 8px 2px 7px 2px;
            """)
            layout_detalhes.addWidget(titulo_grupo)

            grade = QGridLayout()
            grade.setHorizontalSpacing(12)
            grade.setVerticalSpacing(10)

            for i, (nome, chave) in enumerate(itens):
                cartao = QFrame()
                cartao.setObjectName("cartaoDetalhe")
                cartao.setMinimumHeight(76)

                layout_cartao = QVBoxLayout(cartao)
                layout_cartao.setContentsMargins(12, 10, 12, 10)
                layout_cartao.setSpacing(7)

                rotulo = QLabel(nome)
                rotulo.setObjectName("rotuloResumo")
                rotulo.setWordWrap(True)

                valor = QLabel("—")
                valor.setObjectName("valorDetalhe")
                valor.setWordWrap(True)

                layout_cartao.addWidget(rotulo)
                layout_cartao.addWidget(valor)

                self.resultados[chave] = valor
                grade.addWidget(cartao, i // 3, i % 3)

            for coluna in range(3):
                grade.setColumnStretch(coluna, 1)

            layout_detalhes.addLayout(grade)

        adicionar_grupo_detalhes(
            "1. DESLOCAMENTO VAZIO",
            [
                ("Litros consumidos vazio", "litros_vazio"),
                ("Diesel do deslocamento vazio", "diesel_vazio"),
                ("Pedágios do deslocamento vazio", "pedagio_vazio"),
                ("Custo para chegar ao embarque", "custo_chegada"),
            ],
        )

        adicionar_grupo_detalhes(
            "2. FRETE, COMISSÃO E OUTRAS DESPESAS",
            [
                ("Litros consumidos carregado", "litros_carregado"),
                ("Diesel do trecho do frete", "diesel_carregado"),
                ("Pedágios do trecho do frete", "pedagio_frete"),
                ("Comissão do motorista", "comissao_resultado"),
                ("Outras despesas", "outras_resultado"),
            ],
        )

        adicionar_grupo_detalhes(
            "3. TOTAIS DA OPERAÇÃO",
            [
                ("Gasto total com diesel", "diesel_total"),
                ("Total de pedágios", "pedagios_total"),
                ("Distância total rodada", "distancia_total"),
                ("Custo total por quilômetro", "custo_km"),
            ],
        )

        principal.addWidget(grupo_detalhes)

        self.aviso = QLabel("Informe os valores da viagem para calcular o resultado.")
        self.aviso.setObjectName("aviso")
        self.aviso.setWordWrap(True)
        principal.addWidget(self.aviso)

        # AÇÕES
        botoes = QHBoxLayout()
        botoes.addStretch()

        botao_limpar = QPushButton("Limpar valores")
        botao_limpar.setObjectName("limpar")

        self.botao_compartilhar = QPushButton("Copiar resultado")
        botao_pdf = QPushButton("Baixar PDF")
        botao_pdf.setObjectName("calcular")
        self.botao_compartilhar.setObjectName("calcular")

        botao_pdf = QPushButton("Baixar PDF")
        botao_pdf.setObjectName("calcular")

        botoes.addWidget(botao_limpar)
        botoes.addWidget(self.botao_compartilhar)
        botoes.addWidget(botao_pdf)
        principal.addLayout(botoes)

        self.campos_entrada = [
            self.km_vazio,
            self.consumo_vazio,
            self.preco_diesel,
            self.pedagios_vazio,
            self.frete,
            self.km_carregado,
            self.consumo_carregado,
            self.pedagios_frete,
            self.outras_despesas,
            self.comissao,
        ]

        for campo in self.campos_entrada:
            campo.valueChanged.connect(self.calcular)

        botao_limpar.clicked.connect(self.limpar)
        self.botao_compartilhar.clicked.connect(self.compartilhar_resultado)
        botao_pdf.clicked.connect(self.exportar_pdf)

        scroll.setWidget(conteudo)
        layout_externo.addWidget(scroll)

        self.calcular()

    def criar_campo(self, casas=2, passo=1, prefixo="", sufixo=""):
        campo = CampoNumerico()
        campo.setLocale(QLocale("pt_BR"))
        campo.setRange(0, 999999999)
        campo.setDecimals(casas)
        campo.setSingleStep(passo)
        campo.setMinimumHeight(40)

        if prefixo:
            campo.setPrefix(prefixo)

        if sufixo:
            campo.setSuffix(sufixo)

        return campo

    def adicionar_campo(self, grade, linha, coluna, nome, campo):
        rotulo = QLabel(nome)
        rotulo.setObjectName("rotuloCampo")
        rotulo.setWordWrap(True)

        grade.addWidget(rotulo, linha * 2, coluna)
        grade.addWidget(campo, linha * 2 + 1, coluna)

    @staticmethod
    def dinheiro(valor):
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    @staticmethod
    def numero(valor, casas=2):
        return f"{valor:.{casas}f}".replace(".", ",")

    def mostrar_indisponivel(self):
        for campo in self.resultados.values():
            campo.setText("—")

        for campo in self.resumos.values():
            campo.setText("—")

    def calcular(self, *_):
        km_vazio = self.km_vazio.value()
        consumo_vazio = self.consumo_vazio.value()
        preco_diesel = self.preco_diesel.value()
        pedagio_vazio = self.pedagios_vazio.value()

        frete = self.frete.value()
        km_carregado = self.km_carregado.value()
        consumo_carregado = self.consumo_carregado.value()
        pedagio_frete = self.pedagios_frete.value()
        outras = self.outras_despesas.value()
        percentual = self.comissao.value()

        if km_vazio > 0 and consumo_vazio <= 0:
            self.mostrar_indisponivel()
            self.aviso.setText("Informe o consumo médio do caminhão vazio.")
            return

        if km_carregado > 0 and consumo_carregado <= 0:
            self.mostrar_indisponivel()
            self.aviso.setText("Informe o consumo médio do caminhão carregado.")
            return

        distancia_total = km_vazio + km_carregado

        if distancia_total > 0 and preco_diesel <= 0:
            self.mostrar_indisponivel()
            self.aviso.setText("Informe o preço do diesel por litro.")
            return

        litros_vazio = km_vazio / consumo_vazio if consumo_vazio > 0 else 0
        litros_carregado = (
            km_carregado / consumo_carregado if consumo_carregado > 0 else 0
        )

        diesel_vazio = litros_vazio * preco_diesel
        diesel_carregado = litros_carregado * preco_diesel
        diesel_total = diesel_vazio + diesel_carregado

        custo_chegada = diesel_vazio + pedagio_vazio
        pedagios_total = pedagio_vazio + pedagio_frete

        # A comissão é calculada sobre o frete descontados
        # os pedágios do trajeto contratado.
        base_comissao = max(frete - pedagio_frete, 0)
        comissao = base_comissao * percentual / 100

        # Os custos do deslocamento vazio são pagos pela empresa.
        custo_total = diesel_total + pedagios_total + comissao + outras

        lucro = frete - custo_total
        margem = lucro / frete * 100 if frete > 0 else None

        custo_km = custo_total / distancia_total if distancia_total > 0 else None

        self.resumos["frete"].setText(self.dinheiro(frete))
        self.resumos["custo_total"].setText(self.dinheiro(custo_total))
        self.resumos["lucro"].setText(self.dinheiro(lucro))
        self.resumos["margem"].setText(
            self.numero(margem) + "%" if margem is not None else "—"
        )

        self.resumos["lucro"].setStyleSheet(
            "color: #047857;" if lucro >= 0 else "color: #b91c1c;"
        )

        valores = {
            "diesel_vazio": self.dinheiro(diesel_vazio),
            "pedagio_vazio": self.dinheiro(pedagio_vazio),
            "custo_chegada": self.dinheiro(custo_chegada),
            "litros_vazio": self.numero(litros_vazio, 2) + " L",
            "diesel_carregado": self.dinheiro(diesel_carregado),
            "pedagio_frete": self.dinheiro(pedagio_frete),
            "litros_carregado": self.numero(litros_carregado, 2) + " L",
            "diesel_total": self.dinheiro(diesel_total),
            "pedagios_total": self.dinheiro(pedagios_total),
            "comissao_resultado": self.dinheiro(comissao),
            "outras_resultado": self.dinheiro(outras),
            "distancia_total": self.numero(distancia_total, 1) + " km",
            "custo_km": (self.dinheiro(custo_km) if custo_km is not None else "—"),
        }

        for chave, valor in valores.items():
            self.resultados[chave].setText(valor)

        if frete <= 0:
            self.aviso.setText("Informe o valor bruto do frete para avaliar o lucro.")
        elif lucro < 0:
            self.aviso.setText("Atenção: os custos estimados superam o valor do frete.")
        else:
            self.aviso.setText(
                "O lucro considera o diesel e os pedágios dos dois "
                "trechos, a comissão e as outras despesas informadas. "
                "Inclua manutenção, pneus, impostos e demais gastos "
                "em Outras despesas, quando aplicável."
            )

    def exportar_pdf(self):
        self.calcular()

        if self.frete.value() <= 0:
            self.aviso.setText("Informe o valor bruto do frete antes de gerar o PDF.")
            return

        caminho, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar relatório do frete",
            "relatorio_frete.pdf",
            "Arquivo PDF (*.pdf)",
        )

        if not caminho:
            return

        if not caminho.lower().endswith(".pdf"):
            caminho += ".pdf"

        try:
            pdf = QPdfWriter(caminho)
            pdf.setResolution(96)
            pdf.setPageSize(QPageSize(QPageSize.PageSizeId.A4))

            painter = QPainter()

            if not painter.begin(pdf):
                QMessageBox.critical(
                    self,
                    "Erro",
                    "Não foi possível gerar o PDF.",
                )
                return

            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            largura = pdf.width()
            margem = 48
            largura_util = largura - 2 * margem

            # CABEÇALHO
            painter.fillRect(0, 0, largura, 125, QColor("#172554"))

            painter.setPen(QColor("#ffffff"))
            painter.setFont(QFont("Arial", 20, QFont.Weight.Bold))
            painter.drawText(margem, 53, "FROTA GESTÃO")

            painter.setFont(QFont("Arial", 11))
            painter.drawText(margem, 82, "Relatório de frete e custos")

            painter.setFont(QFont("Arial", 9))
            painter.drawText(
                margem,
                105,
                "Gerado em " + datetime.now().strftime("%d/%m/%Y às %H:%M"),
            )

            # CARTÕES FINANCEIROS
            y_cartoes = 150
            espacamento = 12
            largura_cartao = (largura_util - 2 * espacamento) // 3

            cartoes = [
                (
                    "FRETE BRUTO",
                    self.resumos["frete"].text(),
                    "#eff6ff",
                    "#1d4ed8",
                ),
                (
                    "CUSTO TOTAL",
                    self.resumos["custo_total"].text(),
                    "#fff7ed",
                    "#c2410c",
                ),
                (
                    "LUCRO ESTIMADO",
                    self.resumos["lucro"].text(),
                    "#ecfdf5",
                    "#047857",
                ),
            ]

            for i, (titulo, valor, fundo, texto_cor) in enumerate(cartoes):
                x = margem + i * (largura_cartao + espacamento)

                painter.setPen(QColor("#dbe2ea"))
                painter.setBrush(QColor(fundo))
                painter.drawRoundedRect(
                    x,
                    y_cartoes,
                    largura_cartao,
                    82,
                    8,
                    8,
                )

                painter.setPen(QColor("#475569"))
                painter.setFont(QFont("Arial", 8, QFont.Weight.Bold))
                painter.drawText(x + 10, y_cartoes + 25, titulo)

                painter.setPen(QColor(texto_cor))
                painter.setFont(QFont("Arial", 12, QFont.Weight.Bold))
                painter.drawText(x + 10, y_cartoes + 55, valor)

            y = 265

            def desenhar_secao(titulo, linhas):
                nonlocal y

                painter.setPen(QColor("#1d4ed8"))
                painter.setFont(QFont("Arial", 11, QFont.Weight.Bold))
                painter.drawText(margem, y, titulo)

                y += 9

                painter.setPen(QColor("#bfdbfe"))
                painter.drawLine(margem, y, largura - margem, y)

                y += 21

                for rotulo, valor in linhas:
                    painter.setPen(QColor("#334155"))
                    painter.setFont(QFont("Arial", 9))
                    painter.drawText(margem, y, rotulo)

                    painter.setPen(QColor("#0f172a"))
                    painter.setFont(QFont("Arial", 9, QFont.Weight.Bold))
                    painter.drawText(
                        margem,
                        y - 12,
                        largura_util,
                        20,
                        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                        valor,
                    )

                    y += 20

                y += 13

            # DESLOCAMENTO VAZIO
            desenhar_secao(
                "1. DESLOCAMENTO VAZIO",
                [
                    (
                        "Distância até o embarque",
                        self.numero(self.km_vazio.value(), 1) + " km",
                    ),
                    (
                        "Consumo médio vazio",
                        self.numero(self.consumo_vazio.value()) + " km/L",
                    ),
                    (
                        "Litros consumidos",
                        self.resultados["litros_vazio"].text(),
                    ),
                    (
                        "Custo do diesel",
                        self.resultados["diesel_vazio"].text(),
                    ),
                    (
                        "Pedágios",
                        self.resultados["pedagio_vazio"].text(),
                    ),
                    (
                        "Custo para chegar ao embarque",
                        self.resultados["custo_chegada"].text(),
                    ),
                ],
            )

            # FRETE CONTRATADO
            desenhar_secao(
                "2. FRETE CONTRATADO",
                [
                    (
                        "Distância do trajeto contratado",
                        self.numero(self.km_carregado.value(), 1) + " km",
                    ),
                    (
                        "Consumo médio carregado",
                        self.numero(self.consumo_carregado.value()) + " km/L",
                    ),
                    (
                        "Litros consumidos",
                        self.resultados["litros_carregado"].text(),
                    ),
                    (
                        "Custo do diesel",
                        self.resultados["diesel_carregado"].text(),
                    ),
                    (
                        "Pedágios",
                        self.resultados["pedagio_frete"].text(),
                    ),
                ],
            )

            # DEMAIS DESPESAS E TOTAIS
            desenhar_secao(
                "3. DEMAIS DESPESAS E TOTAIS",
                [
                    (
                        "Comissão do motorista",
                        self.resultados["comissao_resultado"].text(),
                    ),
                    (
                        "Outras despesas",
                        self.resultados["outras_resultado"].text(),
                    ),
                    (
                        "Gasto total com diesel",
                        self.resultados["diesel_total"].text(),
                    ),
                    (
                        "Total de pedágios",
                        self.resultados["pedagios_total"].text(),
                    ),
                    (
                        "Distância total rodada",
                        self.resultados["distancia_total"].text(),
                    ),
                    (
                        "Custo total por quilômetro",
                        self.resultados["custo_km"].text(),
                    ),
                    (
                        "Margem de lucro",
                        self.resumos["margem"].text(),
                    ),
                ],
            )

            # RODAPÉ
            painter.setPen(QColor("#64748b"))
            painter.setFont(QFont("Arial", 8))
            painter.drawText(
                margem,
                min(y + 5, pdf.height() - 25),
                "Estimativa baseada nos valores informados no simulador.",
            )

            painter.end()

            QMessageBox.information(
                self,
                "PDF gerado",
                "Relatório salvo com sucesso em:\n" + caminho,
            )

        except Exception as erro:
            QMessageBox.critical(
                self,
                "Erro ao gerar PDF",
                f"Não foi possível gerar o relatório:\n{erro}",
            )

    def exportar_pdf(self):
        self.calcular()

        if self.frete.value() <= 0:
            QMessageBox.warning(
                self,
                "Dados incompletos",
                "Informe o valor bruto do frete antes de gerar o PDF.",
            )
            return

        caminho, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar relatório do frete",
            "relatorio_frete.pdf",
            "Arquivo PDF (*.pdf)",
        )

        if not caminho:
            return

        if not caminho.lower().endswith(".pdf"):
            caminho += ".pdf"

        painter = QPainter()

        try:
            pdf = QPdfWriter(caminho)
            pdf.setResolution(96)
            pdf.setPageSize(QPageSize(QPageSize.PageSizeId.A4))

            if not painter.begin(pdf):
                QMessageBox.critical(self, "Erro", "Não foi possível criar o PDF.")
                return

            largura = pdf.width()
            altura = pdf.height()
            margem = 48
            largura_util = largura - 2 * margem
            y = 0

            # Cabeçalho
            painter.fillRect(0, 0, largura, 125, QColor("#172554"))
            painter.setPen(QColor("#ffffff"))
            painter.setFont(QFont("Arial", 20, QFont.Weight.Bold))
            painter.drawText(margem, 52, "FROTA GESTÃO")

            painter.setFont(QFont("Arial", 11))
            painter.drawText(margem, 80, "Relatório de frete e custos")

            painter.setFont(QFont("Arial", 9))
            painter.drawText(
                margem,
                105,
                "Gerado em " + datetime.now().strftime("%d/%m/%Y às %H:%M"),
            )

            y = 155

            # Resumo financeiro
            cartoes = [
                ("FRETE BRUTO", self.resumos["frete"].text()),
                (
                    "CUSTO TOTAL",
                    self.resumos["custo_total"].text(),
                ),
                ("LUCRO ESTIMADO", self.resumos["lucro"].text()),
                ("MARGEM", self.resumos["margem"].text()),
            ]

            espacamento = 10
            largura_cartao = (largura_util - 3 * espacamento) // 4

            for i, (titulo, valor) in enumerate(cartoes):
                x = margem + i * (largura_cartao + espacamento)

                painter.setPen(QColor("#dbe2ea"))
                painter.setBrush(QColor("#f8fafc"))
                painter.drawRoundedRect(x, y, largura_cartao, 75, 7, 7)

                painter.setPen(QColor("#334155"))
                painter.setFont(QFont("Arial", 8, QFont.Weight.Bold))
                painter.drawText(x + 8, y + 22, titulo)

                painter.setPen(QColor("#1d4ed8"))
                painter.setFont(QFont("Arial", 11, QFont.Weight.Bold))
                painter.drawText(x + 8, y + 49, valor)

            y += 105

            def desenhar_secao(titulo, linhas):
                nonlocal y

                # Cria outra página caso o conteúdo não caiba.
                if y + 100 > altura - margem:
                    pdf.newPage()
                    y = margem

                painter.setPen(QColor("#1d4ed8"))
                painter.setFont(QFont("Arial", 11, QFont.Weight.Bold))
                painter.drawText(margem, y, titulo)
                y += 10

                painter.setPen(QColor("#bfdbfe"))
                painter.drawLine(margem, y, largura - margem, y)
                y += 22

                for rotulo, valor in linhas:
                    if y + 25 > altura - margem:
                        pdf.newPage()
                        y = margem

                    painter.setPen(QColor("#334155"))
                    painter.setFont(QFont("Arial", 9))
                    painter.drawText(margem, y, rotulo)

                    painter.setPen(QColor("#0f172a"))
                    painter.setFont(QFont("Arial", 9, QFont.Weight.Bold))
                    painter.drawText(
                        margem,
                        y - 12,
                        largura_util,
                        20,
                        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                        valor,
                    )
                    y += 21

                y += 18

            # 1. Deslocamento vazio
            desenhar_secao(
                "1. DESLOCAMENTO VAZIO",
                [
                    (
                        "Distância até o embarque",
                        self.numero(self.km_vazio.value(), 1) + " km",
                    ),
                    (
                        "Consumo médio vazio",
                        self.numero(self.consumo_vazio.value()) + " km/L",
                    ),
                    ("Litros consumidos", self.resultados["litros_vazio"].text()),
                    ("Diesel", self.resultados["diesel_vazio"].text()),
                    ("Pedágios", self.resultados["pedagio_vazio"].text()),
                    (
                        "Custo para chegar ao embarque",
                        self.resultados["custo_chegada"].text(),
                    ),
                ],
            )

            # 2. Frete contratado
            desenhar_secao(
                "2. FRETE CONTRATADO",
                [
                    (
                        "Valor bruto do frete",
                        self.resumos["frete"].text(),
                    ),
                    (
                        "Distância contratada",
                        self.numero(self.km_carregado.value(), 1) + " km",
                    ),
                    (
                        "Consumo médio carregado",
                        self.numero(self.consumo_carregado.value()) + " km/L",
                    ),
                    (
                        "Litros consumidos",
                        self.resultados["litros_carregado"].text(),
                    ),
                    (
                        "Diesel do trecho",
                        self.resultados["diesel_carregado"].text(),
                    ),
                    (
                        "Pedágios do trecho",
                        self.resultados["pedagio_frete"].text(),
                    ),
                ],
            )

            # 3. Demais despesas e totais
            desenhar_secao(
                "3. DEMAIS DESPESAS E TOTAIS",
                [
                    (
                        "Comissão do motorista",
                        self.resultados["comissao_resultado"].text(),
                    ),
                    (
                        "Outras despesas",
                        self.resultados["outras_resultado"].text(),
                    ),
                    (
                        "Gasto total com diesel",
                        self.resultados["diesel_total"].text(),
                    ),
                    (
                        "Total de pedágios",
                        self.resultados["pedagios_total"].text(),
                    ),
                    (
                        "Distância total rodada",
                        self.resultados["distancia_total"].text(),
                    ),
                    (
                        "Custo por quilômetro",
                        self.resultados["custo_km"].text(),
                    ),
                    (
                        "Custo total da operação",
                        self.resumos["custo_total"].text(),
                    ),
                    (
                        "Lucro estimado da empresa",
                        self.resumos["lucro"].text(),
                    ),
                    (
                        "Margem de lucro",
                        self.resumos["margem"].text(),
                    ),
                ],
            )

            painter.end()

            QMessageBox.information(
                self,
                "PDF criado",
                "Relatório salvo em:\n" + caminho,
            )

        except Exception as erro:
            if painter.isActive():
                painter.end()

            QMessageBox.critical(
                self,
                "Erro ao gerar PDF",
                f"Não foi possível gerar o relatório:\n{erro}",
            )

    def limpar(self):
        for campo in self.campos_entrada:
            campo.setValue(0)
            campo.resetar_edicao()

    def compartilhar_resultado(self):
        self.calcular()

        if self.frete.value() <= 0:
            self.aviso.setText("Informe o valor bruto do frete antes de compartilhar.")
            return

        texto = "\n".join(
            [
                "RESUMO DO FRETE - FROTA GESTÃO",
                "",
                f"Frete bruto: {self.resumos['frete'].text()}",
                f"Custo total: {self.resumos['custo_total'].text()}",
                f"Lucro estimado: {self.resumos['lucro'].text()}",
                f"Margem de lucro: {self.resumos['margem'].text()}",
                "",
                "DESLOCAMENTO VAZIO",
                f"Distância: {self.numero(self.km_vazio.value(), 1)} km",
                f"Diesel: {self.resultados['diesel_vazio'].text()}",
                f"Pedágios: {self.resultados['pedagio_vazio'].text()}",
                f"Custo para chegar ao embarque: "
                f"{self.resultados['custo_chegada'].text()}",
                "",
                "FRETE CONTRATADO",
                f"Distância: {self.numero(self.km_carregado.value(), 1)} km",
                f"Diesel: {self.resultados['diesel_carregado'].text()}",
                f"Pedágios: {self.resultados['pedagio_frete'].text()}",
                f"Comissão: {self.resultados['comissao_resultado'].text()}",
                f"Outras despesas: {self.resultados['outras_resultado'].text()}",
                "",
                "TOTAIS",
                f"Diesel: {self.resultados['diesel_total'].text()}",
                f"Pedágios: {self.resultados['pedagios_total'].text()}",
                f"Distância total: {self.resultados['distancia_total'].text()}",
                f"Custo por km: {self.resultados['custo_km'].text()}",
            ]
        )

        QApplication.clipboard().setText(texto)
        self.botao_compartilhar.setText("Copiado!")

        QTimer.singleShot(
            1500, lambda: self.botao_compartilhar.setText("Copiar resultado")
        )

        self.aviso.setText(
            "Resumo copiado! Cole no WhatsApp ou em outra mensagem "
            "para compartilhar."
        )

        self.comissao.setValue(11)
        self.calcular()
