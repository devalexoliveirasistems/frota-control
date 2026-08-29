from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QLineEdit,
    QSpinBox,
    QComboBox,
    QPushButton,
    QHBoxLayout,
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

        if self.veiculo:
            self.campo_placa.setText(self.veiculo.placa)
            self.campo_marca.setText(self.veiculo.marca)
            self.campo_modelo.setText(self.veiculo.modelo)
            self.campo_ano.setValue(self.veiculo.ano)

            indice = self.campo_tipo.findText(self.veiculo.tipo)

            if indice >= 0:
                self.campo_tipo.setCurrentIndex(indice)

        layout.addRow("Placa:", self.campo_placa)
        layout.addRow("Marca:", self.campo_marca)
        layout.addRow("Modelo:", self.campo_modelo)
        layout.addRow("Ano:", self.campo_ano)
        layout.addRow("Tipo:", self.campo_tipo)

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
        placa = self.campo_placa.text().strip()
        marca = self.campo_marca.text().strip()
        modelo = self.campo_modelo.text().strip()
        ano = self.campo_ano.value()
        tipo = self.campo_tipo.currentText()

        if not placa or not marca or not modelo:
            return

        sessao = SessionLocal()

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
                )

            else:
                cadastrar_veiculo(
                    sessao=sessao,
                    placa=placa,
                    marca=marca,
                    modelo=modelo,
                    ano=ano,
                    tipo=tipo,
                )

            self.accept()

        finally:
            sessao.close()
