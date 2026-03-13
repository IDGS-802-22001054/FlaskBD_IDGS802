from flask import Blueprint, redirect, render_template, request, url_for
from wtforms import Form, HiddenField, IntegerField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange

from models import Alumno, Curso, Maestros, db


class CursoForm(Form):
    id = HiddenField("Id")
    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=150)])
    descripcion = TextAreaField("Descripcion", validators=[DataRequired()])
    maestro_id = IntegerField("Matricula maestro", validators=[DataRequired(), NumberRange(min=1)])


cursos = Blueprint("cursos", __name__)


@cursos.route("/indexCursos", methods=["GET"])
def index_cursos():
    lista_cursos = Curso.query.all()
    return render_template("indexCursos.html", cursos=lista_cursos)


@cursos.route("/cursos/nuevo", methods=["GET", "POST"])
def nuevo_curso():
    form = CursoForm(request.form)

    if request.method == "POST" and form.validate():
        maestro = Maestros.query.filter_by(matricula=form.maestro_id.data).first_or_404()
        curso = Curso(
            nombre=form.nombre.data,
            descripcion=form.descripcion.data,
            maestro_id=maestro.matricula,
        )
        db.session.add(curso)
        db.session.commit()
        return redirect(url_for("cursos.index_cursos"))

    return render_template("nuevoCurso.html", form=form)


@cursos.route("/cursos/detalles", methods=["GET"])
def detalles_curso():
    id_curso = request.args.get("id", type=int)
    curso = Curso.query.filter_by(id=id_curso).first_or_404()
    alumnos_disponibles = [
        alumno
        for alumno in Alumno.query.order_by(Alumno.nombre, Alumno.apellidos).all()
        if alumno not in curso.alumnos
    ]
    return render_template(
        "detallesCurso.html",
        curso=curso,
        alumnos_disponibles=alumnos_disponibles,
    )


@cursos.route("/cursos/inscribir", methods=["POST"])
def inscribir_alumno():
    curso_id = request.form.get("curso_id", type=int)
    alumno_id = request.form.get("alumno_id", type=int)

    curso = Curso.query.filter_by(id=curso_id).first_or_404()
    alumno = Alumno.query.filter_by(id=alumno_id).first_or_404()

    if alumno not in curso.alumnos:
        curso.alumnos.append(alumno)
        db.session.commit()

    return redirect(url_for("cursos.detalles_curso", id=curso.id))


@cursos.route("/cursos/modificar", methods=["GET", "POST"])
def modificar_curso():
    form = CursoForm(request.form)

    if request.method == "GET":
        id_curso = request.args.get("id", type=int)
        curso = Curso.query.filter_by(id=id_curso).first_or_404()
        form.id.data = curso.id
        form.nombre.data = curso.nombre
        form.descripcion.data = curso.descripcion
        form.maestro_id.data = curso.maestro_id
        return render_template("modificarCurso.html", form=form)

    if request.method == "POST" and form.validate():
        curso = Curso.query.filter_by(id=form.id.data).first_or_404()
        maestro = Maestros.query.filter_by(matricula=form.maestro_id.data).first_or_404()
        curso.nombre = form.nombre.data
        curso.descripcion = form.descripcion.data
        curso.maestro_id = maestro.matricula
        db.session.commit()
        return redirect(url_for("cursos.index_cursos"))

    return render_template("modificarCurso.html", form=form)


@cursos.route("/cursos/eliminar", methods=["GET", "POST"])
def eliminar_curso():
    form = CursoForm(request.form)

    if request.method == "GET":
        id_curso = request.args.get("id", type=int)
        curso = Curso.query.filter_by(id=id_curso).first_or_404()
        form.id.data = curso.id
        form.nombre.data = curso.nombre
        form.descripcion.data = curso.descripcion
        form.maestro_id.data = curso.maestro_id
        return render_template("eliminarCurso.html", form=form)

    if request.method == "POST":
        curso = Curso.query.filter_by(id=form.id.data).first_or_404()
        db.session.delete(curso)
        db.session.commit()
        return redirect(url_for("cursos.index_cursos"))

    return render_template("eliminarCurso.html", form=form)
