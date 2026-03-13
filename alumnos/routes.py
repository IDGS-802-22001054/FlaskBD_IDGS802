from flask import Blueprint, render_template, request, redirect, url_for
import forms
from models import db, Alumno

alumnos = Blueprint("alumnos", __name__)

@alumnos.route("/indexAlumnos", methods=["GET"])
def index_alumnos():
    alumno = Alumno.query.all()
    return render_template("indexAlumnos.html", alumno=alumno)


@alumnos.route("/alumnos", methods=["GET", "POST"])
def alumnos_index():
    create_form = forms.UserForm(request.form)

    if request.method == "POST":
        alumn = Alumno(
            nombre=create_form.nombre.data,
            apellidos=create_form.apellidos.data,
            email=create_form.email.data,
            telefono=create_form.telefono.data,
        )
        db.session.add(alumn)
        db.session.commit()
        return redirect(url_for("alumnos.index_alumnos"))

    return render_template("alumnos.html", form=create_form)


@alumnos.route("/detalles", methods=["GET", "POST"])
def detalles():
    if request.method == "GET":
        id = request.args.get("id")
        alumn1 = db.session.query(Alumno).filter(Alumno.id == id).first()
        nombre = alumn1.nombre
        apellidos = alumn1.apellidos
        email = alumn1.email
        telefono = alumn1.telefono

    return render_template(
        "detalles.html",
        nombre=nombre,
        apellidos=apellidos,
        email=email,
        telefono=telefono,
    )


@alumnos.route("/modificar", methods=["GET", "POST"])
def modificar():
    create_form = forms.UserForm(request.form)

    if request.method == "GET":
        id = request.args.get("id")
        alumn1 = db.session.query(Alumno).filter(Alumno.id == id).first()
        create_form.id.data = request.args.get("id")
        create_form.nombre.data = alumn1.nombre
        create_form.apellidos.data = alumn1.apellidos
        create_form.email.data = alumn1.email
        create_form.telefono.data = alumn1.telefono

    if request.method == "POST":
        id = create_form.id.data
        alumn1 = db.session.query(Alumno).filter(Alumno.id == id).first()
        alumn1.nombre = str.rstrip(create_form.nombre.data)
        alumn1.apellidos = create_form.apellidos.data
        alumn1.email = create_form.email.data
        alumn1.telefono = create_form.telefono.data
        db.session.add(alumn1)
        db.session.commit()
        return redirect(url_for("alumnos.index_alumnos"))

    return render_template("modificar.html", form=create_form)


@alumnos.route("/eliminar", methods=["GET", "POST"])
def eliminar():
    create_form = forms.UserForm(request.form)

    if request.method == "GET":
        id = request.args.get("id")
        alumn1 = db.session.query(Alumno).filter(Alumno.id == id).first()
        create_form.id.data = request.args.get("id")
        create_form.nombre.data = alumn1.nombre
        create_form.apellidos.data = alumn1.apellidos
        create_form.email.data = alumn1.email
        create_form.telefono.data = alumn1.telefono

    if request.method == "POST":
        id = create_form.id.data
        alumn1 = db.session.query(Alumno).filter(Alumno.id == id).first()
        db.session.delete(alumn1)
        db.session.commit()
        return redirect(url_for("alumnos.index_alumnos"))

    return render_template("eliminar.html", form=create_form)
