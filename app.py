from flask import Flask, render_template, request, redirect, session as flask_session, url_for
from database import User, Produtos, session
from werkzeug.security import generate_password_hash, check_password_hash
import os
app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/', methods=['GET', 'POST'])
def index ():
    if 'user_id' not in flask_session:  # Verifica corretamente a sessão do Flask
        return redirect('/login')
    categogias = [ 'Calçados',  'Acessórios', 'Roupas' ]
    voltar_inicio  = 'voltar'
    if voltar_inicio == 'voltar':
        produtos = session.query(Produtos).all()
        session.commit()
    produtos = session.query(Produtos).all()
    session.commit()
    return render_template('index.html', produtos=produtos, categogias=categogias)
    
@app.route('/filtrar_categoria', methods=['POST'])
def filtrar_categoria():
    categoria_desejada = request.form.get('categoria')
    categorias = ['Calçados', 'Acessórios', 'Roupas','Eletrônicos', 'Roupas', 'Alimentos', 'Livros', 'Brinquedos']

    if categoria_desejada in categorias:
        produtos_filtrados = session.query(Produtos).filter(Produtos.categoria == categoria_desejada).all()
    else:
        produtos_filtrados = []
    session.commit()
    return render_template('index.html', produtos=produtos_filtrados)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cargo = request.form['role']  # O papel do usuário é selecionado no formulário
        hashed_password = generate_password_hash(password)

        new_user = User(username=username, password=hashed_password, cargo=cargo)
        session.add(new_user)
        session.commit()
        return redirect('/login')

    return render_template('register.html')

@app.route('/editar/<int:produto_id>', methods=['GET', 'POST'])
def editar(produto_id):
    if 'user_id' not in flask_session:
        return redirect('/login')

    user_id = flask_session['user_id']
    user = session.query(User).filter_by(id=user_id).first()

    if user.role not in ['gerente', 'chefe']:
        return "Você não tem permissão para editar produtos.", 403

    produto = session.query(Produtos).filter_by(id=produto_id).first()
    if request.method == 'POST':
        # Código para editar o produto
        return redirect('/')

    return render_template('editar.html', produto=produto)

@app.route('/deletar/<int:produto_id>', methods=['POST'])
def deletar(produto_id):
    if 'user_id' not in flask_session:
        return redirect('/login')

    user_id = flask_session['user_id']
    user = session.query(User).filter_by(id=user_id).first()

    if user.role != 'gerente':
        return "Você não tem permissão para deletar produtos.", 403

    produto = session.query(Produtos).filter_by(id=produto_id).first()
    session.delete(produto)
    session.commit()
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = session.query(User).filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            flask_session['user_id'] = user.id
            return redirect('/')
        else:
            error = "Login falhou! Verifique suas credenciais ou "
            register_link = "<a href='/register'>registre-se aqui</a>."
            return render_template('login.html', error=error + register_link)

    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
