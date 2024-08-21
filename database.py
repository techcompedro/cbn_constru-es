from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine('sqlite:///loja.db', echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    produtos = relationship('Produtos', back_populates='user')  # Corrigido 'con' para 'produtos'
    

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
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='produtos')  # Mantido o nome 'user'

Session = sessionmaker(bind=engine)
session = Session()
#Base.metadata.create_all(engine)

