from wtforms import Form 
from wtforms import StringField, IntegerField, DateField, EmailField

from wtforms import validators 

class UserForm(Form):
    # lo que aparece en el html 
    id = IntegerField("Matricula", [
        validators.DataRequired(message="El campo es requerido"),
        validators.NumberRange(min=100, max=1000, message="ingrese un valor valido")
    ])

    nombre = StringField("Nombre", [
        validators.DataRequired(message="El campo es requerido"), 
    ])
    
    apaterno = StringField("aPaterno",[
        validators.DataRequired(message="El campo es requerido")
    ])
    email = EmailField("emai;", [
        validators.DataRequired(message="El campo es requerido")
    ])
    created_date = DateField("created_date", [
        validators.DataRequired(message="Ingrese un correo valido")
    ])