from sqlalchemy import create_engine


DATABASE_URL = (
    "postgresql+psycopg://postgres:415263@localhost:5432/frota_gestao"
)


engine = create_engine(DATABASE_URL)
