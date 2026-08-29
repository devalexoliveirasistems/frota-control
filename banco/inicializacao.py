from banco.conexao import engine
from banco.modelos import Base


def inicializar_banco():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    inicializar_banco()
    print("Banco de dados inicializado com sucesso!")
