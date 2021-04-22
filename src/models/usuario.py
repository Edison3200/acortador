from src.config.db import DB
from datetime import datetime, date, time, timedelta

class RegistroUsu():
    def insertarUsu(self,nombres,email,password):
        cursor = DB.cursor()
        cursor.execute("""insert into usuarios(
                nombres,
                email,
                password
            )values (?,?,?)
        """, (nombres, email, password))
        DB.commit()
        cursor.close()

    def Onlogin(self,email,password):
        cursor = DB.cursor()
        cursor.execute(""" select * from usuarios 
        where email = ? and password = ?  and verificado = 1""",(email,password))
        usuario = cursor.fetchone()
     
        return usuario

    def Reenviar(self,url_corta,id_usu):
        cursor = DB.cursor()
        cursor.execute(""" select url_original from url
        where url_corta = ? and id_usu = ? """,(url_corta,id_usu))
        url= cursor.fetchone()
       
        return url

    def Reenviar_public(self,url_corta):
        cursor = DB.cursor()
        cursor.execute(""" select url_original from url
        where url_corta = ? and id_usu is NULL """,(url_corta,))
        url= cursor.fetchone()
      
        return url
    
    def Listado(self,id_usu):
        cursor = DB.cursor()
        sql = """select * from url where id_usu = ?"""
        cursor.execute(sql,(id_usu,))
        direcciones = cursor.fetchall()
        return direcciones
    def EliminarCuenta(self,email):
        cursor = DB.cursor()
        cursor.execute(""" Delete FROM usuarios Where email = ? """, (email,))
        DB.commit()
        cursor.close()

    def ConfirmCuenta(self,email):
        ahora = datetime.now() 
        cursor = DB.cursor()
        cursor.execute(""" update usuarios set verificado = 1,fecha_ver = ? where email = ? """,(ahora,email,))
        DB.commit()
        cursor.close()

