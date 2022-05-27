

from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
import flask
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = Employe.query.filter_by(email=email).first()
        if user:
            role = user.role.str_role
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                if role == 'chef de projet':
                    return redirect(url_for('views.homechef'))
                else:
                    return redirect(url_for('views.homeemp'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    logout_user()
    return render_template("login.html",user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        role_id = request.form.get('id_role')
        responsabilite_id = request.form.get('id_responsabilite')
        competence_id = request.form.getlist('id_competence')
        user = Employe.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
            return redirect('signup')
        if len(email) < 5:
            flash('Email must be greater than 3 characters.', category='error')
            return redirect('signup')
        if len(nom) < 2:
            flash('First name must be greater than 1 character.', category='error')
            return redirect('signup')
        if password != password_confirm:
            flash('Passwords don\'t match.', category='error')
            return redirect('signup')
        if len(password) < 7:
            flash('Password must be at least 7 characters.', category='error')
            return redirect('signup')
        
        new_user = Employe(nom=nom,prenom=prenom,email=email, password=generate_password_hash(password, method='sha256'),id_role=role_id,id_respensabilite=responsabilite_id)
        db.session.add(new_user)
        db.session.commit()
        for competence in competence_id : 
            new_comptence = Employe_competence(id_employe=new_user.id,id_competence=competence)
            db.session.add(new_comptence)
        db.session.commit()
        login_user(new_user, remember=True)
        flash('Account created!', category='success')
        return redirect(url_for('views.homechef'))
    competences =  Competence.query.all()
    return render_template("employe.html",user=current_user, competences = competences)

@auth.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        iden = request.form.get('iden')
        data = Employe.query.get(iden)
        data.nom = request.form.get('nome')
        data.prenom = request.form.get('prenom')
        data.email = request.form.get('email')
        passnew = request.form.get('newpass')
        data.password = generate_password_hash(passnew, method='sha256')
        data.id_role = request.form.get('id_role')
        data.id_respensabilite = request.form.get('id_respensabilite')
        data.id_competence = request.form.get('id_competence')
        db.session.commit()
        flash("Employee Updated Successfully")
        return redirect(url_for('views.homechef'))
    return render_template("employee.html",user=current_user)


@auth.route('/delete/<id>/')
def delete(id):
    data = Employe.query.get(id)
    db.session.delete(data)
    db.session.commit()
    flash("Employee Deleted Successfully")
    return redirect(url_for('views.homechef'))

@auth.route('/addprojet', methods=['GET', 'POST'])
def addprojet():
    if request.method == 'POST':
        titre = request.form.get('Titre')
        description = request.form.get('description')
        datedebut_str = request.form.get('datedebut')
        datedebut = datetime.strptime(datedebut_str, '%Y-%m-%d')
        datefin_str = request.form.get('datefin')
        datefin = datetime.strptime(datefin_str, '%Y-%m-%d')
        projt = Projet.query.filter_by(titre=titre).first()
        if projt:
            flash('Project already exists.', category='error')
            return redirect('addprojet')
        if datedebut > datefin:
            flash('Date debut superieur a la date de fin !!',category='error')
            return redirect('addprojet')
        newprjt = Projet(titre=titre,description=description, date_debut=datedebut , date_fin=datefin,id_employe=1)
        db.session.add(newprjt)
        db.session.commit()
        flash('Project created sucessfully!', category='success')
        return redirect(url_for('views.homechef'))
    return render_template("projet.html",user=current_user,projets=Projet)


@auth.route('/delete2/<id>/')
def delete2(id):
    data = Projet.query.get(id)
    idp = Action.query.filter_by(id_projet=data.id).all()
    for act in idp:
        taches = Tache.query.filter_by(id_action=act.id).all()
        for tache in taches:
            db.session.delete(tache)
    for i in range(len(idp)):
        db.session.delete(idp[i])
    db.session.delete(data)
    db.session.commit()
    flash("Projet Deleted Successfully")
    return redirect(url_for('views.homechef'))

@auth.route('/ajouttache', methods=['POST','GET'])
def ajouttache():
    if request.method == "POST":
        tit = request.form.get('titre')
        desc = request.form.get('description')
        fini = int(request.form.get('rad'))
        id_emp = int(request.form.get('id_emp'))
        id_act = request.form.get('id')
        tach = Tache.query.filter_by(titre=tit).first()
        if tach:
            flash("Tache existe dans la base de donnee",category='error')
            redirect('ajouttache')
        new_tache = Tache(titre=tit,description=desc,est_fini=fini,id_employe=id_emp,id_action=id_act)
        db.session.add(new_tache)
        db.session.commit()
        flash('Tache created sucessfully!', category='success')
        return redirect(url_for('views.afficherprojet'))
    return render_template("afficher.html",user=current_user)


@auth.route('/deleteaction',methods=['POST','GET'])
def deleteaction():
    if request.method == "POST":
        idact = int(request.form.get('id_action'))
        idprojet = int (request.form.get('id_projet'))
        action = Action.query.filter_by(id=idact).first()
        taches = Tache.query.filter_by(id_action=idact).all()
        for tache in taches:
            db.session.delete(tache)
        db.session.delete(action)
        db.session.commit()
        return redirect(url_for('views.affichage',id=idprojet))

@auth.route('/updateact',methods= ['POST','GET'])
def updateact():
    if request.method == "POST":
        ident = request.form.get('iden')
        idact = Action.query.get(ident)
        idact.titre = request.form.get('titrenew')
        idact.description = request.form.get('description')
        idact.est_fini = int(request.form.get('rad'))
        db.session.commit()
        flash("Action Updated Successfully")
        return redirect(url_for('views.afficherprojet'))
    return render_template('affichage.html',user=current_user)

@auth.route('/ajoutaction', methods=['POST','GET'])
def ajoutaction():
    if request.method == "POST":
        tit = request.form.get('titre')
        desc = request.form.get('description')
        act = Action.query.filter_by(titre=tit).first()
        id_pro = request.form.get('id')
        if act:
            flash("Action existe dans la base de donnee",category='error')
            return redirect(url_for('views.afficherprojet'))
        new_action = Action(titre=tit,description=desc,id_projet=id_pro)
        db.session.add(new_action)
        db.session.commit()
        flash('Action created sucessfully!', category='success')
        return redirect(url_for('views.afficherprojet'))
    return render_template("afficher.html",user=current_user)

@auth.route('/editertache',methods=['POST','GET'])
def editertache():
    if request.method == "POST":
        itache = request.form.get('iden')
        tach = Tache.query.get(itache)
        tach.titre = request.form.get('titrenew')
        tach.description = request.form.get('description')
        tach.id_employe = int(request.form.get('idemploye'))
        tach.est_fini = int(request.form.get('rad'))
        db.session.commit()
        return redirect(url_for('views.taches',id=tach.id_action))
    return render_template('tachesaff.html',user=current_user)

@auth.route('/deletetache/<id>')
def deletetache(id):
    data = Tache.query.get(id)
    idact = data.id_action
    db.session.delete(data)
    db.session.commit()
    flash("Tache Deleted Successfully")
    return redirect(url_for('views.taches',id=idact))


