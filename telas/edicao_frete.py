from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QDateEdit,
    QMessageBox,
)
from PySide6.QtCore import QDate

from banco.sessao import SessionLocal
from banco.modelos import Veiculo


class EdicaoFrete(QDialog):
    def __init__(self, frete, parent=None):
        super().__init__(parent)

        self.frete = frete

        self.setWindowTitle("Editar Frete")
        self.resize(800, 500)

        layout_principal = QVBoxLayout()

        titulo = QLabel("Editar Frete")
        titulo.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            """)
        layout_principal.addWidget(titulo)

        # ==================================
        # CONTRATO / DATA
        # ==================================

        linha_1 = QHBoxLayout()

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

        linha_1.addWidget(QLabel("N° Contrato"))
        linha_1.addWidget(self.campo_contrato)

        linha_1.addWidget(QLabel("Dia"))
        linha_1.addWidget(self.campo_dia)

        layout_principal.addLayout(linha_1)

        # ==================================
        # TRANSPORTADORA
        # ==================================

        linha_2 = QHBoxLayout()

        self.campo_transportadora = QLineEdit(frete.transportadora)

        linha_2.addWidget(QLabel("Transportadora"))
        linha_2.addWidget(self.campo_transportadora)

        layout_principal.addLayout(linha_2)

        # ==================================
        # EMBARQUE / DESTINO
        # ==================================

        linha_3 = QHBoxLayout()

        self.campo_embarque = QLineEdit(frete.embarque)

        self.campo_destino = QLineEdit(frete.destino)

        linha_3.addWidget(QLabel("Embarque"))
        linha_3.addWidget(self.campo_embarque)

        linha_3.addWidget(QLabel("Destino"))
        linha_3.addWidget(self.campo_destino)

        layout_principal.addLayout(linha_3)

        # ==================================
        # PLACA
        # ==================================

        linha_4 = QHBoxLayout()

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

        linha_4.addWidget(QLabel("Placa"))
        linha_4.addWidget(self.campo_placa)

        layout_principal.addLayout(linha_4)

        # ==================================
        # VALORES
        # ==================================

        linha_5 = QHBoxLayout()

        self.campo_frete = QLineEdit(self.formatar_moeda(frete.valor_frete))

        self.campo_pedagio = QLineEdit(self.formatar_moeda(frete.pedagio))

        self.campo_adiantamento = QLineEdit(self.formatar_moeda(frete.adiantamento))

        self.campo_saldo = QLineEdit(
            "" if frete.saldo is None else self.formatar_moeda(frete.saldo)
        )

        linha_5.addWidget(QLabel("Frete"))
        linha_5.addWidget(self.campo_frete)

        linha_5.addWidget(QLabel("Pedágio"))
        linha_5.addWidget(self.campo_pedagio)

        layout_principal.addLayout(linha_5)

        linha_6 = QHBoxLayout()

        linha_6.addWidget(QLabel("Adiantamento"))
        linha_6.addWidget(self.campo_adiantamento)

        linha_6.addWidget(QLabel("Saldo recebido"))
        linha_6.addWidget(self.campo_saldo)

        layout_principal.addLayout(linha_6)

        # ==================================
        # OBSERVAÇÃO
        # ==================================
        linha_observacao = QHBoxLayout()

        self.campo_observacao = QLineEdit(
            "" if frete.observacao is None else frete.observacao
        )

        linha_observacao.addWidget(QLabel("Observação"))
        linha_observacao.addWidget(self.campo_observacao)

        layout_principal.addLayout(linha_observacao)

        # ==================================
        # STATUS
        # ==================================

        linha_7 = QHBoxLayout()

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

        linha_7.addWidget(QLabel("Status"))
        linha_7.addWidget(self.campo_status)

        layout_principal.addLayout(linha_7)

        # ==================================
        # BOTÕES
        # ==================================

        linha_botoes = QHBoxLayout()

        linha_botoes.addStretch()

        botao_cancelar = QPushButton("Cancelar")

        botao_salvar = QPushButton("Salvar alterações")

        botao_salvar.setMinimumWidth(160)

        linha_botoes.addWidget(botao_cancelar)
        linha_botoes.addWidget(botao_salvar)

        layout_principal.addLayout(linha_botoes)

        botao_cancelar.clicked.connect(self.reject)

        botao_salvar.clicked.connect(self.salvar_alteracoes)

        self.setLayout(layout_principal)

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

    def salvar_alteracoes(self):
        try:
            veiculo_id = self.campo_placa.currentData()

            if veiculo_id is None:
                QMessageBox.warning(
                    self,
                    "Placa obrigatória",
                    "Selecione a placa do caminhão.",
                )
                return

            valor_frete = self.converter_valor(self.campo_frete.text())

            pedagio = self.converter_valor(self.campo_pedagio.text())

            adiantamento = self.converter_valor(self.campo_adiantamento.text())

            saldo_texto = self.campo_saldo.text().strip()

            saldo = None if not saldo_texto else self.converter_valor(saldo_texto)

            sessao = SessionLocal()

            try:
                self.frete.dia = self.campo_dia.date().toPython()

                self.frete.ordem_servico = self.campo_contrato.text().strip()

                self.frete.transportadora = self.campo_transportadora.text().strip()

                self.frete.embarque = self.campo_embarque.text().strip()

                self.frete.destino = self.campo_destino.text().strip()

                self.frete.veiculo_id = veiculo_id

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
