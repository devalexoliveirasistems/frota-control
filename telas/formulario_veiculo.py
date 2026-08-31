from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QLineEdit,
    QSpinBox,
    QComboBox,
    QPushButton,
    QHBoxLayout,
    QMessageBox,
)

from banco.sessao import SessionLocal
from banco.modelos import Veiculo
from banco.repositorios.veiculo import cadastrar_veiculo, atualizar_veiculo


class FormularioVeiculo(QDialog):
    def __init__(self, veiculo=None, parent=None):
        super().__init__(parent)

        self.veiculo = veiculo

        if self.veiculo:
            self.setWindowTitle("Editar veículo")
        else:
            self.setWindowTitle("Novo veículo")

        self.resize(400, 300)

        layout = QFormLayout()

        self.campo_placa = QLineEdit()
        self.campo_marca = QLineEdit()
        self.campo_modelo = QLineEdit()

        self.campo_ano = QSpinBox()
        self.campo_ano.setRange(1900, 2100)
        self.campo_ano.setValue(2026)

        self.campo_tipo = QComboBox()
        self.campo_tipo.addItems(
            [
                "Caminhão",
                "Carreta",
                "Van",
                "Carro",
                "Utilitário",
                "Outro",
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

        if self.veiculo:
            self.campo_placa.setText(self.veiculo.placa)
            self.campo_marca.setText(self.veiculo.marca)
            self.campo_modelo.setText(self.veiculo.modelo)
            self.campo_ano.setValue(self.veiculo.ano)

            indice_status = self.campo_status.findText(self.veiculo.status)

            if indice_status >= 0:
                self.campo_status.setCurrentIndex(indice_status)

            indice = self.campo_tipo.findText(self.veiculo.tipo)

            if indice >= 0:
                self.campo_tipo.setCurrentIndex(indice)

        layout.addRow("Placa:", self.campo_placa)
        layout.addRow("Marca:", self.campo_marca)
        layout.addRow("Modelo:", self.campo_modelo)
        layout.addRow("Ano:", self.campo_ano)
        layout.addRow("Tipo:", self.campo_tipo)
        layout.addRow("Status:", self.campo_status)

        linha_botoes = QHBoxLayout()

        botao_cancelar = QPushButton("Cancelar")
        botao_salvar = QPushButton("Salvar")

        linha_botoes.addWidget(botao_cancelar)
        linha_botoes.addWidget(botao_salvar)

        layout.addRow(linha_botoes)

        self.setLayout(layout)

        botao_cancelar.clicked.connect(self.reject)
        botao_salvar.clicked.connect(self.salvar)

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
        tipo = self.campo_tipo.currentText()
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
                )

            else:
                cadastrar_veiculo(
                    sessao=sessao,
                    placa=placa,
                    marca=marca,
                    modelo=modelo,
                    ano=ano,
                    tipo=tipo,
                    status=status,
                )

            self.accept()

        finally:
            sessao.close()
