import db 

class usuario():
    id=0
    login=''
    contrasena=''
    id_rol=0
    estado=''

    def __init__(self, p_id, p_login, p_contrasena, p_id_rol, p_estado='A'):
        self.id = p_id
        self.login = p_login
        self.contrasena = p_contrasena
        self.id_rol = p_id_rol
        self.estado = p_estado
    
    @classmethod
    def cargar(cls, p_id):
        sql = "SELECT * FROM usuarios WHERE id = ?;"
        obj = db.ejecutar_select(sql, [ p_id ])
        if obj:
            if len(obj)>0:
                return cls(obj[0]["id"], obj[0]["login"], obj[0]["contrasena"], obj[0]["id_rol"], obj[0]["estado"])

        return None


    def insertar(self):
        sql = "INSERT INTO usuarios (login, id_rol, estado) VALUES (?,?,?);"
        afectadas = db.ejecutar_insert(sql, [ self.login, self.id_rol, 'A' ])
        return (afectadas > 0)


    def eliminar(self):
        sql = "UPDATE usuarios SET estado = 'N' WHERE id = ?;"
        afectadas = db.ejecutar_insert(sql, [ self.id ])
        return (afectadas > 0)


    @staticmethod
    def listado():
        sql = "SELECT * FROM usuarios ORDER BY id;"
        return db.ejecutar_select(sql, None)