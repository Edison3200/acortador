from flask import render_template, request, redirect, url_for, flash, session,Flask
from src import app
import random, datetime ,os
from random import choice
from src.models.acortador import AcortadorUrl
from src.models.usuario import RegistroUsu
from src.config.token import generate_confirmation_token, confirm_token
from flask_mail import Mail, Message
import sqlite3

db = sqlite3.connect('data.db', check_same_thread=False)

app.secret_key ='spbYO0JJ0PUFLUikKYbKrpS5w3KUEnab5KcYDdYb'
app.config['SECURITY_PASSWORD_SALT']= 'my_precious_two'
app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'Tucorreo' #ingresa tu correo electronico, para que sirva como servidor
app.config['MAIL_PASSWORD'] = 'Tucontraseña'#tu contraseña
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'Tucorreo' #ingresa tu correo electronico, para que sirva como servidor
app.config['MAIL_ASCII_ATTACHMENTS'] =False
mail = Mail(app)

@app.route('/', methods =['GET','POST'])
def index():
   
   if request.method == 'GET':
      if 'usuario' in session:
            direcciones = RegistroUsu()
            direcciones = direcciones.Listado(session['usuario'][0])
            return render_template('index.html',direcciones=direcciones)
      
      return render_template('index.html')
   if request.method == 'POST':
      url_original = request.form.get('acortar')
      #Url local
      url_local = "http://127.0.0.1:5000/"
      
      #cantidad de caracateres que tomara en el recorrido del for
      longitud = 4
      
      #caracteres a seleccionar aleaotorios
      caracter = "abcdefghijklmñopqrstuvwxyz1234567890"
      
      #4 caracteres aleatorios
      url_corta = url_local + ''.join(random.choice(caracter) for i in range(longitud))

      #concat url local y url corta
      #url_final = url_local + url_corta
      acortadorUrl = AcortadorUrl()
      if 'usuario' in session:
            
            acortadorUrl.insertar(url_original, url_corta,session['usuario'][0])

            direcciones = RegistroUsu()
            direcciones = direcciones.Listado(session['usuario'][0])
            #me redirecciona a la misma pagina pero esta vez con la url cargada en la vista
            return render_template('index.html', url_corta = url_corta,direcciones=direcciones)
      else:
            acortadorUrl.insert_public(url_original,url_corta)
      return render_template('index.html',url_corta = url_corta)

@app.route('/<link>',methods =['GET','POST']) # linkNombre
def enviar(link):
    
   if 'usuario' in session:
         usuario = session['usuario'][0]
         url_local = "http://127.0.0.1:5000/" + link
         mi_url = RegistroUsu()
         mi_url = mi_url.Reenviar(url_local, usuario)
         
         if mi_url is None  :
            mi_url = RegistroUsu()
            mi_url = mi_url.Reenviar_public(url_local)
            if mi_url is None:
                return redirect(url_for('index'))
         return redirect(mi_url[0])
   else:
        url_local = "http://127.0.0.1:5000/"+link
        mi_url = RegistroUsu()
        mi_url = mi_url.Reenviar_public(url_local)

        if mi_url is None :
            return redirect(url_for('index'))
        return redirect(mi_url[0])

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    email = request.form.get('email')
    password = request.form.get('password')

    onLogin = RegistroUsu()
    onLogin = onLogin.Onlogin(email, password)
    if onLogin is None:
        flash('datos incorrectos','badge bg-danger')
        return redirect(url_for('login'))
    session['usuario'] = onLogin 
    return redirect(url_for('index'))

@app.route('/logout',methods=['GET','POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/login/usuario', methods=['GET', 'POST'])
def usuario_crear():
    if request.method == 'GET':
        return render_template('crear.html')

    if request.method == 'POST':
         nombres = request.form.get('nombres')
         email = request.form.get('email')
         password = request.form.get('password')

         new_usu = RegistroUsu()
         new_usu.insertarUsu(nombres, email, password)

         token = generate_confirmation_token(email)  
         confirm_url = url_for('confirm_email', token=token, _external=True)
         html = render_template('activacion.html', confirm_url=confirm_url)
         subject = "Por favor confirma tu Correo electronico"
 
         msg = Message(subject,
                        sender=app.config.get("MAIL_DEFAULT_SENDER"),
                        recipients=[email],
                        html=html)
         mail.send(msg)
         
         flash("Un correo ha sido enviado, para la verificacion de usuario","badge bg-success")
    return redirect(url_for('login'))

@app.route('/login/confirm/<token>', methods=['GET', 'POST'])
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        RegistroUsu().EliminarCuenta(email)
        flash('La confirmacion del link es invalida, ha expirado', 'danger')
        return redirect(url_for('index'))
    
    confirm = RegistroUsu()
    confirm.ConfirmCuenta(email)

    flash('Has confirmado tu cuenta, Puedes Iniciar sesion!', 'success')
    return redirect(url_for('login'))


#Formulario para actualizar
@app.route('/direcciones/actualizar',methods=['GET','POST',])
def actualizar_direcciones():
    if not 'usuario' in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        return redirect(url_for('index'))

    id = request.form.get('id') # Id de url acortada

    direccion = AcortadorUrl()
    direccion = direccion.llamar_link(id)   
    return render_template('actualizar.html',direccion =direccion)

#Actualizar formulario
@app.route('/direcciones/actualizado', methods=['GET', 'POST'])
def solicitud_direcciones():
    if not 'usuario' in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        return redirect(url_for('index'))
    if request.method == 'POST':
        identificador= request.form.get('identificador')# id de url acortada
        url_original = request.form.get('original')
        usuario = session['usuario'][0]
        print(identificador,url_original,usuario)
        direccion = AcortadorUrl()
        direccion = direccion.actualizar_link(identificador,usuario,url_original)
        flash("La direccion principal fue actualizada!!..","info")
    return redirect(url_for('index'))

#Eliminar direcciones
@app.route('/direcciones/delete', methods=['GET','POST',])
def delete_direccion():
    if not 'usuario' in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        return redirect(url_for('index'))

    if request.method == 'POST':
        id = request.form.get('id')
        usuario = session['usuario'][0]
        direccion = AcortadorUrl()
        direccion = direccion.eliminar_link(id,usuario)
        flash("La direccion fue eliminada!..","warning")
    return redirect(url_for('index'))
