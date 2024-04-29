from sqlalchemy.orm import relationship

from main import db

class Receita(db.Model):
    id_receita = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100))
    valor = db.Column(db.String(254))
    data = db.Column(db.String(100))

class Despesa(db.Model):
    id_despesa = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100))
    valor = db.Column(db.String(254))
    data = db.Column(db.String(100))

class Usuario(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(254))
    senha = db.Column(db.String(50))
    despesas = relationship("Despesa", back_populates="usuario")
    receitas = relationship("Receita", back_populates="usuario")