
from datetime import datetime
from flask import Blueprint, flash, render_template, request,url_for,redirect
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import *
views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def homelogout():
    return redirect(url_for('auth.logout'))

@views.route('/home1', methods=['GET', 'POST'])
@login_required
def home1():
    return render_template('home.html',user=current_user)



@views.route('/homechef')
@login_required
def homechef():
    return render_template('homechef.html',user=current_user)

@views.route('/homeemp')
@login_required
def homeemp():
    taches = Tache.query.filter_by(id_employe=current_user.id)
    projects_dict = {}
    actions = {}

    """
    projects = [
        {
            "project" : project_object,
            "actions" : [
                {
                    "action" : action_object
                    "taches" : [
                        tache_object,
                        ...
                    ]
                },
                ...
            ]
        },
        {
            ...
        },
        ...
    ]
    """

    for tache in taches:
        if tache.id_action not in actions:
            actions[tache.id_action] = {
                "action" : tache.action,
                "taches" : []
            }
        actions[tache.id_action]["taches"].append(tache)

    for dictionary in actions.values():
        if dictionary["action"].id_projet not in projects_dict:
            projects_dict[dictionary["action"].id_projet] = {
                "project" : dictionary["action"].projet,
                "actions" : []
            }
        projects_dict[dictionary["action"].id_projet]["actions"].append(dictionary)
    
    projects = []

    for proj_dict in projects_dict.values():
        projects.append(proj_dict)

    return render_template('homeemp.html',user=current_user, projects=projects)


@views.route('/test')
def test():
    new_respensabilite1 = Respensabilite(str_respensabilite="Coder")
    db.session.add(new_respensabilite1)
    new_respensabilite2 = Respensabilite(str_respensabilite="Test unitaire")
    db.session.add(new_respensabilite2)
    new_compt1 = Competence(str_competence="c++")
    db.session.add(new_compt1)
    new_compt2 = Competence(str_competence="java")
    db.session.add(new_compt2)
    new_compt3 = Competence(str_competence="Javascript")
    db.session.add(new_compt3)
    new_compt4 = Competence(str_competence="html/css")
    db.session.add(new_compt4)
    new_role = Role(str_role="chef de projet")
    db.session.add(new_role)
    new_role2 = Role(str_role="developpeur")
    db.session.add(new_role2)
    new_resp = Respensabilite(str_respensabilite="appweb")
    db.session.add(new_resp)
    new_user2 = Employe(nom="admin",email='admin1@gmail.com', password=generate_password_hash('test123', method='sha256'),id_role=1,id_respensabilite=1)
    db.session.add(new_user2)
    new_emp_com = Employe_competence(id_employe=1,id_competence=1)
    db.session.add(new_emp_com)
    new_emp_com = Employe_competence(id_employe=1,id_competence=2)
    db.session.add(new_emp_com)
    new_user = Employe(email='mustapha15@gmail.com', password=generate_password_hash('test123', method='sha256'),id_role=2,id_respensabilite=1)
    db.session.add(new_user)
    newprojet = Projet(titre="carshelp",description="application web",date_debut=datetime.strptime("2020-5-11", '%Y-%m-%d'),date_fin=datetime.strptime("2021-5-11", '%Y-%m-%d'), id_employe=1)
    db.session.add(newprojet)
    newprojet2 = Projet(titre="whatssap",description="application mobile",date_debut=datetime.strptime("2020-5-2", '%Y-%m-%d'),date_fin=datetime.strptime("2021-6-19", '%Y-%m-%d'), id_employe=1)
    db.session.add(newprojet2)
    newaction = Action(titre="action1",description="commitdescription",id_projet=1)
    db.session.add(newaction)
    newaction2 = Action(titre="action2",description="rollback description",id_projet=1)
    db.session.add(newaction2)
    newaction4 = Action(titre="action4",description="descriptio,",id_projet=2)
    db.session.add(newaction4)
    newaction5 = Action(titre="action5",description="descript",id_projet=2)
    db.session.add(newaction5)
    newaction2 = Action(titre="action3",description="tttt description",id_projet=2)
    db.session.add(newaction2)
    newtache = Tache(titre="tache 1",description="tache html/css",est_fini=False,id_employe=2,id_action=1)
    db.session.add(newtache)
    newtache2 = Tache(titre="tache 2",description="flask task",est_fini=False,id_employe=3,id_action=2)
    db.session.add(newtache2)
    newtache3 = Tache(titre="tache 3",description="flask pask",est_fini=False,id_employe=5,id_action=5)
    db.session.add(newtache3)
    db.session.commit()
    
    return redirect(url_for('views.homelogout'))

@views.route('/vis')
def visualiser():
    competences = Competence.query.all()
    return render_template('employe.html',competences=competences,user=current_user)

    #testing1222
@views.route('/afficheremp')
def index():
    employees = Employe.query.order_by(Employe.id).all()
    employee = list()
    for emp in employees:
        responsabilite = ''
        roles = ''
        if emp.role:
            roles = emp.role.str_role
        if emp.respensabilite:
            responsabilite = emp.respensabilite.str_respensabilite
        emp_dict = {'id':emp.id ,'nom':emp.nom,'prenom':emp.prenom ,'email':emp.email,'role':roles,'respensabilite':responsabilite}
        competences = ''
        empcomp = Employe_competence.query.filter_by(id_employe=emp.id)
        for comp in empcomp:
            competences += ', ' + comp.competence.str_competence
        emp_dict['competences'] = competences
        employee.append(emp_dict)
    return render_template('afficher.html',employee=employee,user=current_user)

@views.route('/afficherprojet')
def afficherprojet():
    projets = Projet.query.order_by(Projet.id).all()
    return render_template('afficherprojet.html',projets=projets ,user=current_user)


@views.route('/affichage/<id>', methods=['GET','POST'])
def affichage(id):
    idemp = int(id)
    projects = Projet.query.filter_by(id=idemp)# .filter_by  importation d'une liste !!!
    actions = Action.query.filter_by(id_projet=idemp)
    listd=dict()
    for act in actions :
        progress=0
        taches = Tache.query.filter_by(id_action=act.id)
        nbTache= 0 
        nbTacheFini= 0
        for tach in taches:
            nbTache += 1
            if tach.est_fini :
                nbTacheFini += 1
        if nbTache== 0:        
            continue
        progress= int((nbTacheFini/nbTache)*100)
        listd[act.id]= progress
    return render_template("affichage.html",user=current_user,project=projects[0],Action=actions, listd=listd)

@views.route('/tacheafficher/<id>',methods=['GET','POST'])
def taches(id):
        idemp = int(id)
        taches = Tache.query.filter_by(id_action=idemp)
        return render_template('tachesaff.html',user=current_user,taches=taches)


@views.route('/validertache',methods=['GET','POST'])
@login_required
def validertache():
    if request.method == 'POST':
        idtach = int(request.form.get('idTache'))
        tache = Tache.query.filter_by(id=idtach).first()
        tache.est_fini = True
        db.session.commit()
        return redirect(url_for('views.homeemp'))

