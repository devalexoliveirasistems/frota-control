from sqlalchemy.orm import Session

from banco.modelos import Veiculo


def cadastrar_veiculo(
    sessao: Session,
    placa: str,
    marca: str,
    modelo: str,
    ano: int,
    tipo: str,
):
    codigos = (
        sessao.query(Veiculo.codigo_frota).order_by(Veiculo.codigo_frota.asc()).all()
    )

    proximo_codigo = 1

    for (codigo,) in codigos:
        if codigo == proximo_codigo:
            proximo_codigo += 1
        elif codigo > proximo_codigo:
            break

    veiculo = Veiculo(
        codigo_frota=proximo_codigo,
        placa=placa,
        marca=marca,
        modelo=modelo,
        ano=ano,
        tipo=tipo,
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
):
    veiculo.placa = placa
    veiculo.marca = marca
    veiculo.modelo = modelo
    veiculo.ano = ano
    veiculo.tipo = tipo

    sessao.commit()
    sessao.refresh(veiculo)

    return veiculo
