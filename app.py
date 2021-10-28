import datetime
import os
import functools

from werkzeug.utils import redirect
from wtforms.form import Form

from flask import Flask, jsonify, render_template, request, g, url_for, session
from flask.templating import render_template
from db import ejecutar_select
from forms import FormRegistro, FormLogin, FormUsuario, FormEmpleado
from models import usuario, empleado
from utils import isPasswordValid


app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

#decorador para verificar que el usuario que accede se ha autenticado
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        
        if g.user is None:
            return redirect( url_for('login'))
        
        return view(**kwargs)
    
    return wrapped_view

#Hace que se ejecute la verificación de usuario autenticado antes de que se ejecuten las funciones controladoras
@app.before_request
def cargar_usuario_autenticado():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = usuario.cargar(user_id)


@app.route('/', methods=["GET", "POST"])
def login():
    mensaje = ""

    if request.method == "GET":
        formulario = FormLogin()
        return render_template('index.html', titulo='Iniciar Sesión', form=formulario)
    else:
        formulario = FormLogin(request.form)
        if formulario.validate_on_submit():
            obj_usuario = usuario(0,0,formulario.usuario.data,formulario.password.data,0,'','','')

            if not obj_usuario.usuario.__contains__("'") and not obj_usuario.password.__contains__("'"):
                dic_usuario = usuario.verificar(obj_usuario)
                if dic_usuario != None:
                    session.clear()
                    session['user_id'] = dic_usuario[0]["usuario"]
                    return redirect(url_for('menu'))
                    
        return render_template('index.html',form=formulario, mensaje='Usuario o contraseña NO válidos.')


@app.route('/logout/')
@login_required
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/registro/', methods=('GET', 'POST'))
def registro():
    mensaje = ""
    if request.method == "GET": 
        formulario = FormRegistro()
        return render_template('registro.html', form = formulario)
    else:
        formulario = FormRegistro(request.form)
        if formulario.validate_on_submit():
            obj_usuario = usuario(0, 0, formulario.usuario.data, formulario.password.data, 0, '', '', '')

            dic_usuario = usuario.verificar_reg(obj_usuario)
            if dic_usuario == None:
                mensaje += "El usuario no es válido o ya fue registrado"

            if not isPasswordValid(obj_usuario.password):
                mensaje += "El password no cumple con los requisitos mínimos. "
                  
            if (formulario.password.data != formulario.repassword.data):
                mensaje += "Las contraseñas no coinciden."   
        else:
            mensaje += "Todos los datos son requeridos."
        
        if not mensaje:  
            dic_usuario[0]["password"] =  obj_usuario.password
            if usuario.registrar_usuario(dic_usuario[0]):
                print = "Su cuenta ha sido registrada, puede iniciar sesión."
                return redirect('/')
            else:
                mensaje += "Ocurrió un error durante el registro, por favor intente nuevamente."

        return render_template('registro.html',form=formulario, mensaje = mensaje)


@app.route("/menu/")
@login_required
def menu():
    return redirect('/admin_empleados/crear_empleado')


@app.route("/admin_usuarios/crear_usuario/", methods=["GET", "POST"])
@login_required
def crear_u():
    mensaje = ""
    if request.method == "GET": 
        formulario = FormUsuario()
        return render_template('crear_usuario.html', form = formulario)
    else:
        formulario = FormUsuario(request.form)
        if formulario.validate_on_submit():
            #-con la identificación debo consultar el id del empleado para verificar que exista y no tenga ya usuario asociado y luego instanciar un objeto usuario
            obj_usuario = usuario(p_id=0, p_id_empleado = formulario.identificacion.data, p_usuario=formulario.usuario.data,
            p_password = None, p_id_rol = formulario.rol.data, p_estado='A', p_creado_por = 'admin', p_creado_en = '2021-10-25')

            #- validar antes de la inserción que no haya ya un registro creado con ese mismo usuario
            if obj_usuario.insertar():
                return render_template("crear_usuario.html", form=FormUsuario(), mensaje= "El usuario ha sido creado.")
            else:
                return render_template("crear_usuario.html", form=formulario, mensaje= "No fue posible crear el usuario, consulte a soporte técnico.")

        return render_template("crear_usuario.html", form=formulario, mensaje = "Todos los datos son requeridos.")


@app.route("/admin_usuarios/editar_usuario/", methods=["GET", "POST"])
@login_required
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

            #-Debo validar antes de la inserción que no haya ya un registro creado con ese mismo usuario
            if obj_usuario.editar():
                return render_template("crear_usuario.html", form=FormUsuario(), mensaje= "El usuario ha sido editado.")
            else:
                return render_template("crear_usuario.html", form=formulario, mensaje= "No fue posible editar el usuario, consulte a soporte técnico.")

        return render_template("crear_usuario.html", form=formulario, mensaje = "Todos los datos son requeridos.")


@app.route("/admin_usuarios/consultar_usuario/",methods=["GET"])
@login_required
def get_listado_usuarios_json():
    return jsonify(usuario.listado())

@app.route("/admin_usuarios/consultar_usuario/ver/<id>")
@login_required
def get_usuario_json(id):
    obj_usuario = usuario.cargar(id)
    if obj_usuario:
        return obj_usuario
    return jsonify({"error":"No existe un usuario con el id especificado." })


@app.route("/admin_empleados/consultar_empleado/",methods=["GET"])
@login_required
def get_listado_empleados_json():
    return jsonify(empleado.listado())

@app.route("/admin_empleados/consultar_empleado/ver/<id>")
@login_required
def get_empleado_json(id):
    obj_empleado = empleado.cargar(id)
    if obj_empleado:
        return obj_empleado
    return jsonify({"error":"No existe un empleado con el id especificado." })


@app.route("/admin_empleados/crear_empleado/", methods=["GET", "POST"])
@login_required
def crear_empleado():
    mensaje = ""

    if request.method == "GET": 
        formulario = FormEmpleado()

        dependencias=()
        dependencias = ejecutar_select("SELECT id, descripcion FROM dependencias")
        cargos=()
        cargos = ejecutar_select("SELECT id, descripcion FROM cargos")
        contratos=()
        contratos = ejecutar_select("SELECT id, descripcion FROM tipos_contrato")
        jefes=()
        jefes = ejecutar_select("SELECT id, nombre FROM empleados WHERE es_jefe = True AND estado = 'A' ")

        ld=[]
        for i in dependencias:
            ld.append((i["id"],i["descripcion"]))

        lc=[]
        for i in cargos:
            lc.append((i["id"],i["descripcion"]))

        lt=[]
        for i in contratos:
            lt.append((i["id"],i["descripcion"]))

        lj=[]
        for i in jefes:
            lj.append((i["id"],i["nombre"]))

        formulario.idDependencia.choices = ld
        formulario.idCargo.choices = lc
        formulario.idTipoContrato.choices = lt
        formulario.idJefe.choices = lj
        
        return render_template('crear_empleado.html', form = formulario, dependencias=dependencias, cargos=cargos, contratos= contratos)
    else:
        formulario = FormEmpleado(request.form)
        if formulario.validate_on_submit():
            #if not isEmailValid(FormEmpleado.correo.data):
                #mensaje += "El email es inválido. "

            today = datetime.today()
            obj_empleado = empleado(p_id=0, p_tipo_identificacion = formulario.tipoIdentificacion.data, 
            p_numero_identificacion = formulario.identificacion.data, p_nombre = formulario.nombre.data,
            p_id_correo = formulario.idcorreo, p_id_tipo_contrato = formulario.idTipoContrato, p_fecha_ingreso = formulario.fechaIngreso.data,
            p_fecha_fin_contrato = formulario.fechaFin.data, p_id_dependencia = formulario.idDependencia.data,
            p_id_cargo = formulario.idCargo.data, p_salario = formulario.salario.data, p_id_jefe = formulario.idJefe.data, 
            p_es_jefe = formulario.esJefe.data, p_estado='A', p_creado_por = 'admin', p_creado_en = today)

            dic_empleado = empleado.verificar(obj_empleado)
            if dic_empleado != None:
                return render_template("crear_empleado.html", form=formulario, mensaje = "La identificación ya está asociada a otro empleado.")

            if obj_empleado.insertar(obj_empleado):
                return render_template("crear_empleado.html", form=FormEmpleado(), mensaje= "El empleado ha sido creado.")
            else:
                return render_template("crear_empleado.html", form=formulario, mensaje= "No fue posible crear el empleado, consulte a soporte técnico.")

        return render_template("crear_empleado.html", form=formulario, mensaje = "Todos los datos son requeridos.")


@app.route("/admin_empleados/editar_empleado/", methods=["GET", "POST"])
@login_required
def editar_e():
    if request.method == "GET": 
        formulario = FormEmpleado()

        dependencias=()
        dependencias = ejecutar_select("SELECT id, descripcion FROM dependencias")
        print(dependencias)
        cargos=()
        cargos = ejecutar_select("SELECT id, descripcion FROM cargos")
        print(cargos)
        contratos=()
        contratos = ejecutar_select("SELECT id, descripcion FROM tipos_contrato")
        print(contratos)

        ld=[]
        for i in dependencias:
            ld.append((i["id"],i["descripcion"]))

        lc=[]
        for i in cargos:
            lc.append((i["id"],i["descripcion"]))

        lt=[]
        for i in contratos:
            lt.append((i["id"],i["descripcion"]))

        formulario.idDependencia.choices = ld
        print(ld)
        formulario.idCargo.choices = lc
        print(lc)
        formulario.idTipoContrato.choices = lt
        print(lt)

        return render_template('crear_empleado.html', form = formulario, dependencias=dependencias, cargos=cargos, contratos= contratos)
    else:
        formulario = FormEmpleado(request.form)
        if formulario.validate_on_submit():
            #if not isEmailValid(FormEmpleado.correo.data):
                #mensaje += "El email es inválido. "

            obj_empleado = empleado(p_id=0, p_tipo_identificacion = formulario.tipoIdentificacion.data, 
            p_numero_identificacion = formulario.identificacion.data, p_nombre = formulario.nombre.data,
            p_id_tipo_contrato = formulario.idTipoContrato, p_fecha_ingreso = formulario.fechaIngreso.data,
            p_fecha_fin_contrato = formulario.fechaFin.data, p_id_dependencia = formulario.idDependencia.data,
            p_id_cargo = formulario.idCargo.data, p_salario = formulario.salario.data, p_id_jefe = formulario.idJefe.data, 
            p_es_jefe = formulario.esJefe.data, p_estado='A', p_creado_por = 'admin', p_creado_en = '2021-10-25')

            if obj_empleado.insertar(obj_empleado):
                return render_template("crear_empleado.html", form=FormEmpleado(), mensaje= "El empleado ha sido creado.")
            else:
                return render_template("crear_empleado.html", form=formulario, mensaje= "No fue posible crear el empleado, consulte a soporte técnico.")

        return render_template("crear_empleado.html", form=formulario, mensaje = "Todos los datos son requeridos.")


@app.route("/admin_empleados/consultar_empleado/")
@login_required
def consultar_e():
    return render_template('consultar_empleado.html')

@app.route("/evaluacion/")
@login_required
def evaluacion():
    return render_template('evaluacion.html')

@app.route("/evaluacion/empleado_evaluar/")
@login_required
def empleado_evaluar():
    return render_template('empleado_evaluar.html')
