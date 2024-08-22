from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import  random
engine = create_engine('sqlite:///loja.db', echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    cargo = Column(String(20), nullable=False, default='cliente')
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
Base.metadata.create_all(engine)
def adicionar_produtos():
    categorias = ['Eletrônicos', 'Roupas', 'Alimentos', 'Livros', 'Brinquedos']  # Lista de categorias

    for i in range(220):
        produto = Produtos(
            nome=f'Produto {i+1}',
            img=f'url_da_imagem_{i+1}.jpg',
            venda_valor=round(random.uniform(10.0, 100.0), 2),
            custo_valor=round(random.uniform(5.0, 50.0), 2),
            lucro=round(random.uniform(5.0, 50.0), 2),
            qtn=random.randint(1, 100),
            categoria=random.choice(categorias)  # Seleciona uma categoria aleatória
        )
        session.add(produto)

    # Comita as mudanças no banco de dados
    session.commit()
