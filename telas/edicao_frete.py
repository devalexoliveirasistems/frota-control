from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QDateEdit,
    QMessageBox,
)
from PySide6.QtCore import QDate

from banco.sessao import SessionLocal
from banco.modelos import Veiculo, Motorista


class EdicaoFrete(QDialog):
    def __init__(self, frete, parent=None):
        super().__init__(parent)

        self.frete = frete

        self.setWindowTitle("Editar Frete")
        self.resize(900, 650)
        self.setMinimumSize(850, 600)

        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(25, 20, 25, 20)
        layout_principal.setSpacing(15)

        titulo = QLabel("Editar Frete")
        titulo.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            """)
        layout_principal.addWidget(titulo)

        # ==================================
        # CONTRATO / DATA
        # ==================================

        self.campo_contrato = QLineEdit(str(frete.ordem_servico))

        self.campo_dia = QDateEdit()
        self.campo_dia.setCalendarPopup(True)
        self.campo_dia.setDate(
            QDate(
                frete.dia.year,
                frete.dia.month,
                frete.dia.day,
            )
        )

        grid_contrato = QGridLayout()
        grid_contrato.setHorizontalSpacing(15)
        grid_contrato.setVerticalSpacing(6)

        grid_contrato.addWidget(QLabel("N° Contrato"), 0, 0)
        grid_contrato.addWidget(QLabel("Data"), 0, 1)

        grid_contrato.addWidget(self.campo_contrato, 1, 0)
        grid_contrato.addWidget(self.campo_dia, 1, 1)

        grid_contrato.setColumnStretch(0, 1)
        grid_contrato.setColumnStretch(1, 1)

        layout_principal.addLayout(grid_contrato)

        # ==================================
        # TRANSPORTADORA / PESO
        # ==================================

        self.campo_transportadora = QLineEdit(frete.transportadora)

        self.campo_peso = QLineEdit("" if frete.peso is None else str(frete.peso))
        self.campo_peso.setPlaceholderText("Peso da carga (kg)")

        grid_transportadora = QGridLayout()
        grid_transportadora.setHorizontalSpacing(15)
        grid_transportadora.setVerticalSpacing(6)

        grid_transportadora.addWidget(QLabel("Transportadora"), 0, 0)
        grid_transportadora.addWidget(QLabel("Peso (kg)"), 0, 1)

        grid_transportadora.addWidget(self.campo_transportadora, 1, 0)
        grid_transportadora.addWidget(self.campo_peso, 1, 1)

        grid_transportadora.setColumnStretch(0, 1)
        grid_transportadora.setColumnStretch(1, 1)

        layout_principal.addLayout(grid_transportadora)

        # ==================================
        # EMBARQUE / DESTINO
        # ==================================

        self.campo_embarque = QLineEdit(frete.embarque)

        self.campo_destino = QLineEdit(frete.destino)

        grid_origem_destino = QGridLayout()
        grid_origem_destino.setHorizontalSpacing(15)
        grid_origem_destino.setVerticalSpacing(6)

        grid_origem_destino.addWidget(QLabel("Embarque"), 0, 0)
        grid_origem_destino.addWidget(QLabel("Destino"), 0, 1)

        grid_origem_destino.addWidget(self.campo_embarque, 1, 0)
        grid_origem_destino.addWidget(self.campo_destino, 1, 1)

        grid_origem_destino.setColumnStretch(0, 1)
        grid_origem_destino.setColumnStretch(1, 1)

        layout_principal.addLayout(grid_origem_destino)

        # ==================================
        # PLACA / MOTORISTA
        # ==================================

        self.campo_placa = QComboBox()
        self.campo_placa.addItem(
            "Selecione a placa",
            None,
        )

        sessao = SessionLocal()

        try:
            veiculos = (
                sessao.query(Veiculo)
                .filter(Veiculo.status == "Ativo")
                .order_by(Veiculo.placa.asc())
                .all()
            )

            for veiculo in veiculos:
                self.campo_placa.addItem(
                    veiculo.placa,
                    veiculo.id,
                )

        finally:
            sessao.close()

        indice = self.campo_placa.findData(frete.veiculo_id)

        if indice >= 0:
            self.campo_placa.setCurrentIndex(indice)

        self.campo_motorista = QComboBox()
        self.campo_motorista.addItem(
            "Selecione o motorista",
            None,
        )

        sessao = SessionLocal()

        try:
            motoristas = (
                sessao.query(Motorista)
                .filter(Motorista.status == "Ativo")
                .order_by(Motorista.nome.asc())
                .all()
            )

            for motorista in motoristas:
                self.campo_motorista.addItem(
                    motorista.nome,
                    motorista.id,
                )
        finally:
            sessao.close()

        indice_motorista = self.campo_motorista.findData(frete.motorista_id)

        if indice_motorista >= 0:
            self.campo_motorista.setCurrentIndex(indice_motorista)

        grid_veiculo = QGridLayout()
        grid_veiculo.setHorizontalSpacing(15)
        grid_veiculo.setVerticalSpacing(6)

        grid_veiculo.addWidget(QLabel("Placa"), 0, 0)
        grid_veiculo.addWidget(QLabel("Motorista"), 0, 1)

        grid_veiculo.addWidget(self.campo_placa, 1, 0)
        grid_veiculo.addWidget(self.campo_motorista, 1, 1)

        grid_veiculo.setColumnStretch(0, 1)
        grid_veiculo.setColumnStretch(1, 1)

        layout_principal.addLayout(grid_veiculo)

        # ==================================
        # MOTORISTA
        # ==================================

        linha_motorista = QHBoxLayout()

        self.campo_motorista = QComboBox()
        self.campo_motorista.addItem(
            "Selecione o motorista",
            None,
        )

        sessao = SessionLocal()

        try:
            motoristas = (
                sessao.query(Motorista)
                .filter(Motorista.status == "Ativo")
                .order_by(Motorista.nome.asc())
                .all()
            )

            for motorista in motoristas:
                self.campo_motorista.addItem(
                    motorista.nome,
                    motorista.id,
                )
        finally:
            sessao.close()

        linha_motorista.addWidget(QLabel("Motorista"))
        linha_motorista.addWidget(self.campo_motorista)

        layout_principal.addLayout(linha_motorista)

        # ==================================
        # VALORES
        # ==================================

        self.campo_frete = QLineEdit(self.formatar_moeda(frete.valor_frete))

        self.campo_pedagio = QLineEdit(self.formatar_moeda(frete.pedagio))

        self.campo_adiantamento = QLineEdit(self.formatar_moeda(frete.adiantamento))

        self.campo_frete.editingFinished.connect(self.calcular_saldo)
        self.campo_adiantamento.editingFinished.connect(self.calcular_saldo)

        self.campo_saldo = QLineEdit(
            "" if frete.saldo is None else self.formatar_moeda(frete.saldo)
        )
        self.campo_saldo.setReadOnly(True)

        self.calcular_saldo()

        grid_valores = QGridLayout()
        grid_valores.setHorizontalSpacing(15)
        grid_valores.setVerticalSpacing(6)

        grid_valores.addWidget(QLabel("Frete"), 0, 0)
        grid_valores.addWidget(QLabel("Pedágio"), 0, 1)
        grid_valores.addWidget(self.campo_frete, 1, 0)
        grid_valores.addWidget(self.campo_pedagio, 1, 1)

        grid_valores.addWidget(QLabel("Adiantamento"), 2, 0)
        grid_valores.addWidget(QLabel("Saldo recebido"), 2, 1)
        grid_valores.addWidget(self.campo_adiantamento, 3, 0)
        grid_valores.addWidget(self.campo_saldo, 3, 1)

        grid_valores.setColumnStretch(0, 1)
        grid_valores.setColumnStretch(1, 1)

        layout_principal.addLayout(grid_valores)

        # ==================================
        # OBSERVAÇÃO
        # ==================================

        self.campo_observacao = QLineEdit(
            "" if frete.observacao is None else frete.observacao
        )
        self.campo_observacao.setPlaceholderText("Observação")

        grid_observacao = QGridLayout()
        grid_observacao.setVerticalSpacing(6)

        grid_observacao.addWidget(QLabel("Observação"), 0, 0)
        grid_observacao.addWidget(self.campo_observacao, 1, 0)

        layout_principal.addLayout(grid_observacao)

        # ==================================
        # STATUS
        # ==================================

        self.campo_status = QComboBox()

        self.campo_status.addItems(
            [
                "Pendente",
                "Aguardando carregamento",
                "Carregado",
                "Em viagem",
                "Aguardando descarga",
                "Descarregado",
                "Aguardando saldo",
                "Frete quitado",
                "Cancelado",
            ]
        )

        self.campo_status.setCurrentText(frete.status)

        grid_status = QGridLayout()
        grid_status.setVerticalSpacing(6)

        grid_status.addWidget(QLabel("Status"), 0, 0)
        grid_status.addWidget(self.campo_status, 1, 0)

        layout_principal.addLayout(grid_status)

        # ==================================
        # BOTÕES
        # ==================================

        linha_botoes = QHBoxLayout()
        linha_botoes.addStretch()

        botao_cancelar = QPushButton("Cancelar")
        botao_cancelar.setMinimumWidth(120)

        botao_salvar = QPushButton("Salvar alterações")
        botao_salvar.setMinimumWidth(160)

        linha_botoes.addWidget(botao_cancelar)
        linha_botoes.addWidget(botao_salvar)

        layout_principal.addLayout(linha_botoes)

    def converter_valor(self, texto):
        texto = texto.strip()

        if not texto:
            return 0.0

        texto = texto.replace(
            "R$",
            "",
        ).strip()

        texto = texto.replace(
            ".",
            "",
        )

        texto = texto.replace(
            ",",
            ".",
        )

        return float(texto)

    def formatar_moeda(self, valor):
        return (
            f"R$ {float(valor):,.2f}".replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

    def calcular_saldo(self):
        try:
            valor_frete = self.converter_valor(self.campo_frete.text())
            adiantamento = self.converter_valor(self.campo_adiantamento.text())

            saldo = valor_frete - adiantamento

            if saldo < 0:
                saldo = 0

            self.campo_saldo.setText(self.formatar_moeda(saldo))

        except ValueError:
            self.campo_saldo.clear()

    def salvar_alteracoes(self):
        try:
            veiculo_id = self.campo_placa.currentData()

            motorista_id = self.campo_motorista.currentData()

            if not self.campo_contrato.text().strip():
                QMessageBox.warning(
                    self,
                    "Campo obrigatório",
                    "Informe o número do contrato.",
                )
                return

            if motorista_id is None:
                QMessageBox.warning(
                    self,
                    "Motorista obrigatório",
                    "Selecione o motorista.",
                )
                return

            if veiculo_id is None:
                QMessageBox.warning(
                    self,
                    "Placa obrigatória",
                    "Selecione a placa do caminhão.",
                )
                return

            if not self.campo_transportadora.text().strip():
                QMessageBox.warning(
                    self,
                    "Campo obrigatório",
                    "Informe a transportadora.",
                )
                return

            if not self.campo_embarque.text().strip():
                QMessageBox.warning(
                    self,
                    "Campo obrigatório",
                    "Informe o local de embarque.",
                )
                return

            if not self.campo_destino.text().strip():
                QMessageBox.warning(
                    self,
                    "Campo obrigatório",
                    "Informe o local de destino.",
                )
                return

            valor_frete = self.converter_valor(self.campo_frete.text())

            pedagio = self.converter_valor(self.campo_pedagio.text())

            if pedagio > valor_frete:
                QMessageBox.warning(
                    self,
                    "Valor inválido",
                    "O pedágio não pode ser maior que o valor do frete.",
                )
                return

            adiantamento = self.converter_valor(self.campo_adiantamento.text())

            if adiantamento > valor_frete:
                QMessageBox.warning(
                    self,
                    "Valor inválido",
                    "O adiantamento não pode ser maior que o valor do frete.",
                )
                return

            saldo = valor_frete - adiantamento

            if saldo < 0:
                saldo = 0

            peso = None

            texto_peso = self.campo_peso.text().strip()

            if texto_peso:
                texto_peso = texto_peso.replace(".", "").replace(",", ".")
                peso = float(texto_peso)

                if peso <= 0:
                    QMessageBox.warning(
                        self,
                        "Peso inválido",
                        "Informe um peso maior que zero.",
                    )
                    return

            sessao = SessionLocal()

            try:
                self.frete.dia = self.campo_dia.date().toPython()

                self.frete.ordem_servico = self.campo_contrato.text().strip()

                self.frete.transportadora = self.campo_transportadora.text().strip()

                self.frete.embarque = self.campo_embarque.text().strip()

                self.frete.destino = self.campo_destino.text().strip()

                self.frete.peso = peso

                self.frete.veiculo_id = veiculo_id

                self.frete.motorista_id = motorista_id

                self.frete.valor_frete = valor_frete

                self.frete.pedagio = pedagio

                self.frete.adiantamento = adiantamento

                self.frete.saldo = saldo

                self.frete.status = self.campo_status.currentText()

                self.frete.observacao = self.campo_observacao.text().strip()

                sessao.merge(self.frete)
                sessao.commit()

            except Exception:
                sessao.rollback()
                raise

            finally:
                sessao.close()

            QMessageBox.information(
                self,
                "Alteração concluída",
                "Frete atualizado com sucesso.",
            )

            self.accept()

        except ValueError:
            QMessageBox.warning(
                self,
                "Valor inválido",
                "Confira os valores financeiros.",
            )

        except Exception as erro:
            QMessageBox.critical(
                self,
                "Erro",
                f"Não foi possível atualizar o frete:\n\n{erro}",
            )
