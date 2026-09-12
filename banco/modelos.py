from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String, Integer, ForeignKey, Date, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date


class Base(DeclarativeBase):
    pass


class Veiculo(Base):
    __tablename__ = "veiculos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    codigo_frota: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True,
    )

    placa: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)

    marca: Mapped[str] = mapped_column(String(50), nullable=False)

    modelo: Mapped[str] = mapped_column(String(100), nullable=False)

    ano: Mapped[int] = mapped_column(Integer, nullable=False)

    tipo: Mapped[str] = mapped_column(String(50), nullable=False)

    status: Mapped[str] = mapped_column(String(20), nullable=False, default="Ativo")


class Motorista(Base):
    __tablename__ = "motoristas"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    nome: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    cpf: Mapped[str] = mapped_column(
        String(14),
        unique=True,
        nullable=False,
    )

    telefone: Mapped[str] = mapped_column(
        String(20),
        nullable=True,
    )

    cep: Mapped[str | None] = mapped_column(String(10), nullable=True)
    logradouro: Mapped[str | None] = mapped_column(String(150), nullable=True)
    numero: Mapped[str | None] = mapped_column(String(20), nullable=True)
    complemento: Mapped[str | None] = mapped_column(String(100), nullable=True)
    bairro: Mapped[str | None] = mapped_column(String(100), nullable=True)
    cidade: Mapped[str | None] = mapped_column(String(100), nullable=True)
    estado: Mapped[str | None] = mapped_column(String(2), nullable=True)

    categoria_cnh: Mapped[str | None] = mapped_column(
        String(5),
        nullable=True,
    )

    validade_cnh: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="Pendente",
    )

    observacao: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )


class DocumentoMotorista(Base):
    __tablename__ = "documentos_motoristas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    motorista_id: Mapped[int] = mapped_column(
        ForeignKey("motoristas.id"),
        nullable=False,
    )
    tipo_documento: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    nome_arquivo: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    caminho_arquivo: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )
    validade: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )


class Frete(Base):
    __tablename__ = "fretes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    dia: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    ordem_servico: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    transportadora: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    embarque: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    destino: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    veiculo_id: Mapped[int] = mapped_column(
        ForeignKey("veiculos.id"),
        nullable=False,
    )

    motorista_id: Mapped[int] = mapped_column(
        ForeignKey("motoristas.id"),
        nullable=False,
    )

    valor_frete: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    pedagio: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=0,
    )

    adiantamento: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=0,
    )

    saldo: Mapped[float | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="Pendente",
    )

    observacao: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )


class Empresa(Base):
    __tablename__ = "empresas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    nome: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    cnpj: Mapped[str] = mapped_column(
        String(18),
        unique=True,
        nullable=False,
    )

    ativo: Mapped[bool] = mapped_column(
        nullable=False,
        default=True,
    )


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    empresa_id: Mapped[int] = mapped_column(
        ForeignKey("empresas.id"),
        nullable=False,
    )

    nome: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
    )

    senha_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    perfil: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="Administrador",
    )

    ativo: Mapped[bool] = mapped_column(
        nullable=False,
        default=True,
    )
