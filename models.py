import db 

class usuario():
    id = 0
    id_empleado = 0
    login = ''
    password = ''
    id_rol = 0
    estado = 0
    creado_por = ''
    creado_en = ''

    def __init__(self, p_id, p_id_empleado, p_login, p_password, p_id_rol, p_estado='A', p_creado_por='', p_creado_en=''):
        self.id = p_id
        self.id_empleado = p_id_empleado
        self.login = p_login
        self.password = p_password
        self.id_rol = p_id_rol
        self.estado = p_estado
        self.creado_por = p_creado_por
        self.creado_en = p_creado_en
    
    @classmethod
    def cargar(cls, p_id):
        sql = "SELECT * FROM usuarios WHERE id = ?;"
        obj = db.ejecutar_select(sql, [ p_id ])
        if obj:
            if len(obj)>0:
                return cls(obj[0]["id"], obj[0]["id_empleado"], obj[0]["login"], obj[0]["password"], obj[0]["id_rol"], obj[0]["estado"], obj[0]["creado_por"], obj[0]["creado_en"])

        return None


    def insertar(self):
        sql = "INSERT INTO usuarios (id_empleado, login, id_rol, estado, creado_por, creado_en) VALUES (?,?,?,?,?,?);"
        afectadas = db.ejecutar_insert(sql, [ self.id_empleado, self.login, self.id_rol, 'A', self.creado_por, self.creado_en ])
        return (afectadas > 0)


    def eliminar(self):
        sql = "UPDATE usuarios SET estado = 'N' WHERE id = ?;"
        afectadas = db.ejecutar_insert(sql, [ self.id ])
        return (afectadas > 0)


    def editar(self):
        sql = "UPDATE usuarios SET id_rol = ? WHERE id = ?;"
        afectadas = db.ejecutar_insert(sql, [ self.id_rol, self.id ])
        return (afectadas > 0)

    @staticmethod
    def listado():
        sql = "SELECT * FROM usuarios ORDER BY id;"
        return db.ejecutar_select(sql, None)

    
class empleado():
    id = 0
    tipo_identificacion = ''
    numero_identificacion = ''
    nombre = ''
    correo = ''
    fecha_ingreso = ''
    fecha_fin_contrato = ''
    id_dependencia = 0
    id_cargo = 0
    salario = 0
    id_jefe = 0
    es_jefe = ''
    estado = ''
    creado_por = ''
    creado_en = ''

    def __init__(self, p_id, p_tipo_identificacion, p_numero_identificacion, p_nombre,
        p_id_tipo_contrato, p_fecha_ingreso, p_fecha_fin_contrato, p_id_dependencia,
        p_id_cargo, p_salario, p_id_jefe, p_es_jefe = False, p_estado='A', 
        p_creado_por = 'admin', p_creado_en = '2021-10-25'):
        
        self.id = p_id
        self.tipo_identificacion = p_tipo_identificacion
        self.numero_identificacion = p_numero_identificacion
        self.nombre = p_nombre
        self.id_tipo_contrato = p_id_tipo_contrato
        self.fecha_ingreso = p_fecha_ingreso
        self.fecha_fin_contrato = p_fecha_fin_contrato
        self.id_dependencia = p_id_dependencia
        self.id_cargo = p_id_cargo
        self.salario = p_salario
        self.id_jefe = p_id_jefe
        self.es_jefe = p_es_jefe
        self.p_estado = p_estado
        self.creado_por = p_creado_por
        self.creado_en = p_creado_en

    
    @classmethod
    def cargar(cls, p_id):
        sql = "SELECT * FROM empleados WHERE id = ?;"
        obj = db.ejecutar_select(sql, [ p_id ])
        if obj:
            if len(obj)>0:
                return cls(obj[0]["id"], obj[0]["tipo_identificacion"],obj[0]["numero_identificacion"],
                obj[0]["nombre"],obj[0]["correo"],obj[0]["fecha_ingreso"],obj[0]["fecha_fin_contrato"],
                obj[0]["id_dependencia"],obj[0]["id_cargo"],obj[0]["salario"],obj[0]["id_jefe"],
                obj[0]["es_jefe"],obj[0]["estado"],obj[0]["creado_por"], obj[0]["creado_en"])

        return None        


    def insertar(self):
        sql = "INSERT INTO empleados (tipo_identificacion,numero_identificacion,nombre,correo,fecha_ingreso,fecha_fin_contrato,id_dependencia,id_cargo,salario,id_jefe,es_jefe,estado,creado_por,creado_en) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
            
        afectadas = db.ejecutar_insert(sql, [ self.tipo_identificacion, self.numero_identificacion, self.nombre, self.correo, self.fecha_ingreso, self.fecha_fin_contrato, self.id_dependencia, self.id_cargo, self.salario, self.id_jefe, self.es_jefe, 'A', self.creado_por, self.creado_en ])
        return (afectadas > 0)


    def eliminar(self):
        sql = "UPDATE empleados SET estado = 'N' WHERE id = ?;"
        afectadas = db.ejecutar_insert(sql, [ self.id ])
        return (afectadas > 0)


    def editar(self):
        sql = "UPDATE empleados SET (correo, fecha_fin_contrato, id_dependencia, id_cargo, salario, id_jefe, es_jefe) = (?,?,?,?,?,?,?) WHERE id = ?;"
        afectadas = db.ejecutar_insert(sql, [ self.correo, self.fecha_fin_contrato, self.id_dependencia, 
                    self.id_cargo, self.salario, self.id_jefe, self.es_jefe, self.id ])
        return (afectadas > 0)

    @staticmethod
    def listado():
        sql = "SELECT * FROM empleados ORDER BY id;"
        return db.ejecutar_select(sql, None)
