from flask import Flask,Response,request
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/cadastro"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class ListadeEspera(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    email = db.Column(db.String(50))
    item = db.Column(db.String(15))
    item_desc = db.Column(db.String(50))

    def to_json(self):
        return {"id": self.id,
                "nome": self.nome,
                "email": self.email,
                "item": self.item,
                "item_desc": self.item_desc
                }

@app.route("/cadastro", methods=["GET"])
def selecionar_all():
    lista = ListadeEspera.query.all()
    lista_json = [ListadeEspera.to_json() for ListadeEspera in lista]
    return gera_response(200,"ListadeEspera", lista_json)

@app.route("/cadastro/<item>", methods=["GET"])
def seleciona_unico(item):
    lista = ListadeEspera.query.filter_by(item=item).first()
    lista_json = lista.to_json()

    return gera_response(200,"ListadeEspera", lista_json)

@app.route("/cadastro", methods=["POST"])
def cria_registro():
    body = request.get_json()

    try:
        lista = ListadeEspera(nome=body["nome"],
                              email=body["email"],
                              item=body["item"],
                              item_desc=body["item_desc"])
        db.session.add(lista)
        db.session.commit()
        return gera_response(201, "ListadeEspera", lista.to_json(),"Criado com sucesso")
    except Exception as e:
        print(e)
        return gera_response(400,"ListadeEspera", {}, "Erro ao cadastrar")

@app.route("/cadastro/<item>", methods=["DELETE"])
def deleta_registro(item):
    lista = ListadeEspera.query.filter_by(item=item).first()

    try:
        db.session.delete(lista)
        db.session.commit()
        return gera_response(201, "ListadeEspera", lista.to_json(), "Nome foi retirado da lista de espera desse item com sucesso!")
    except Exception as e:
        print(e)
        print(body)
        return gera_response(400, "ListadeEspera", {}, "Erro ao deletar")

def gera_response(status, nome_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json")

app.run()