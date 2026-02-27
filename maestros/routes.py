from flask import Blueprint, redirect, render_template, request, url_for
from models import Maestros, db

maestros = Blueprint("maestros", __name__)


@maestros.route("/maestros", methods=["GET"])
def maestros_index():
    lista_maestros = Maestros.query.all()
    return render_template("indexMaestros.html", maestros=lista_maestros)


@maestros.route("/maestros/nuevo", methods=["GET", "POST"])
def agregar_maestro():
    if request.method == "POST":
        nuevo_maestro = Maestros(
            nombre=request.form.get("nombre"),
            apellidos=request.form.get("apellidos"),
            especialidad=request.form.get("especialidad"),
            email=request.form.get("email"),
        )
        db.session.add(nuevo_maestro)
        db.session.commit()
        return redirect(url_for("maestros.maestros_index"))

    return render_template("nuevoMaestro.html")

@maestros.route("/maestros/detalles", methods=["GET"])
def detalles_maestro():
    matricula = request.args.get("matricula", type=int)
    maestro = Maestros.query.filter_by(matricula=matricula).first_or_404()
    return render_template("detallesMaestro.html", maestro=maestro)


@maestros.route("/maestros/modificar", methods=["GET", "POST"])
def modificar_maestro():
    if request.method == "POST":
        matricula = request.form.get("matricula", type=int)
        maestro = Maestros.query.filter_by(matricula=matricula).first_or_404()
        maestro.nombre = request.form.get("nombre")
        maestro.apellidos = request.form.get("apellidos")
        maestro.especialidad = request.form.get("especialidad")
        maestro.email = request.form.get("email")
        db.session.commit()
        return redirect(url_for("maestros.maestros_index"))

    matricula = request.args.get("matricula", type=int)
    maestro = Maestros.query.filter_by(matricula=matricula).first_or_404()
    return render_template("modificarMaestro.html", maestro=maestro)


@maestros.route("/maestros/eliminar", methods=["GET", "POST"])
def eliminar_maestro():
    if request.method == "POST":
        matricula = request.form.get("matricula", type=int)
        maestro = Maestros.query.filter_by(matricula=matricula).first_or_404()
        db.session.delete(maestro)
        db.session.commit()
        return redirect(url_for("maestros.maestros_index"))

    matricula = request.args.get("matricula", type=int)
    maestro = Maestros.query.filter_by(matricula=matricula).first_or_404()
    return render_template("eliminarMaestro.html", maestro=maestro)
