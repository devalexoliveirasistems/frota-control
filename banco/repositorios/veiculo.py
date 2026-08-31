from sqlalchemy.orm import Session

from banco.modelos import Veiculo

from sqlalchemy import text


def cadastrar_veiculo(
    sessao: Session,
    placa: str,
    marca: str,
    modelo: str,
    ano: int,
    tipo: str,
    status: str,
):
    resultado = sessao.execute(text("""
            UPDATE controle_frota
            SET proximo_numero = proximo_numero + 1
            WHERE id = 1
            RETURNING proximo_numero - 1
            """))

    numero = resultado.scalar_one()
    codigo_frota = f"AAA-{numero:03d}"

    veiculo = Veiculo(
        codigo_frota=codigo_frota,
        placa=placa,
        marca=marca,
        modelo=modelo,
        ano=ano,
        tipo=tipo,
        status=status,
    )

    sessao.add(veiculo)
    sessao.commit()
    sessao.refresh(veiculo)

    return veiculo


def atualizar_veiculo(
    sessao: Session,
    veiculo: Veiculo,
    placa: str,
    marca: str,
    modelo: str,
    ano: int,
    tipo: str,
    status: str,
):
    veiculo.placa = placa
    veiculo.marca = marca
    veiculo.modelo = modelo
    veiculo.ano = ano
    veiculo.tipo = tipo
    veiculo.status = status

    sessao.commit()
    sessao.refresh(veiculo)

    return veiculo
