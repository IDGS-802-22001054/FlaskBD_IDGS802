from flask import Flask, render_template, request, redirect, url_for, flash, g
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate, migrate
from config import DevelopmentConfig
import forms
from models import db, Alumno
from alumnos.routes import alumnos
from cursos.routes import cursos
from maestros.routes import maestros

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.register_blueprint(alumnos)
app.register_blueprint(cursos)
app.register_blueprint(maestros)
db.init_app(app)
csrf = CSRFProtect()
migrate = Migrate(app,db)

@app.route("/", methods = ['GET', 'POST'])
@app.route("/index")
def index():
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"),404

if __name__ == '__main__':
    csrf.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)

