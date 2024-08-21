from flask import Flask, render_template, request, redirect, session as flask_session, url_for
from database import User, Produtos, session
from werkzeug.security import generate_password_hash, check_password_hash
import os
app = Flask(__name__)
app.secret_key = os.urandom(24)

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        new_user = User(username=username, password=hashed_password)
        session.add(new_user)
        session.commit()
        return flask_session('/login')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = session.query(User).filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            flask_session['user_id'] = user.id
            return redirect('/one')
        else:
            error = "Login falhou! Verifique suas credenciais ou "
            register_link = "<a href='/register'>registre-se aqui</a>."
            return render_template('login.html', error=error + register_link)

    return render_template('login.html')
@app.route('/one')
def one():
    if 'user_id' not in flask_session:  # Verifica corretamente a sessão do Flask
        return redirect('/login')
    user_id = flask_session['user_id']
    con = session.query(Produtos).filter_by(user_id=user_id).all()
    produtos = session.query(Produtos).all()
    return render_template('index2chefe.html', produtos=produtos, con=con)



if __name__ == '__main__':
    app.run(debug=True)
