from wtforms.validators import email
from flask import Flask, render_template, request, redirect, url_for, flash, g
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate, migrate
from config import DevelopmentConfig
import forms
from models import db, Alumno

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)
csrf = CSRFProtect()
migrate = Migrate(app,db)

@app.route("/", methods = ['GET', 'POST'])
@app.route("/index")
def index():
    create_form = forms.UserForm(request.form)
    alumno = Alumno.query.all()
    
    return render_template("index.html", form = create_form, alumno = alumno)

@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"),404

@app.route("/alumnos", methods = ['GET', 'POST'])
def alumnos():
    create_form = forms.UserForm(request.form)
    
    if request.method == 'POST':
        alumn = Alumno(nombre = create_form.nombre.data,
                       apellidos = create_form.apellidos.data,
                       email = create_form.email.data,
                       telefono = create_form.telefono.data,)
        db.session.add(alumn)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template("alumnos.html", form=create_form)

@app.route("/detalles", methods = ['GET', 'POST'])
def detalles():
    create_form = forms.UserForm(request.form)
    
    if request.method == 'GET':
        id = request.args.get('id')
        alumn1 = db.session.query(Alumno).filter(Alumno.id == id).first()
        nombre = alumn1.nombre
        apellidos = alumn1.apellidos
        email = alumn1.email
        telefono = alumn1.telefono

    return render_template("detalles.html", nombre = nombre, apellidos = apellidos, email = email, telefono = telefono )

@app.route("/modificar", methods = ['GET', 'POST'])
def modificar():
    create_form = forms.UserForm(request.form)
    
    if request.method == 'GET':
        id = request.args.get('id')
        alumn1 = db.session.query(Alumno).filter(Alumno.id == id).first()
        create_form.id.data = request.args.get('id')
        create_form.nombre.data = alumn1.nombre
        create_form.apellidos.data = alumn1.apellidos
        create_form.email.data = alumn1.email
        create_form.telefono.data = alumn1.telefono
    if request.method == 'POST':
        id = create_form.id.data
        alumn1 = db.session.query(Alumno).filter(Alumno.id == id).first()
        alumn1.nombre = str.rstrip(create_form.nombre.data)
        alumn1.apellidos = create_form.apellidos.data
        alumn1.email = create_form.email.data
        alumn1.telefono = create_form.telefono.data
        db.session.add(alumn1)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template("modificar.html", form=create_form)

@app.route("/eliminar", methods = ['GET', 'POST'])
def eliminar():
    create_form = forms.UserForm(request.form)
    
    if request.method == 'GET':
        id = request.args.get('id')
        alumn1 = db.session.query(Alumno).filter(Alumno.id == id).first()
        create_form.id.data = request.args.get('id')
        create_form.nombre.data = alumn1.nombre
        create_form.apellidos.data = alumn1.apellidos
        create_form.email.data = alumn1.email
        create_form.telefono.data = alumn1.telefono
    if request.method == 'POST':
        id = create_form.id.data
        alumn1 = db.session.query(Alumno).filter(Alumno.id == id).first()
        db.session.delete(alumn1)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template("eliminar.html", form=create_form)


if __name__ == '__main__':
    csrf.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)

