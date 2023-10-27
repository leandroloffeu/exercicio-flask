from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345678@127.0.0.1/empresa'
db = SQLAlchemy(app)

   
class Setor(db.Model):
    id_setor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    setor = db.Column(db.String(50), nullable=False)
    
    funcionarios = db.relationship('Funcionario', backref='setor', lazy=True)
    
    def __str__(self):
        return f'Setor {self.setor}'
    
class Funcionario(db.Model):
    id_funcionario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    primeiro_nome = db.Column(db.String(50), nullable=False)
    sobrenome = db.Column(db.String(50), nullable=False)
    data_admissao = db.Column(db.Date, nullable=False)
    status_funcionario = db.Column(db.Integer, nullable=False)    

    id_setor = db.Column(db.Integer, db.ForeignKey('setor.id_setor'), nullable=False)
    cargo_id = db.Column(db.Integer, db.ForeignKey('cargo.id_cargo'), nullable=False)


    def __str__(self):
        return f'Setor {self.primeiro_nome}'
    
    
class Cargo(db.Model):
    id_cargo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cargo = db.Column(db.String(50), nullable=False)   

    funcionarios = db.relationship('Funcionario', backref='cargo', lazy=True)

    def __str__(self):
        return f'Setor {self.nome}'

with app.app_context():
    db.create_all()

# Rotas
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        setor = request.form['setor']   
        novo_setor = Setor(setor=setor)
        db.session.add(novo_setor)

        cargo = request.form['cargo']
        novo_cargo = Cargo(cargo=cargo)
        db.session.add(novo_cargo)           
        db.session.commit()
        
        
        primeiro_nome = request.form['primeiro_nome']  
        sobrenome = request.form['sobrenome']
        data_admissao = request.form['data_admissao']
        status_funcionario = request.form['status_funcionario']

# IDs do setor e cargo criados acima
        id_setor = novo_setor.id_setor
        cargo_id = novo_cargo.id_cargo

        novo_funcionario = Funcionario(primeiro_nome=primeiro_nome, sobrenome=sobrenome, data_admissao=data_admissao,status_funcionario=status_funcionario,
                                       id_setor=id_setor, cargo_id=cargo_id)
        db.session.add(novo_funcionario)
        db.session.commit()
        
        return 'Usuário adicionado com sucesso!'
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
