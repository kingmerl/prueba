from .entities.User import User
class ModelUser():

    @classmethod
    def login(self, db, user):
        try:
            cursor=db.connection.cursor()
            sql= """SELECT id, nombre, usuario, roll, direccion, email, contrasena, estado, fecha_ingreso FROM usuario 
                        WHERE usuario = '{}' """.format(user.usuario)
            cursor.execute(sql)
            row=cursor.fetchone()
            if row != None:
                user=User(row[0], row[1], row[2], row[3], row[4], row[5], User.check_password(row[6], user.contrasena), row[7], row[8])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor=db.connection.cursor()
            sql= "SELECT  id, nombre, usuario, roll, direccion, email, estado, fecha_ingreso FROM usuario WHERE id = {}".format(id)
            cursor.execute(sql)
            row=cursor.fetchone()
            if row != None:
                return User(row[0], row[1], row[2], row[3], row[4], row[5], None, row[6], row[7])
                
            else:
                return None
        except Exception as ex:
            raise Exception(ex)