from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import mysql.connector

MYSQL_USER = "root"
MYSQL_HOST = "localhost"
MYSQL_PORT = "3306" 
MYSQL_DB = "faiscabd"

conn = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER
)
cursor = conn.cursor()
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DB};")
conn.commit()
cursor.close()
conn.close()

DATABASE_URL = f"mysql+mysqlconnector://{MYSQL_USER}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

# Criando o motor do banco
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Criando a sessão do banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base para os modelos
Base = declarative_base()

# Função para obter uma sessão de banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()