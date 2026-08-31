from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


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
