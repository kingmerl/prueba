
#from json import dumps
#from lib2to3.pgen2 import token
#import re
from array import array
from lib2to3.pgen2 import token
from werkzeug.security import generate_password_hash
from flask import Flask, render_template, json, request, redirect, url_for, flash, session, jsonify
import psycopg2 #pip install psycopg2 
import psycopg2.extras
import webbrowser
from flask_mysqldb import MySQL, MySQLdb
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required

from config import config
from datetime import date

# modelos
from models.ModelUser import ModelUser

#entities
from models.entities.User import User
app = Flask(__name__)
csrf=CSRFProtect()
db=MySQL(app)

login_manager_app=LoginManager(app)
@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db,id)
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        print(request.form['username'])
        print(request.form['password'])
        user = User(0,0,request.form['username'],0,0,0,request.form['password'],0,0)
        logged_user=ModelUser.login(db,user)
        if logged_user != None:
            if logged_user.contrasena:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash("contraseña no valida")
                return render_template('auth/login.html')
        else:
            flash("usuario no encotrado")
            return render_template('auth/login.html')   
    else:
        return render_template('auth/login.html')
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
def status_401(error):
    return redirect(url_for('login'))
def status_404(error):
    return "<h1>Pagina no encontrada</h1><h2>contactese con el desarrollador</h2>", 404
@app.route('/producto')
@login_required
def producto():
  
    cur=db.connection.cursor()
    cur.execute('SELECT * FROM marca')
    data = cur.fetchall()
    cur1=db.connection.cursor()
    cur1.execute('SELECT * FROM categoria')
    data1 = cur1.fetchall()
    
    return render_template('producto.html', marcas =data, categorias =data1)

@app.route('/add_producto', methods=['GET','POST'])
def add_producto():
    if request.method == 'POST':
        id_producto = request.form['id_producto']
        nombre = request.form['nombre']
        marca = request.form['marca']
        categoria = request.form['categoria']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        estado = request.form['estado']
        cur = db.connection.cursor()
        cur.execute('INSERT INTO producto (id_producto, nombre, marca, categoria, descripcion, precio, estado) VALUES (%s, %s, %s, %s, %s, %s, %s)',
        (id_producto, nombre, marca, categoria,descripcion, precio, estado),)
        db.connection.commit()
        flash("Producto agregado")
        return redirect(url_for('producto'))


@app.route('/proveedor')
@login_required
def proveedor():
    return render_template('proveedor.html')
    
@app.route('/add_Proveedor', methods=['GET','POST'])
def add_Proveedor():
    if request.method == 'POST':
        
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        lugar = request.form['lugar']
        fecha = request.form['fecha']
        cur = db.connection.cursor()
        cur.execute('INSERT INTO proveedor (id_proveedor, nombre, apellido, direccion, telefono, lugar, fecha) VALUES (%s, %s, %s, %s, %s, %s, %s)',
        (None, nombre, apellido, direccion, telefono, lugar, fecha))
        db.connection.commit()
        flash("Proveedor agregado")
        return redirect(url_for('proveedor'))

@app.route('/add_proveedorcompra', methods=['GET','POST'])
def add_proveedorcompra():
    if request.method == 'POST':
        
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        lugar = request.form['lugar']
        fecha = request.form['fecha']
        cur = db.connection.cursor()
        cur.execute('INSERT INTO proveedor (id_proveedor, nombre, apellido, direccion, telefono, lugar, fecha) VALUES (%s, %s, %s, %s, %s, %s, %s)',
        (None, nombre, apellido, direccion, telefono, lugar, fecha))
        db.connection.commit()
        flash("Proveedor agregado")
        return redirect(url_for('compra'))

@app.route('/cliente')
@login_required
def cliente():
    return render_template('cliente.html')
@app.route('/add_cliente', methods=['GET','POST'])
def add_cliente():
    if request.method == 'POST':
        
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        email = request.form['email']
        descripcion = request.form['descripcion']
        estado = request.form['estado']
        fecha = request.form['fecha']
        cur = db.connection.cursor()
        cur.execute('INSERT INTO cliente (id_cliente, nombre, apellido, direccion, telefono, email, descripcion, estado, fecha) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
        (None, nombre, apellido, direccion, telefono, email, descripcion, estado, fecha),)
        db.connection.commit()
        flash("Cliente agregado")
        
        return redirect(url_for('cliente'))

@app.route('/add_clienteventa', methods=['GET','POST'])
def add_clienteventa():
    if request.method == 'POST':
        
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        email = request.form['email']
        descripcion = request.form['descripcion']
        estado = request.form['estado']
        fecha = request.form['fecha']
        cur = db.connection.cursor()
        cur.execute('INSERT INTO cliente (id_cliente, nombre, apellido, direccion, telefono, email, descripcion, estado, fecha) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
        (None, nombre, apellido, direccion, telefono, email, descripcion, estado, fecha),)
        db.connection.commit()
        flash("Cliente agregado")
        return redirect(url_for('venta'))

@app.route('/usuario')
@login_required
def usuario():
    return render_template('usuario.html')
@app.route('/add_usuario', methods=['GET','POST'])
def add_usuario():
    if request.method == 'POST':
        
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        email = request.form['email']
        usuario = request.form['usuario']
        password1 = request.form['password']
        password = generate_password_hash(password1)
        roll = request.form['roll']
        estado = request.form['estado']
        fecha = request.form['fecha']
        cur = db.connection.cursor()
        cur.execute('INSERT INTO usuario (id, nombre, apellido, usuario, roll, telefono, direccion, email, contrasena, estado, fecha_ingreso) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
        (None, nombre, apellido, usuario, roll, telefono, direccion, email, password, estado, fecha),)
        db.connection.commit()
        flash("Usuario agregado")

        return redirect(url_for('usuario'))

@app.route('/categoria')
@login_required
def categoria():
    return render_template('categoria.html')
@app.route('/add_categoria', methods=['GET','POST'])
def add_categoria():
    if request.method == 'POST':
        nombre = request.form('nombre')
        descripcion = request.form('descripcion')
        cur = db.connection.cursor()
        cur.execute('INSERT INTO categoria (id, nombre, descripcion) VALUES (%s, %s, %s)',
        (None, nombre, descripcion),)
        db.connection.commit()
        flash("Categoria agregada")
        return redirect(url_for('categoria'))

@app.route('/add_categoriajx', methods=['GET','POST'])

def add_categoriajx():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        cur = db.connection.cursor()
        cur.execute('INSERT INTO categoria (id, nombre, descripcion) VALUES (%s, %s, %s)',
        (None, nombre, descripcion),)
        db.connection.commit()
        flash("Categoria agregada")
    return redirect(url_for('producto'))

@app.route('/add_marcajx', methods=['GET','POST'])
def add_marcajx():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        cur = db.connection.cursor()
        cur.execute('INSERT INTO marca (id, nombre, descripcion) VALUES (%s, %s, %s)',
        (None, nombre, descripcion),)
        db.connection.commit()
        flash("Marca agregada")
    return redirect(url_for('producto'))

@app.route('/marca')
@login_required
def marca():
    return render_template('marca.html')
@app.route('/add_marca', methods=['GET','POST'])
def add_marca():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        cur = db.connection.cursor()
        cur.execute('INSERT INTO marca (id, nombre, descripcion) VALUES (%s, %s, %s)',
        (None, nombre, descripcion),)
        db.connection.commit()
        flash("marca agregada")
        return redirect(url_for('marca'))

@app.route('/configuracion/<id>')
@login_required
def configuracion(id):
    cur = db.connection.cursor()
    cur.execute('SELECT * FROM usuario WHERE id =%s', [id])
    data = cur.fetchall()
    print (data[0])
    return render_template('configuracion.html', dato = data[0])

@app.route('/mi_usuario/<id>', methods = ['POST'])
def mi_usuario(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        usuario = request.form['usuario']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        email = request.form['email']
        password1 = request.form['password']
        password = generate_password_hash(password1)
        cur = db.connection.cursor()
        cur.execute("""
        UPDATE usuario
        SET nombre = %s,
            apellido = %s,
            usuario = %s,
            telefono = %s,
            direccion = %s,
            email = %s,
            contrasena = %s
        WHERE id = %s
        """, (nombre, apellido, usuario,  telefono, direccion, email, password, [id]))
        db.connection.commit()
        return redirect(url_for('home'))

#*/*/*/*/*/**//**/*/*/*/*/*/*/**/*/*/*/*/*/*/*/**/*/*/*/**/*/*/*/*
@app.route('/venta')
@login_required
def venta():
    return render_template('venta.html')



@csrf.exempt
@app.route("/sacar_cliente",methods=["POST","GET"])
def sacar_cliente():
    #cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        codcliente = request.form['cliente']
        cur=db.connection.cursor()
        #cur.execute('SELECT * FROM cliente WHERE id_cliente LIKE %(id_cliente)s', { 'id_cliente': '%{}%'.format(codcliente)})
        cur.execute('SELECT * FROM cliente WHERE id_cliente =%s', [codcliente])
        row_headers=[x[0] for x in cur.description] #this will extract row headers
        rv = cur.fetchall()
        numrows = int(cur.rowcount)
        
        #print(numrows)
        data=''
        json_data=[]
        for result in rv:
            json_data.append(dict(zip(row_headers,result)))
        #print(rv)

        if numrows == 0:
            return json.dumps(data)
        else:
            data=json_data
            return json.dumps(data[0])

       # numrows = int(cur.rowcount)
       # dato = cur.fetchall()
        
        #print(numrows)
       # clnt = []
        #contenido = {}
        #for resultado in dato:
        #    contenido = {'id_cliente': resultado["id_cliente"],'nombre': resultado["nombre"],'apellido': resultado["apellido"],'direccion': resultado['direccion'],'telefono': resultado['telefono'],'email': resultado['email'],'descripcion': resultado['descripcion'],'estado': resultado['estado'],'fecha': resultado['fecha']}
        #    clnt.append(contenido)

        #print(contenido)
       # return jsonify("[{'id_cliente': 220001, 'nombre': 'walter', 'apellido': 'pepito', 'direccion': 'ciudad', 'telefono': '15141819', 'email': 'lkjlhjkj@asdfg.com', 'descripcion': 'qwerty qwerty', 'estado': 'Activo', 'fecha': '17/17/2022'}]")


@csrf.exempt
@app.route("/sacar_producto",methods=["POST","GET"])
def sacar_producto():
    #cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        codproducto = request.form['producto']
        cur=db.connection.cursor()
        #cur.execute('SELECT * FROM cliente WHERE id_cliente LIKE %(id_cliente)s', { 'id_cliente': '%{}%'.format(codcliente)})
        cur.execute('SELECT id_producto, nombre, precio, stock FROM producto WHERE id_producto =%s', [codproducto])
        row_headers=[x[0] for x in cur.description] #this will extract row headers
        rv = cur.fetchall()
        numrows = int(cur.rowcount)
        #var1 = [i[3] for i in rv]
        #print (var1)
        #print (rv)
        #print(numrows)
        data=0
        json_data=[]
        for result in rv:
            json_data.append(dict(zip(row_headers,result)))
        #print(rv)

        if numrows == 0:
            return json.dumps(data)
        else:
            data=json_data
            #print(data)
        return json.dumps(data[0])

@csrf.exempt
@app.route("/detallejx",methods=["POST","GET"])
def detallejx():
    if request.method == 'POST':
        codproducto = request.form['codproducto']
        cantidad = request.form['cantidad']
        idp = codproducto
        token = request.form['token']
        cur1=db.connection.cursor()
        cur1.execute('SELECT precio FROM producto WHERE id_producto =%s', [idp])
        data1 = cur1.fetchone()
        #print (data1)
        cur2 = db.connection.cursor()
        #token = 'IjEzMjAyMzllYjljZTM0MjJlNTRiNzFlOWY1MjZkMDNkNmZmZTdlNmUi.Y0eg5A.NAyZEsSEkO0Iyrb8rOVWtzoLB3Q'
        cur2.execute('INSERT INTO detalleventa_temp (token_user,id_producto,cantidad,precio_venta) VALUES (%s, %s, %s, %s)',
        (token, codproducto, cantidad,data1[0]),)
        db.connection.commit()
        cur=db.connection.cursor(MySQLdb.cursors.DictCursor)
        #bb = cur.callproc('addtemp', [codproducto,cantidad,token,'10'])
        cur.execute('CALL add_detalle_temp (%s, %s, %s)',[codproducto,cantidad,token])
        
        #print(codproducto)
        #print(cantidad)
        #print(token)
        rv = cur.fetchall()
        numrows = int(cur.rowcount)
        detalletabla = ''''''
        detalletabla1=''
        sub_total = 0
        total = 0
        array = {}
        json_data = []
        #print(rv)
        #recorrido por 
        for row in rv:
            precio_total = row['cantidad']*row['precio_venta']
            sub_total = sub_total + precio_total
            total = total + precio_total
            
            detalletabla ='''<tr>
                                <td>%s</td>
                                <td colspan="2">%s</td>
                                <td class="textcenter">%s</td>
                                <td class="textright">%s</td>
                                <td class="textright">%s</td>
                                <td class="">
                                    <a class="link_delete" href="#" onclick="event.preventDefault();
                                    del_producto_detalle(%s);"><i class=" far fa-trash-alt"></i></a>
                                </td>
                            </tr>'''%(row['id_producto'],row['nombre'],row['cantidad'],row['precio_venta'],precio_total,row['id_ventatemp'])
           # print (detalletabla)
            detalletabla1 = detalletabla1+detalletabla

            

        detalletotales = '''<tr>
                                <td colspan="6" class="textright"> TOTAL</td>
                                <td class="textright">%s</td>
                            </tr>
        '''%(sub_total)

        #array.append('detalle'(detalletabla1).__dict__)
        #array.append('totales'(detalletotales).__dict__)

        array ['detalle']=detalletabla1
        array ['totales']=detalletotales#json_data.append(dict(zip(row_headers,result)))
        row_headers = [x[0] for x in array]
        

        #for result in array:
          #  json_data.append(dict(zip(rv,result)))
        #pr1 = json.dumps(array)
        #print(json_data)

        #print (array)
        
        return json.dumps(array)
    else:
        return json.dumps('error')
    
    #print(array)   
    
#-------------------------
@csrf.exempt
@app.route("/buscarpordetalle",methods=["POST","GET"])
def buscarpordetalle():
    if request.method == 'POST':
        #user = 'IjEzMjAyMzllYjljZTM0MjJlNTRiNzFlOWY1MjZkMDNkNmZmZTdlNmUi.Y0eg5A.NAyZEsSEkO0Iyrb8rOVWtzoLB3Q'
        user = request.form['user']
        cur=db.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('''SELECT   tmp.id_ventatemp, 
                                tmp.token_user,
                                tmp.cantidad,
                                tmp.precio_venta,
                                p.id_producto,
                                p.nombre
                            FROM detalleventa_temp tmp
                            INNER JOIN producto p
                            ON tmp.id_producto = p.id_producto
                            WHERE token_user = %s
        
        ''', [user])
        
        rv = cur.fetchall()
        
        numrows = int(cur.rowcount)
        detalletabla = ''''''
        detalletabla1=''
        sub_total = 0
        total = 0
        array = {}
        json_data = []
        #print(rv)
        #recorrido por 
        for row in rv:
            
            cant = row['cantidad']
            precio_total = row['cantidad']*row['precio_venta']
            sub_total = sub_total + precio_total
            total = total + precio_total
            
            detalletabla ='''<tr>
                                <td>%s</td>
                                <td colspan="2">%s</td>
                                <td class="textcenter">%s</td>
                                <td class="textright">%s</td>
                                <td class="textright">%s</td>
                                <td class="">
                                    <a class="link_delete" href="#" onclick="event.preventDefault();
                                    del_producto_detalle(%s);"><i class=" far fa-trash-alt"></i></a>
                                </td>
                            </tr>'''%(row['id_producto'],row['nombre'],row['cantidad'],row['precio_venta'],precio_total,row['id_ventatemp'])
           # print (detalletabla)
            detalletabla1 = detalletabla1+detalletabla

            

        detalletotales = '''<tr>
                                <td colspan="6" class="textright"> TOTAL</td>
                                <td class="textright">%s</td>
                            </tr>
        '''%(sub_total)

        #array.append('detalle'(detalletabla1).__dict__)
        #array.append('totales'(detalletotales).__dict__)

        array ['detalle']=detalletabla1
        array ['totales']=detalletotales#json_data.append(dict(zip(row_headers,result)))
        row_headers = [x[0] for x in array]
        

        #for result in array:
          #  json_data.append(dict(zip(rv,result)))
        #pr1 = json.dumps(array)
        #print(json_data)

        #print (array)
        
        return json.dumps(array)
    else:
        return json.dumps('error')
    
    #print(array)   

#--------------------

@csrf.exempt
@app.route("/delpordetalle",methods=["POST","GET"])
def delpordetalle():
    if request.method == 'POST':
        id_detalle = request.form['id_detalle']
        #user = 'IjEzMjAyMzllYjljZTM0MjJlNTRiNzFlOWY1MjZkMDNkNmZmZTdlNmUi.Y0eg5A.NAyZEsSEkO0Iyrb8rOVWtzoLB3Q'
        user = request.form['user']
        cur1=db.connection.cursor()
        cur1.execute('DELETE FROM detalleventa_temp WHERE id_ventatemp = %s',[id_detalle])
        db.connection.commit()
        cur=db.connection.cursor(MySQLdb.cursors.DictCursor)
        #bb = cur.callproc('addtemp', [codproducto,cantidad,token,'10'])
        cur.execute('CALL deldetalle_temp (%s, %s)',[id_detalle,user])
        
        rv = cur.fetchall()
        
        numrows = int(cur.rowcount)
        detalletabla = ''''''
        detalletabla1=''
        sub_total = 0
        total = 0
        array = {}
        json_data = []
        #recorrido por 
        for row in rv:
            
            cant = row['cantidad']
            precio_total = row['cantidad']*row['precio_venta']
            sub_total = sub_total + precio_total
            total = total + precio_total
            
            detalletabla ='''<tr>
                                <td>%s</td>
                                <td colspan="2">%s</td>
                                <td class="textcenter">%s</td>
                                <td class="textright">%s</td>
                                <td class="textright">%s</td>
                                <td class="">
                                    <a class="link_delete" href="#" onclick="event.preventDefault();
                                    del_producto_detalle(%s);"><i class=" far fa-trash-alt"></i></a>
                                </td>
                            </tr>'''%(row['id_producto'],row['nombre'],row['cantidad'],row['precio_venta'],precio_total,row['id_ventatemp'])
           # print (detalletabla)
            detalletabla1 = detalletabla1+detalletabla

        detalletotales = '''<tr>
                                <td colspan="6" class="textright"> TOTAL</td>
                                <td class="textright">%s</td>
                            </tr>
        '''%(sub_total)

        array ['detalle']=detalletabla1
        array ['totales']=detalletotales
        row_headers = [x[0] for x in array]
        
        
        return json.dumps(array)
    else:
        return json.dumps('error')
   

@csrf.exempt
@app.route('/anularventa', methods=['GET', 'POST'])
def anularventa():  
    if request.method == 'POST':  
        token = request.form['token']
        cur = db.connection.cursor()
        cur.execute('DELETE FROM detalleventa_temp WHERE token_user = %s',[token])
        db.connection.commit()
        return json.dumps('OKS')
    else:
        return json.dumps('No jala')

#procesarventa
@csrf.exempt
@app.route('/procesarventa', methods=['GET', 'POST'])
def procesarventa():  
    if request.method == 'POST':
        id_usuario = request.form['user']
        token = request.form['token']
        codcliente = request.form['id_cliente']
        cur1=db.connection.cursor()
        cur1.execute('SELECT * FROM detalleventa_temp WHERE token_user =%s', [id_usuario])
        data1 = cur1.fetchall()
        numrows = int(cur1.rowcount)
        if numrows > 0:
            cur=db.connection.cursor()
            cur.execute('CALL procesar_venta (%s, %s, %s)',[id_usuario,codcliente,id_usuario])
            row_headers=[x[0] for x in cur.description] #this will extract row headers
            rv = cur.fetchall()

            numrows1=int(cur.rowcount)
            data=0
            json_data=[]
            for result in rv:
                json_data.append(dict(zip(row_headers,result)))

            if numrows1 > 0:
                data=json_data
                return json.dumps(data[0])      
            else:
                return json.dumps('error')    
                    #print(data)
        else:
            return json.dumps('error')
        
#*/*/*/*/*/**//**/*/*/*/*/*/*/**/*/*/*/*/*/*/*/**/*/*/*/**/*/*/*/*
@app.route('/compra')
@login_required
def compra():
    return render_template('compra.html')



@csrf.exempt
@app.route("/sacar_proveedor",methods=["POST","GET"])
def sacar_proveedor():
    if request.method == 'POST':
        codproveedor = request.form['cliente']
        cur=db.connection.cursor()
        cur.execute('SELECT * FROM proveedor WHERE id_proveedor =%s', [codproveedor])
        row_headers=[x[0] for x in cur.description] #this will extract row headers
        rv = cur.fetchall()
        numrows = int(cur.rowcount)
        
        data=''
        json_data=[]
        for result in rv:
            json_data.append(dict(zip(row_headers,result)))
        #print(rv)

        if numrows == 0:
            return json.dumps(data)
        else:
            data=json_data
            return json.dumps(data[0])


@csrf.exempt
@app.route("/detallejxc",methods=["POST","GET"])
def detallejxc():
    if request.method == 'POST':
        codproducto = request.form['codproducto']
        cantidad = request.form['cantidad']
        idp = codproducto
        cur1=db.connection.cursor()
        cur1.execute('SELECT precio FROM producto WHERE id_producto =%s', [idp])
        data1 = cur1.fetchone()
        #print (data1)
        cur2 = db.connection.cursor()
        #token = 'IjEzMjAyMzllYjljZTM0MjJlNTRiNzFlOWY1MjZkMDNkNmZmZTdlNmUi.Y0eg5A.NAyZEsSEkO0Iyrb8rOVWtzoLB3Q'
        token = request.form['token']
        cur2.execute('INSERT INTO detallecompra_temp (token_user,id_producto,cantidad,precio_venta) VALUES (%s, %s, %s, %s)',
        (token, codproducto, cantidad,data1[0]),)
        db.connection.commit()
        cur=db.connection.cursor(MySQLdb.cursors.DictCursor)
        #bb = cur.callproc('addtemp', [codproducto,cantidad,token,'10'])
        cur.execute('CALL add_detalle_tempc (%s, %s, %s)',[codproducto,cantidad,token])
        
        #print(codproducto)
        #print(cantidad)
        #print(token)
        rv = cur.fetchall()
        numrows = int(cur.rowcount)
        detalletabla = ''''''
        detalletabla1=''
        sub_total = 0
        total = 0
        array = {}
        json_data = []
        #print(rv)
        #recorrido por 
        for row in rv:
            precio_total = row['cantidad']*row['precio_venta']
            sub_total = sub_total + precio_total
            total = total + precio_total
            
            detalletabla ='''<tr>
                                <td>%s</td>
                                <td colspan="2">%s</td>
                                <td class="textcenter">%s</td>
                                <td class="textright">%s</td>
                                <td class="textright">%s</td>
                                <td class="">
                                    <a class="link_delete" href="#" onclick="event.preventDefault();
                                    del_producto_detalle(%s);"><i class=" far fa-trash-alt"></i></a>
                                </td>
                            </tr>'''%(row['id_producto'],row['nombre'],row['cantidad'],row['precio_venta'],precio_total,row['id_compratemp'])
           # print (detalletabla)
            detalletabla1 = detalletabla1+detalletabla

            

        detalletotales = '''<tr>
                                <td colspan="6" class="textright"> TOTAL</td>
                                <td class="textright">%s</td>
                            </tr>
        '''%(sub_total)

        #array.append('detalle'(detalletabla1).__dict__)
        #array.append('totales'(detalletotales).__dict__)

        array ['detalle']=detalletabla1
        array ['totales']=detalletotales#json_data.append(dict(zip(row_headers,result)))
        row_headers = [x[0] for x in array]
        

        #for result in array:
          #  json_data.append(dict(zip(rv,result)))
        #pr1 = json.dumps(array)
        #print(json_data)

        #print (array)
        
        return json.dumps(array)
    else:
        return json.dumps('error')
    
    #print(array)

@csrf.exempt
@app.route('/anularcompra', methods=['GET', 'POST'])
def anularcompra():  
    if request.method == 'POST':  
        token = request.form['token']
        cur = db.connection.cursor()
        cur.execute('DELETE FROM detallecompra_temp WHERE token_user = %s',[token])
        db.connection.commit()
        return json.dumps('OKS')
    else:
        return json.dumps('No jala')


@csrf.exempt
@app.route("/buscarpordetallec",methods=["POST","GET"])
def buscarpordetallec():
    if request.method == 'POST':
        #user = 'IjEzMjAyMzllYjljZTM0MjJlNTRiNzFlOWY1MjZkMDNkNmZmZTdlNmUi.Y0eg5A.NAyZEsSEkO0Iyrb8rOVWtzoLB3Q'
        user = request.form['user']
        cur=db.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('''SELECT   tmp.id_compratemp, 
                                tmp.token_user,
                                tmp.cantidad,
                                tmp.precio_venta,
                                p.id_producto,
                                p.nombre
                            FROM detallecompra_temp tmp
                            INNER JOIN producto p
                            ON tmp.id_producto = p.id_producto
                            WHERE token_user = %s
        
        ''', [user])
        
        rv = cur.fetchall()
        
        numrows = int(cur.rowcount)
        detalletabla = ''''''
        detalletabla1=''
        sub_total = 0
        total = 0
        array = {}
        json_data = []
        #print(rv)
        #recorrido por 
        for row in rv:
            
            cant = row['cantidad']
            precio_total = row['cantidad']*row['precio_venta']
            sub_total = sub_total + precio_total
            total = total + precio_total
            
            detalletabla ='''<tr>
                                <td>%s</td>
                                <td colspan="2">%s</td>
                                <td class="textcenter">%s</td>
                                <td class="textright">%s</td>
                                <td class="textright">%s</td>
                                <td class="">
                                    <a class="link_delete" href="#" onclick="event.preventDefault();
                                    del_producto_detalle(%s);"><i class=" far fa-trash-alt"></i></a>
                                </td>
                            </tr>'''%(row['id_producto'],row['nombre'],row['cantidad'],row['precio_venta'],precio_total,row['id_compratemp'])
           # print (detalletabla)
            detalletabla1 = detalletabla1+detalletabla

            

        detalletotales = '''<tr>
                                <td colspan="6" class="textright"> TOTAL</td>
                                <td class="textright">%s</td>
                            </tr>
        '''%(sub_total)

        #array.append('detalle'(detalletabla1).__dict__)
        #array.append('totales'(detalletotales).__dict__)

        array ['detalle']=detalletabla1
        array ['totales']=detalletotales#json_data.append(dict(zip(row_headers,result)))
        row_headers = [x[0] for x in array]
        

        #for result in array:
          #  json_data.append(dict(zip(rv,result)))
        #pr1 = json.dumps(array)
        #print(json_data)

        #print (array)
        
        return json.dumps(array)
    else:
        return json.dumps('error')
    
    #print(array)   
    

@csrf.exempt
@app.route("/delpordetallec",methods=["POST","GET"])
def delpordetallec():
    if request.method == 'POST':
        id_detalle = request.form['id_detalle']
        #user = 'IjEzMjAyMzllYjljZTM0MjJlNTRiNzFlOWY1MjZkMDNkNmZmZTdlNmUi.Y0eg5A.NAyZEsSEkO0Iyrb8rOVWtzoLB3Q'
        user = request.form['user']
        cur1=db.connection.cursor()
        cur1.execute('DELETE FROM detallecompra_temp WHERE id_compratemp = %s',[id_detalle])
        db.connection.commit()
        cur=db.connection.cursor(MySQLdb.cursors.DictCursor)
        #bb = cur.callproc('addtemp', [codproducto,cantidad,token,'10'])
        cur.execute('CALL deldetalle_tempc (%s, %s)',[id_detalle,user])
        
        rv = cur.fetchall()
        
        numrows = int(cur.rowcount)
        detalletabla = ''''''
        detalletabla1=''
        sub_total = 0
        total = 0
        array = {}
        json_data = []
        #recorrido por 
        for row in rv:
            
            cant = row['cantidad']
            precio_total = row['cantidad']*row['precio_venta']
            sub_total = sub_total + precio_total
            total = total + precio_total
            
            detalletabla ='''<tr>
                                <td>%s</td>
                                <td colspan="2">%s</td>
                                <td class="textcenter">%s</td>
                                <td class="textright">%s</td>
                                <td class="textright">%s</td>
                                <td class="">
                                    <a class="link_delete" href="#" onclick="event.preventDefault();
                                    del_producto_detalle(%s);"><i class=" far fa-trash-alt"></i></a>
                                </td>
                            </tr>'''%(row['id_producto'],row['nombre'],row['cantidad'],row['precio_venta'],precio_total,row['id_compratemp'])
           # print (detalletabla)
            detalletabla1 = detalletabla1+detalletabla

        detalletotales = '''<tr>
                                <td colspan="6" class="textright"> TOTAL</td>
                                <td class="textright">%s</td>
                            </tr>
        '''%(sub_total)

        array ['detalle']=detalletabla1
        array ['totales']=detalletotales
        row_headers = [x[0] for x in array]
        
        
        return json.dumps(array)
    else:
        return json.dumps('error')


@csrf.exempt
@app.route('/procesarcompra', methods=['GET', 'POST'])
def procesarcompra():  
    if request.method == 'POST':
        id_usuario = request.form['user']
        token = request.form['token']
        codcliente = request.form['id_cliente']
        cur1=db.connection.cursor()
        cur1.execute('SELECT * FROM detallecompra_temp WHERE token_user =%s', [id_usuario])
        data1 = cur1.fetchall()
        numrows = int(cur1.rowcount)
        if numrows > 0:
            cur=db.connection.cursor()
            cur.execute('CALL procesar_compra (%s, %s, %s)',[id_usuario,codcliente,id_usuario])
            row_headers=[x[0] for x in cur.description] #this will extract row headers
            rv = cur.fetchall()

            numrows1=int(cur.rowcount)
            data=0
            json_data=[]
            for result in rv:
                json_data.append(dict(zip(row_headers,result)))

            if numrows1 > 0:
                data=json_data
                return json.dumps(data[0])      
            else:
                return json.dumps('error')    
                    #print(data)
        else:
            return json.dumps('error')

#CRUDSS
@app.route('/view_proveedor')
@login_required
def view_proveedor():
    cur=db.connection.cursor()
    cur.execute('SELECT * FROM proveedor')
    data = cur.fetchall()
    return render_template('viewproveedor.html', listas =data)

@app.route('/view_proveedorsearch', methods = ['POST'])
@login_required
def view_proveedorsearch():
    if request.method == 'POST':
        id_producto = request.form['id_producto']
        cur=db.connection.cursor()
        cur.execute('SELECT * FROM proveedor WHERE nombre LIKE %(nombre)s or id_proveedor LIKE %(id_proveedor)s', { 'nombre': '%{}%'.format(id_producto),'id_proveedor': '%{}%'.format(id_producto)})
        data = cur.fetchall()
        numrows = int(cur.rowcount)

        flash("%s Proveedor(es) encontrado(s)"%(numrows))
        return render_template('viewsearchproveedor.html', listas =data)
    else:
        flash("Proveedor No encontrado")
        return redirect(url_for('view_proveedorsearch'))

@app.route('/editproveedor/<id>')
@login_required
def editproveedor(id):
    cur = db.connection.cursor()
    cur.execute('SELECT * FROM proveedor WHERE id_proveedor =%s', [id])
    data = cur.fetchall()
    print (data[0])
    return render_template('conf_proveedor.html', dato = data[0])


@app.route('/editpr/<id>', methods = ['POST'])
def editpr(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        lugar = request.form['lugar']
        cur = db.connection.cursor()
        cur.execute("""
        UPDATE proveedor
        SET nombre = %s,
            apellido = %s,
            direccion = %s,
            telefono = %s,
            lugar = %s
        WHERE id_proveedor = %s
        """, (nombre, apellido, direccion,  telefono, lugar, [id]))
        db.connection.commit()
        flash("Datos proveedor actualizados")
        return redirect(url_for('view_proveedor'))

@app.route('/eliminarpr/<id>')
def eliminar(id):
    cur = db.connection.cursor()
    cur.execute('DELETE FROM proveedor WHERE id_proveedor = {0}'.format(id))
    db.connection.commit()
    flash("Proveedor eliminado")
    return redirect(url_for('view_proveedor'))

@app.route('/view_venta')
@login_required
def view_venta():
    cur=db.connection.cursor()
    cur.execute('SELECT * FROM venta')
    data = cur.fetchall()
    return render_template('viewventa.html', listas =data)

@app.route('/view_compra')
@login_required
def view_compra():
    cur=db.connection.cursor()
    cur.execute('SELECT * FROM compra')
    data = cur.fetchall()
    return render_template('viewcompra.html', listas =data)

@app.route('/view_marca')
@login_required
def view_marca():
    cur=db.connection.cursor()
    cur.execute('SELECT * FROM marca')
    data = cur.fetchall()
    return render_template('viewmarca.html', listas =data)

@app.route('/view_marcasearch', methods = ['POST'])
@login_required
def view_marcasearch():
    if request.method == 'POST':
        id_producto = request.form['id_producto']
        cur=db.connection.cursor()
        cur.execute('SELECT * FROM marca WHERE nombre LIKE %(nombre)s or id LIKE %(id)s', { 'nombre': '%{}%'.format(id_producto),'id': '%{}%'.format(id_producto)})
        data = cur.fetchall()
        numrows = int(cur.rowcount)

        flash("%s Marca(s) encontrada(s)"%(numrows))
        return render_template('viewsearchmarca.html', listas =data)
    else:
        flash("Marca No encontrada")
        return redirect(url_for('view_marcasearch'))

@app.route('/editmarca/<id>')
@login_required
def editmarca(id):
    cur = db.connection.cursor()
    cur.execute('SELECT * FROM marca WHERE id =%s', [id])
    data = cur.fetchall()
    print (data[0])
    return render_template('conf_marca.html', dato = data[0])


@app.route('/editmar/<id>', methods = ['POST'])
def editmar(id):
    if request.method == 'POST':

        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        cur = db.connection.cursor()
        cur.execute("""
        UPDATE marca
        SET nombre = %s,
        descripcion = %s
        WHERE id = %s
        """, (nombre,descripcion,[id]))
        db.connection.commit()
        flash("Marca actualizada")
        return redirect(url_for('view_marca'))

@app.route('/eliminarmarca/<id>')
def eliminarmarca(id):
    cur = db.connection.cursor()
    cur.execute('DELETE FROM marca WHERE id = {0}'.format(id))
    db.connection.commit()
    flash("Marca eliminada")
    return redirect(url_for('view_marca'))



@app.route('/view_categoria')
@login_required
def view_categoria():
    cur=db.connection.cursor()
    cur.execute('SELECT * FROM categoria')
    data = cur.fetchall()
    return render_template('viewcategoria.html', listas =data)



@app.route('/view_categoriasearch', methods = ['POST'])
@login_required
def view_categoriasearch():
    if request.method == 'POST':
        id_producto = request.form['id_producto']
        cur=db.connection.cursor()
        cur.execute('SELECT * FROM categoria WHERE nombre LIKE %(nombre)s or id LIKE %(id)s', { 'nombre': '%{}%'.format(id_producto),'id': '%{}%'.format(id_producto)})
        data = cur.fetchall()
        numrows = int(cur.rowcount)

        flash("%s Categoria(s) encontrada(s)"%(numrows))
        return render_template('viewsearchcategoria.html', listas =data)
    else:
        flash("Categoria No encontrada")
        return redirect(url_for('view_categoriasearch'))   


@app.route('/editcategoria/<id>')
@login_required
def editcategoria(id):
    cur = db.connection.cursor()
    cur.execute('SELECT * FROM categoria WHERE id =%s', [id])
    data = cur.fetchall()
    print (data[0])
    return render_template('conf_categoria.html', dato = data[0])


@app.route('/editcat/<id>', methods = ['POST'])
def editcat(id):
    if request.method == 'POST':

        nombre = request.form['nombree']
        descripcion = request.form['descripcion']
        cur = db.connection.cursor()
        cur.execute("""
        UPDATE categoria
        SET nombre = %s,
        descripcion = %s
        WHERE id = %s
        """, (nombre,descripcion,[id]))
        db.connection.commit()
        flash("Categoria actualizada")
        return redirect(url_for('view_categoria'))

@app.route('/eliminarcategoria/<id>')
def eliminarcategoria(id):
    cur = db.connection.cursor()
    cur.execute('DELETE FROM categoria WHERE id = {0}'.format(id))
    db.connection.commit()
    flash("Categoria eliminada")
    return redirect(url_for('view_categoria'))


@app.route('/view_usuario')
@login_required
def view_usuario():
    cur=db.connection.cursor()
    cur.execute('SELECT * FROM usuario')
    data = cur.fetchall()
    return render_template('viewusuario.html', listas =data)

@app.route('/view_usuariosearch', methods = ['POST'])
@login_required
def view_usuariosearch():
    if request.method == 'POST':
        id_producto = request.form['id_producto']
        cur=db.connection.cursor()
        cur.execute('SELECT * FROM usuario WHERE nombre LIKE %(nombre)s or id LIKE %(id)s or usuario LIKE %(usuario)s or roll LIKE %(roll)s', { 'nombre': '%{}%'.format(id_producto),'id': '%{}%'.format(id_producto),'usuario': '%{}%'.format(id_producto),'roll': '%{}%'.format(id_producto)})
        data = cur.fetchall()
        numrows = int(cur.rowcount)

        flash("%s Usuario(s) encontrado(s)"%(numrows))
        return render_template('viewsearchusuario.html', listas =data)
    else:
        flash("Usuario No encontrado")
        return redirect(url_for('view_usuariosearch'))

@app.route('/editusuario/<id>')
@login_required
def editusuario(id):
    cur = db.connection.cursor()
    cur.execute('SELECT * FROM usuario WHERE id =%s', [id])
    data = cur.fetchall()
    print (data[0])
    return render_template('conf_usuario.html', dato = data[0])


@app.route('/edituse/<id>', methods = ['POST'])
def edituse(id):
    if request.method == 'POST':

        nombre = request.form['nombre']
        apellido = request.form['apellido']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        email = request.form['email']
        usuario = request.form['usuario']
        roll = request.form['roll']
        estado = request.form['estado']
        cur = db.connection.cursor()
        cur.execute("""
        UPDATE usuario
        SET nombre = %s,
        apellido = %s,
        usuario = %s,
        roll = %s,
        telefono = %s,
        direccion = %s,
        email = %s,
        estado = %s
        WHERE id = %s
        """, (nombre,apellido,usuario,roll,telefono,direccion,email,estado,[id]))
        db.connection.commit()
        flash("Datos de usuario actualizados")
        return redirect(url_for('view_usuario'))

@app.route('/eliminarusuario/<id>')
def eliminarusuario(id):
    cur = db.connection.cursor()
    cur.execute('DELETE FROM usuario WHERE id = {0}'.format(id))
    db.connection.commit()
    flash("Usuario eliminado")
    return redirect(url_for('view_usuario'))



@app.route('/view_cliente')
@login_required
def view_cliente():
    cur=db.connection.cursor()
    cur.execute('SELECT * FROM cliente')
    data = cur.fetchall()
    return render_template('viewcliente.html', listas =data)

@app.route('/view_clientesearch', methods = ['POST'])
@login_required
def view_clientesearch():
    if request.method == 'POST':
        id_producto = request.form['id_producto']
        cur=db.connection.cursor()
        cur.execute('SELECT * FROM cliente WHERE nombre LIKE %(nombre)s or id_cliente LIKE %(id_cliente)s', { 'nombre': '%{}%'.format(id_producto),'id_cliente': '%{}%'.format(id_producto)})
        data = cur.fetchall()
        numrows = int(cur.rowcount)

        flash("%s Cliente(s) encontrado(s)"%(numrows))
        return render_template('viewsearchcliente.html', listas =data)
    else:
        flash("Proveedor No encontrado")
        return redirect(url_for('view_clientesearch'))

@app.route('/editcliente/<id>')
@login_required
def editcliente(id):
    cur = db.connection.cursor()
    cur.execute('SELECT * FROM cliente WHERE id_cliente =%s', [id])
    data = cur.fetchall()
    print (data[0])
    return render_template('conf_cliente.html', dato = data[0])


@app.route('/editcli/<id>', methods = ['POST'])
def editcli(id):
    if request.method == 'POST':

        nombre = request.form['nombre']
        apellido = request.form['apellido']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        email = request.form['email']
        descripcion = request.form['descripcion']
        estado = request.form['estado']
        cur = db.connection.cursor()
        cur.execute("""
        UPDATE cliente
        SET nombre = %s,
        apellido = %s,
        direccion = %s,
        telefono = %s,
        email = %s,
        descripcion = %s,
        estado = %s
        WHERE id_cliente = %s
        """, (nombre,apellido,direccion,telefono,email,descripcion,estado,[id]))
        db.connection.commit()
        flash("Datos de cliente actualizados")
        return redirect(url_for('view_cliente'))

@app.route('/eliminarcliente/<id>')
def eliminarcliente(id):
    cur = db.connection.cursor()
    cur.execute('DELETE FROM cliente WHERE id_cliente = {0}'.format(id))
    db.connection.commit()
    flash("Cliente eliminado")
    return redirect(url_for('view_cliente'))


@app.route('/view_productoSearch', methods = ['POST'])
@login_required
def view_productoSearch():
    if request.method == 'POST':
        id_producto = request.form['id_producto']
        cur=db.connection.cursor()
        cur.execute('SELECT * FROM producto WHERE nombre LIKE %(nombre)s or marca LIKE %(marca)s or id_producto LIKE %(id_producto)s', { 'nombre': '%{}%'.format(id_producto),'marca': '%{}%'.format(id_producto),'id_producto': '%{}%'.format(id_producto)})
        data = cur.fetchall()
        numrows = int(cur.rowcount)

        flash("%s Producto(s) encontrado(s)"%(numrows))
        return render_template('viewsearchproducto.html', listas =data)
    else:
        flash("Producto No encontrado")
        return redirect(url_for('view_producto'))   

@app.route('/view_producto')
@login_required
def view_producto():
    cur=db.connection.cursor()
    cur.execute('SELECT * FROM producto')
    data = cur.fetchall()
    return render_template('viewproducto.html', listas =data)


@app.route('/editproducto/<id>')
@login_required
def editproducto(id):
    cur2=db.connection.cursor()
    cur2.execute('SELECT * FROM marca')
    data2 = cur2.fetchall()
    cur1=db.connection.cursor()
    cur1.execute('SELECT * FROM categoria')
    data1 = cur1.fetchall()
    
    cur = db.connection.cursor()
    cur.execute('SELECT * FROM producto WHERE id_producto =%s', [id])
    data = cur.fetchall()
    print (data[0])
    return render_template('conf_producto.html', dato = data[0], marcas =data2, categorias =data1)


@app.route('/editprod/<id>', methods = ['POST'])
def editprod(id):
    if request.method == 'POST':
        id_prod =request.form['id_producto']
        nombre = request.form['nombre']
        marca = request.form['marca']
        categoria = request.form['categoria']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        estado = request.form['estado']
        cur = db.connection.cursor()
        cur.execute("""
        UPDATE producto
        SET id_producto = %s,
            nombre = %s,
            marca = %s,
            categoria = %s,
            descripcion = %s,
            precio = %s,
            estado = %s
        WHERE id_producto = %s
        """, (id_prod, nombre, marca, categoria,  descripcion, precio, estado, [id]))
        db.connection.commit()
        flash("Datos de producto actualizados")
        return redirect(url_for('view_producto'))

@app.route('/eliminarprod/<id>')
def eliminarprod(id):
    cur = db.connection.cursor()
    cur.execute('DELETE FROM producto WHERE id_producto = {0}'.format(id))
    db.connection.commit()
    flash("Producto eliminado")
    return redirect(url_for('view_producto'))

#VER LA COMPRA

@app.route('/view_comprasearch', methods = ['POST'])
@login_required
def view_comprasearch():
    if request.method == 'POST':
        fechad = request.form['fecha_de']
        fechaa = request.form['fecha_a']

        cur=db.connection.cursor()
        cur.execute('SELECT * FROM compra WHERE fecha BETWEEN %s AND %s',(fechad,fechaa))
        data = cur.fetchall()
        numrows = int(cur.rowcount)

        flash("%s Compra(s) encontrada(s)"%(numrows))
        return render_template('viewcompra.html', listas =data)
    else:
        flash("Producto No encontrado")
        return redirect(url_for('view_compra'))   

@app.route('/view_ventasearch', methods = ['POST'])
@login_required
def view_ventasearch():
    if request.method == 'POST':
        fechad = request.form['fecha_de']
        fechaa = request.form['fecha_a']

        cur=db.connection.cursor()
        cur.execute('SELECT * FROM venta WHERE fecha BETWEEN %s AND %s',(fechad,fechaa))
        data = cur.fetchall()
        numrows = int(cur.rowcount)

        flash("%s venta(s) encontrada(s)"%(numrows))
        return render_template('viewventa.html', listas =data)
    else:
        flash("Producto No encontrado")
        return redirect(url_for('view_venta')) 


@csrf.exempt
@app.route("/seleccioncompra")
def seleccioncompra():
    #if request.method == 'POST':
        fac = request.args.get('factu')
        user = 'IjEzMjAyMzllYjljZTM0MjJlNTRiNzFlOWY1MjZkMDNkNmZmZTdlNmUi.Y0eg5A.NAyZEsSEkO0Iyrb8rOVWtzoLB3Q'
        cur=db.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('''SELECT   dt.correlativo, 
                                dt.nocompra,
                                dt.cantidad,
                                dt.precio_venta,
                                p.id_producto,
                                p.nombre
                            FROM detallecompra dt
                            INNER JOIN producto p
                            ON dt.id_producto = p.id_producto
                            WHERE nocompra = %s
        
        ''', [fac])
        
        rv = cur.fetchall()
        
        numrows = int(cur.rowcount)
        detalletabla = ''''''
        detalletabla1=''
        sub_total = 0
        total = 0
        nocompra =''
        array = {}
        json_data = []
        #print(rv)
        #recorrido por 
        for row in rv:
            nocompra = row['nocompra']
            cant = row['cantidad']
            precio_total = row['cantidad']*row['precio_venta']
            sub_total = sub_total + precio_total
            total = total + precio_total
            
            detalletabla ='''<tr>
                                <td>%s</td>
                                <td colspan="2">%s</td>
                                <td class="textcenter">%s</td>
                                <td class="textright">%s</td>
                                <td class="textright">%s</td>
                                
                            </tr>'''%(row['id_producto'],row['nombre'],row['cantidad'],row['precio_venta'],precio_total)
           # print (detalletabla)
            detalletabla1 = detalletabla1+detalletabla

            

        detalletotales = '''<tr>
                                <td colspan="5" class="textright"> TOTAL</td>
                                <td class="textright">%s</td>
                            </tr>
        '''%(sub_total)


        #array.append('detalle'(detalletabla1).__dict__)
        #array.append('totales'(detalletotales).__dict__)

        array ['detalle']=detalletabla1
        array ['totales']=detalletotales
        array ['compra']=nocompra#json_data.append(dict(zip(row_headers,result)))
        row_headers = [x[0] for x in array]
        

        #for result in array:
          #  json_data.append(dict(zip(rv,result)))
        #pr1 = json.dumps(array)
        #print(json_data)

        #print (array)
       # webbrowser.open_new("https://flask.palletsprojects.com/en/2.2.x/patterns/javascript/")
        global res 
        res = array
       # print (res)
        return (json.dumps(array))
    #else:
       # return json.dumps('error')
    
    #print(array)   



@csrf.exempt
@app.route('/selectorcompra')
def selectorcompra():
    a = json.dumps(res)
    print (a)
    return render_template('selectcompra.html', resi = a)




#VER LA venta

@csrf.exempt
@app.route("/seleccionventa")
def seleccionventa():
    #if request.method == 'POST':
        fac = request.args.get('factu')
        user = 'IjEzMjAyMzllYjljZTM0MjJlNTRiNzFlOWY1MjZkMDNkNmZmZTdlNmUi.Y0eg5A.NAyZEsSEkO0Iyrb8rOVWtzoLB3Q'
        cur=db.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('''SELECT   dt.correlativo, 
                                dt.nofactura,
                                dt.cantidad,
                                dt.precio_venta,
                                p.id_producto,
                                p.nombre
                            FROM detalleventa dt
                            INNER JOIN producto p
                            ON dt.id_producto = p.id_producto
                            WHERE nofactura = %s
        
        ''', [fac])
        
        rv = cur.fetchall()
        
        numrows = int(cur.rowcount)
        detalletabla = ''''''
        detalletabla1=''
        sub_total = 0
        total = 0
        nofactura =''
        array = {}
        json_data = []
        #print(rv)
        #recorrido por 
        for row in rv:
            nofactura = row['nofactura']
            cant = row['cantidad']
            precio_total = row['cantidad']*row['precio_venta']
            sub_total = sub_total + precio_total
            total = total + precio_total
            
            detalletabla ='''<tr>
                                <td>%s</td>
                                <td colspan="2">%s</td>
                                <td class="textcenter">%s</td>
                                <td class="textright">%s</td>
                                <td class="textright">%s</td>
                                
                            </tr>'''%(row['id_producto'],row['nombre'],row['cantidad'],row['precio_venta'],precio_total)
           # print (detalletabla)
            detalletabla1 = detalletabla1+detalletabla

            

        detalletotales = '''<tr>
                                <td colspan="5" class="textright"> TOTAL</td>
                                <td class="textright">%s</td>
                            </tr>
        '''%(sub_total)


        #array.append('detalle'(detalletabla1).__dict__)
        #array.append('totales'(detalletotales).__dict__)

        array ['detalle']=detalletabla1
        array ['totales']=detalletotales
        array ['venta']=nofactura#json_data.append(dict(zip(row_headers,result)))
        row_headers = [x[0] for x in array]
        

        #for result in array:
          #  json_data.append(dict(zip(rv,result)))
        #pr1 = json.dumps(array)
        #print(json_data)

        #print (array)
       # webbrowser.open_new("https://flask.palletsprojects.com/en/2.2.x/patterns/javascript/")
        global res 
        res = array
       # print (res)
        return (json.dumps(array))
    #else:
       # return json.dumps('error')
    
    #print(array)   



@csrf.exempt
@app.route('/selectorventa')
def selectorventa():
    a = json.dumps(res)
    print (a)
    return render_template('selectventa.html', resi = a)



@csrf.exempt
@app.route('/vercompra')
def vercompra():
    if request.method == 'POST':
        codpro = request.form['pro']
        codfac = request.form['fac']
        cur1=db.connection.cursor(MySQLdb.cursors.DictCursor)
        cur1.execute('SELECT * FROM empresa')
        numrows1 = int(cur1.rowcount)
        rv1 = cur1.fetchall()
        cur2=db.connection.cursor(MySQLdb.cursors.DictCursor)
        cur2.execute('''SELECT c.nocompra, c.fecha, c.id_proveedor, c.estatus
                    v.nombre as usuario
                    cl.id_cliente, cl.nombre, cl.telefono,cl.direccion
                    FROM compra c
                    INNER JOIN usuario v
                    ON c.usuario = v.id
                    INNER JOIN cliente cl
                    ON c.id_proveedor = cl.id_cliente
                    WHERE c.nocompra = %s AND c.id_proveedor = %s
        ''', [codfac,codpro])
        numrows = int(cur2.rowcount)
        rv = cur2.fetchall()
        compra = ''
        for row in rv:
            compra = row['nocompra']

        cur=db.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('''SELECT p.nombre,dt.cantidad,dt.precio_venta, (dt.cantidad * dt.precio_venta) as precio_total
                    FROM compra c
                    INNER JOIN detallecompra dt
                    ON c.nocompra = dt.nocompra
                    INNER JOIN producto.p
                    ON dt.id_producto = p.id_producto
                    WHERE c.nocompra = %s

        ''', [codfac ])
        numrows = int(cur.rowcount)
        rv = cur.fetchall()

        

        return 0






@csrf.exempt
@app.route('/ajax')
def ajax():
    cursor = db.connection.cursor()
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    result = cur.execute("SELECT * FROM tbl_employee ORDER BY id")
    employee = cur.fetchall()   
    return render_template('ajax.html', employee=employee)

@csrf.exempt
@app.route('/insert', methods=['GET', 'POST'])
def insert():   
    cursor = db.connection.cursor()
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST': 
        name = request.form['name']
        address = request.form['address']
        gender = request.form['gender']
        designation = request.form['designation']
        age = request.form['age']
        cur.execute("INSERT INTO tbl_employee (name, address, gender, designation, age) VALUES (%s, %s, %s, %s, %s)",[name, address, gender, designation, age])
        db.connection.commit()
        
    return jsonify('success')

@csrf.exempt
@app.route('/select', methods=['GET', 'POST'])
def select():   
    cursor = db.connection.cursor()
    cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST': 
        employee_id = request.form['employee_id']
        print(employee_id)      
        result = cur.execute("SELECT * FROM tbl_employee WHERE id = %s", [employee_id])
        rsemployee = cur.fetchall()
        employeearray = []
        for rs in rsemployee:
            employee_dict = {
                    'Id': rs['id'],
                    'emp_name': rs['name'],
                    'address': rs['address'],
                    'gender': rs['gender'],
                    'designation': rs['designation'],
                    'age': rs['age']}
            employeearray.append(employee_dict)
        return json.dumps(employeearray)



@app.route('/home')
@login_required
def home():

    #now = date.today()
    #print("now =", now)
    return render_template('home.html')

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf = CSRFProtect(app)
    app.register_error_handler(401,status_401)
    app.register_error_handler(404,status_404)
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run()
