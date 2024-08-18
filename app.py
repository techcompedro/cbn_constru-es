from flask import Flask, render_template, request, redirect
from database import Produtos, session
app = Flask(__name__)

@app.route('/')
def index ():
    categogias = [ 'Calçados',  'Acessórios', 'Roupas' ]
    voltar_inicio  = 'voltar'
    if voltar_inicio == 'voltar':
        produtos = session.query(Produtos).all()
        session.commit()
        
    produtos = session.query(Produtos).all()
    return render_template('index.html', produtos=produtos, categogias=categogias)
    
@app.route('/filtrar_categoria', methods=['POST'])
def filtrar_categoria():
    categoria_desejada = request.form.get('categoria')
    categorias = ['Calçados', 'Acessórios', 'Roupas']

    if categoria_desejada in categorias:
        produtos_filtrados = session.query(Produtos).filter(Produtos.categoria == categoria_desejada).all()
    else:
        produtos_filtrados = []

    session.commit()
    return render_template('index.html', produtos=produtos_filtrados)

if __name__ == '__main__':
    app.run(debug=True)
