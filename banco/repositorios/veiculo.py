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
    configuracao: str | None = None,
    commit: bool = True,
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
        configuracao=configuracao,
        status=status,
    )

    sessao.add(veiculo)

    if commit:
        sessao.commit()
    else:
        sessao.flush()

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
    configuracao: str | None = None,
    commit: bool = True,
):
    veiculo.placa = placa
    veiculo.marca = marca
    veiculo.modelo = modelo
    veiculo.ano = ano
    veiculo.tipo = tipo

    if configuracao is not None:
        veiculo.configuracao = configuracao

    veiculo.status = status

    if commit:
        sessao.commit()
    else:
        sessao.flush()

    sessao.refresh(veiculo)

    return veiculo
