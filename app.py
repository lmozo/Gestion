import os
from flask import Flask, request
from flask.templating import render_template
from forms import FormEmpleado, FormLogin, FormUsuario
from listas import lista_usuarios, lista_empleados
from forms import FormRegistro
from models import empleado, usuario
# FormCrearEmadople,

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


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
                return render_template('Index.html',form=FormLogin(),mensaje=mensaje)
            else:
                mensaje = "Los datos ingresados NO son válidos."
               
        mensaje += "Todos los datos son requeridos"
        return render_template('index.html',form=formulario, mensaje=mensaje)


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


@app.route("/menu/")
def menu():
    return render_template('menu.html')

@app.route("/crear_usuario/")
def crear_u():
    mensaje = ""
    if request.method == "GET": 
        formulario = FormUsuario()
        return render_template('crear_usuario.html', form = formulario)
    else:
        formulario = FormUsuario(request.form)
        if formulario.validate_on_submit():
            #falta-con la identificación debo consultar primero el id del empleado para verificar que exista y no tenga ya usuario asociado y luego instanciar un objeto usuario
            obj_usuario = usuario(p_id=0, p_id_empleado = formulario.identificacion.data, p_login=formulario.usuario.data,
            p_password = None, p_id_rol = formulario.rol.data, p_estado='A', p_creado_por = 'admin', p_creado_en = '2021-10-25')

            #falta-Debo validar antes de la inserción que no haya ya un usuario creado con ese mismo login
            if obj_usuario.insertar():
                return render_template("crear_usuario.html", form=FormUsuario(), mensaje= "El usuario ha sido creado.")
            else:
                return render_template("crear_usuario.html", form=formulario, mensaje= "No fue posible crear el usuario, consulte a soporte técnico.")

        return render_template("crear_usuario.html", form=formulario, mensaje = "Todos los datos son requeridos.")


@app.route("/editar_usuario/")
def editar_u():
    mensaje = ""
    if request.method == "GET": 
        formulario = FormUsuario()
        return render_template('editar_usuario.html', form = formulario)
    else:
        formulario = FormUsuario(request.form)
        if formulario.validate_on_submit():
            obj_usuario = usuario(p_id=0, p_id_empleado = formulario.identificacion.data, p_login=formulario.usuario.data,
            p_password = None, p_id_rol = formulario.rol.data, p_estado='A', p_creado_por = 'admin', p_creado_en = '2021-10-25')

            #falta-Debo validar antes de la inserción que no haya ya un usuario creado con ese mismo login
            if obj_usuario.editar():
                return render_template("crear_usuario.html", form=FormUsuario(), mensaje= "El usuario ha sido editado.")
            else:
                return render_template("crear_usuario.html", form=formulario, mensaje= "No fue posible editar el usuario, consulte a soporte técnico.")

        return render_template("crear_usuario.html", form=formulario, mensaje = "Todos los datos son requeridos.")



@app.route("/consultar_usuario/")
def consultar_u():
    return render_template('consultar_usuario.html')

@app.route("/crear_empleado/")
def crear_e():
    mensaje = ""
    if request.method == "GET": 
        formulario = FormEmpleado()
        return render_template('crear_empleado.html', form = formulario)
    else:
        formulario = FormEmpleado(request.form)
        if formulario.validate_on_submit():
            #falta- incluir validaciones para asegurar que no exista esa identificación ya registrada
            obj_empleado = empleado(p_id=0, p_tipo_identificacion = formulario.tipoIdentificacion.data, 
            p_numero_identificacion = formulario.identificacion.data, p_nombre = formulario.nombre.data,
            p_id_tipo_contrato = formulario.idTipoContrato, p_fecha_ingreso = formulario.fechaIngreso.data,
            p_fecha_fin_contrato = formulario.fechaFin.data, p_id_dependencia = formulario.idDependencia.data,
            p_id_cargo = formulario.idCargo.data, p_salario = formulario.salario.data, p_id_jefe = formulario.idJefe.data, 
            p_es_jefe = formulario.esJefe.data, p_estado='A', p_creado_por = 'admin', p_creado_en = '2021-10-25')

            #falta-Debo validar antes de la inserción que no haya ya un usuario creado con ese mismo login
            if obj_empleado.insertar():
                return render_template("crear_empleado.html", form=FormUsuario(), mensaje= "El empleado ha sido creado.")
            else:
                return render_template("crear_empleado.html", form=formulario, mensaje= "No fue posible crear el empleado, consulte a soporte técnico.")

        return render_template("crear_empleado.html", form=formulario, mensaje = "Todos los datos son requeridos.")



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


"""@app.route('/admin_empleados/crear_empleado/', methods=('GET', 'POST'))
def crear_empleado():
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
"""

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
    