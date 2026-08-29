from sqlalchemy.orm import sessionmaker

from banco.conexao import engine


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)
