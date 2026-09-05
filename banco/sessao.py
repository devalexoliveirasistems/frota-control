from sqlalchemy.orm import sessionmaker

from banco.conexao import engine

from banco.modelos import Frete

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)
