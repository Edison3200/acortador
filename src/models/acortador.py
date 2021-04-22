from src.config.db import DB


class AcortadorUrl():
    
    def insertar(self, url_original, url_corta,id_usu):
        cursor = DB.cursor()

        cursor.execute('insert into url(url_original, url_corta ,id_usu) values(?,?,?)', (url_original, url_corta,id_usu,))
        
        cursor.close()

    def insert_public(self, url_original, url_corta):
        cursor = DB.cursor()

        cursor.execute('insert into url(url_original, url_corta ,id_usu) values(?,?,?)', (url_original, url_corta,None,))
        
        cursor.close()
    def llamar_link(self,id_acortado):
        cursor = DB.cursor()
        cursor.execute(""" select * from url
        where id = ? """,(id_acortado,))
        url= cursor.fetchone()
        return url
    def actualizar_link(self,id_acortado,id_usu,url_original):
        cursor = DB.cursor()
        cursor.execute(""" update url set url_original = ? where id_usu = ? and id = ? """,(url_original,id_usu,id_acortado,))
        DB.commit()
        cursor.close()
    def eliminar_link(self,id_acortado,id_usu):
        cursor = DB.cursor()
        cursor.execute(""" Delete FROM url Where id = ? and id_usu = ? """, (id_acortado,id_usu))
        DB.commit()
        cursor.close()

  