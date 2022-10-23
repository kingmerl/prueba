from traceback import format_exception
from werkzeug.security import check_password_hash
from flask_login import UserMixin
class User(UserMixin ):

    def __init__(self, id, nombre, usuario, rol, direccion, email, contrasena, estado, fecha_ingreso) -> None:
        self.id = id
        self.nombre = nombre
        self.usuario = usuario
        self.rol = rol
        self.direccion = direccion
        self.email = email
        self.contrasena = contrasena
        self.estado = estado
        self.fecha_ingreso = fecha_ingreso
    @classmethod
    def check_password(self,hashed_password, password):
        return check_password_hash(hashed_password,password)

