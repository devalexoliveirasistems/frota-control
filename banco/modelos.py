from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Veiculo(Base):
    __tablename__ = "veiculos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    codigo_frota: Mapped[int] = mapped_column(Integer, nullable=False)

    placa: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)

    marca: Mapped[str] = mapped_column(String(50), nullable=False)

    modelo: Mapped[str] = mapped_column(String(100), nullable=False)

    ano: Mapped[int] = mapped_column(Integer, nullable=False)

    tipo: Mapped[str] = mapped_column(String(50), nullable=False)

    status: Mapped[str] = mapped_column(String(20), nullable=False, default="Ativo")
