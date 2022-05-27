from . import db
from flask_login import UserMixin
from sqlalchemy.orm import relationship



class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    str_role = db.Column(db.String(40))

    def _repr_(self):
        return f'Item {self.id}'


class Competence(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    str_competence = db.Column(db.String(40))

    def _repr_(self):
        return f'Item {self.id}'


class Respensabilite(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    str_respensabilite = db.Column(db.String(40))

    def _repr_(self):
        return f'Item {self.id}'


class Employe(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(20))
    prenom = db.Column(db.String(20))
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(50))
    id_role = db.Column(db.Integer, db.ForeignKey(Role.id))
    role = relationship('Role', foreign_keys='Employe.id_role')
    id_respensabilite = db.Column(db.Integer, db.ForeignKey(Respensabilite.id))
    respensabilite = relationship('Respensabilite', foreign_keys='Employe.id_respensabilite')

    def repr(self):
        return f'Item {self.id}'


class Employe_competence(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_employe = db.Column(db.Integer, db.ForeignKey(Employe.id))
    employe = relationship('Employe', foreign_keys='Employe_competence.id_employe')
    id_competence = db.Column(db.Integer, db.ForeignKey(Competence.id))
    competence = relationship('Competence', foreign_keys='Employe_competence.id_competence')
    premiere_experience = db.Column(db.Date)

    def repr(self):
        return f'Item {self.id}'


class Projet(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titre = db.Column(db.String(40))
    description = db.Column(db.String(100))
    date_debut = db.Column(db.Date())
    date_fin = db.Column(db.Date())
    id_employe = db.Column(db.Integer, db.ForeignKey(Employe.id))
    employe = relationship('Employe', foreign_keys='Projet.id_employe')

    def repr(self):
        return f'Item {self.id}'


class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titre = db.Column(db.String(40))
    description = db.Column(db.String(100))
    id_projet = db.Column(db.Integer, db.ForeignKey(Projet.id))
    projet = relationship('Projet', foreign_keys='Action.id_projet')

    def repr(self):
        return f'Item {self.id}'


class Tache(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titre = db.Column(db.String(40))
    description = db.Column(db.String(100))
    est_fini = db.Column(db.Boolean)
    id_employe = db.Column(db.Integer, db.ForeignKey(Employe.id))
    employe = relationship('Employe', foreign_keys='Tache.id_employe')
    id_action = db.Column(db.Integer, db.ForeignKey(Action.id))
    action = relationship('Action', foreign_keys='Tache.id_action')

    def repr(self):
        return f'Item {self.id}'
