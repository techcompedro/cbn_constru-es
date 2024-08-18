from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker  

engine = create_engine('sqlite:///loja.db', echo=True)

Base = declarative_base()
class Produtos(Base):
    __tablename__ = 'produtos'
    id = Column(Integer, primary_key=True)
    nome = Column(String(150))
    img = Column(String(500))
    venda_valor = Column(Float)
    custo_valor = Column(Float)
    lucro = Column(Float)
    qtn = Column(Integer)
    categoria = Column(String(100))


Session = sessionmaker(bind=engine)
session = Session()
