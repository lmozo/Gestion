from datetime import date
from flask_wtf import FlaskForm
from werkzeug.utils import ArgumentValidationError
from wtforms.fields.core import BooleanField, DateField, FloatField, IntegerField, StringField
from wtforms.fields.simple import PasswordField, SubmitField
from wtforms import validators

class FormLogin(FlaskForm):
    usuario = StringField('Usuario',validators=[validators.required(message="Esciba el usuario"),validators.length(max=20)])
    password = PasswordField('Contraseña',validators=[validators.required(message="Esciba la contraseña"),validators.length(max=50)])
    ingresar = SubmitField("Ingresar")

class FormRegistro(FlaskForm):
    usuario = StringField('Usuario',validators=[validators.required(message="Esciba el usuario"),validators.length(max=20)])
    password = PasswordField('Password',validators=[validators.required(message="Escriba la contraseña"),validators.length(max=50, min=10)])
    repassword = PasswordField("Confirmar Password", validators=[validators.required(message="Re escriba la contraseña"),validators.length(max=50, min=10),])
    enviar = SubmitField("Registrar")

class FormEmpleado(FlaskForm):
    tipoIdentificacion = StringField('Tipo de Identificacion',validators=[validators.required()])
    identificacion = StringField('Número de Identificación',validators=[validators.required(message="Esciba la identificación"),validators.length(max=20)])
    nombre = StringField('Nombre del Empleado',validators=[validators.required(message="Esciba la identificación"),validators.length(max=50, min=5)])
    correo = StringField('Correo Electrónico', validators=[validators.required(message="El correo electrónico es obligatorio"),validators.length(max=150)])
    idArea = StringField('Área', validators=[validators.required(message="El área es obligatorio")])
    idCargo = StringField('Cargo', validators=[validators.required(message="El cargo es obligatorio")])
    idTipoContrato = IntegerField('Tipo de Contrato', validators=[validators.required(message="El tipo de contraro es obligatorio")])
    fechaIngreso = DateField('Fecha de Ingreso', validators=[validators.required(message="La fecha de ingreso es requerida")])
    fechaFin = DateField('Fecha Final del Contrato')
    salario = FloatField('Salario', validators=[validators.required(message="El salario es requerido")])
    idJefe = IntegerField('Jefe')
    esJefe = BooleanField('¿Es Jefe?', validators=[validators.required(message="Indique si el empleado se desempeñará o no como jefe")])
    registrar = SubmitField("Registrar")

class FormUsuario(FlaskForm):
    usuario = StringField('Usuario',validators=[validators.required(message="Escriba el usuario"),validators.length(max=20)])
    identificacion = PasswordField('Identificacion',validators=[validators.required(message="Escriba su numero de Identificacion")])
    area = StringField('Area',validators=[validators.required(message="Por favor ingrese el area, a la cual pertenece")])
    cargo = StringField('Cargo',validators=[validators.required(message="Por favor ingrese el cargo en el cual se desempeña")])
    


