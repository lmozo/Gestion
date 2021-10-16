import os
from flask import Flask, request
from flask.templating import render_template
from forms import FormEmpleado, FormLogin
from listas import lista_usuarios, lista_empleados
from forms import FormRegistro
# FormCrearEmadople,

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

"""@app.route("/")
def index():
    return render_template('index.html')

@app.route("/")
def logins():
    return render_template('login.html')"""

@app.route('/', methods=["GET", "POST"])
def login():
    mensaje = ""

    if request.method == "GET":
        formulario = FormLogin()
        return render_template('index.html', titulo='Iniciar Sesión', form=formulario)
    else:
        formulario = FormLogin(request.form)
        if formulario.validate_on_submit():
            if validar_login(formulario.usuario.data,formulario.password.data):
                mensaje = "El usuario {0} inició sesión".format(formulario.usuario.data)
                return render_template('Index.html',mensaje=mensaje)
            else:
                mensaje = "Los datos ingresados NO son válidos."
               
        mensaje += "Todos los datos son requeridos"
        return render_template('index.html',form=FormLogin(), mensaje=mensaje)

@app.route("/crear_usuario/")
def crear_u():
    return render_template('crear_usuario.html')

@app.route("/editar_usuario/")
def editar_u():
    return render_template('editar_usuario.html')

@app.route("/consultar_usuario/")
def consultar_u():
    return render_template('consultar_usuario.html')

@app.route("/crear_empleado/")
def crear_e():
    return render_template('crear_empleado.html')

@app.route("/editar_empleado/")
def editar_e():
    return render_template('editar_empleado.html')

@app.route("/consultar_empleado/")
def consultar_e():
    return render_template('consultar_empleado.html')

@app.route("/evaluacion/")
def evaluacion():
    return render_template('evaluacion.html')

@app.route("/empleado_evaluar/")
def empleado_evaluar():
    return render_template('empleado_evaluar.html')

@app.route('/registro/', methods=('GET', 'POST'))
def registro():
    mensaje = ""
    if request.method == "GET": 
        formulario = FormRegistro()
        return render_template('registro.html', form = formulario)
    else:
        formulario = FormRegistro(request.form)
        if formulario.validate_on_submit():
            if not validar_usuario(formulario.usuario.data):
                mensaje += "El usuario no es válido o ya fue registrado"    
            if (formulario.password.data != formulario.repassword.data):
                mensaje += "Las contraseñas no coinciden."   
        else:
            mensaje += "Todos los datos son requeridos."
        
        if not mensaje:
            if (registrar_usuario(formulario.usuario.data, formulario.password.data)):
                mensaje = "Su cuenta ha sido registrada, puede iniciar sesión."
            else:
                mensaje += "Ocurrió un error durante el registro, por favor intente nuevamente."

            return render_template('registro.html', form=formulario, mensaje = mensaje)
        else:
            return render_template('registro.html',form=formulario, mensaje = mensaje)

@app.route('/AdministracionEmpleados/CrearEmpleado', methods=('GET', 'POST'))
def crearEmpleado():
    mensaje = ""
    if request.method == "GET": 
        formulario = FormEmpleado()
        return render_template('crear_empleado.html', form = formulario)
    else:
        formulario = FormEmpleado(request.form)
        if formulario.validate_on_submit():
            if registrar_empleado(formulario.data):
                 mensaje += "Empleado registrado exitosamente."
            else:
                mensaje += "Ocurrió un error durante el registro del empleado, por favor intente nuevamente."
        else:
            mensaje += "Todos los datos son requeridos."
        
        return render_template('crear_empleado.html',form=formulario, mensaje = mensaje)

def validar_login(usuario,password):
    for i in range(len(lista_usuarios)):
        if lista_usuarios[i]["usuario"] == usuario:
            if lista_usuarios[i]["password"] == password:
                return True

    return False

def validar_usuario(usuario):
    for i in range(len(lista_usuarios)):
        if lista_usuarios[i]["usuario"] == usuario:
            if lista_usuarios[i]["password"] == None:
                return True

    return False

def registrar_usuario(usuario,contrasena):
    id = len(lista_usuarios) + 1
    lista_usuarios.append({"id": id,"usuario": usuario,"password": contrasena})
    return True    
    