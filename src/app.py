from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL
from datetime import datetime
import os

app= Flask(__name__)
mysql= MySQL()

app.config['MYSQL_DATABASE_HOST']= 'localhost'
app.config['MYSQL_DATABASE_USER']= 'root'
app.config['MYSQL_DATABASE_PASSWORD']= ''
app.config['MYSQL_DATABASE_BD']= 'empleados'

UPLOADS= os.path.join('uploads')
app.config['UPLOADS']= UPLOADS #NOTA -> Guardamos la ruta como un valor en la app

mysql.init_app(app)

@app.route('/')
def index():
    conn= mysql.connect()
    cursor= conn.cursor()

    sql= "SELECT * FROM empleados.empleados"
    cursor.execute(sql) 
    
    empleados= cursor.fetchall()

    conn.commit()

    return render_template('empleados/index.html', empleados= empleados)


@app.route('/create')
def create():
    return render_template('empleados/create.html')


@app.route('/store', methods=['post'])
def store():
    _nombre= request.form['txtNombre']
    _correo= request.form['txtCorreo']
    _foto= request.files['txtFoto']

    now= datetime.now()
    tiempo= now.strftime("%Y%H%M%S")

    nuevoNombreFoto= ''
    if _foto.filename != '':
        nuevoNombreFoto= tiempo + '_' + _foto.filename
        _foto.save("src/uploads/" + nuevoNombreFoto)

    sql= "INSERT INTO empleados.empleados (Nombre, Correo, Foto) VALUES (%s, %s, %s);"
    datos= (_nombre, _correo, nuevoNombreFoto)
    
    conn= mysql.connect()
    cursor= conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/')


@app.route('/delete/<int:id>')
def delete(id):
    sql= "DELETE FROM empleados.empleados WHERE id=%s"
    conn= mysql.connect()
    cursor= conn.cursor()
    cursor.execute(sql, id)
    conn.commit()

    return redirect('/')



@app.route('/modify/<int:id>')
def modify(id):
    sql= f'SELECT * FROM empleados.empleados WHERE id={id}' # También se admite esta sintaxis
    conn= mysql.connect()
    cursor= conn.cursor()
    cursor.execute(sql) # Y aquí se quita la , id
    empleado= cursor.fetchone()
    conn.commit()

    return render_template('empleados/edit.html', empleado=empleado)

@app.route('/update', methods=['POST'])
def update():
    _nombre= request.form['txtNombre']
    _correo= request.form['txtCorreo']
    _foto= request.files['txtFoto']
    id= request.form['txtId']

    datos= (_nombre, _correo, id)

    conn= mysql.connect()
    cursor= conn.cursor()

    nuevoNombreFoto= ''
    if _foto.filename != '':
        now= datetime.now()
        tiempo= now.strftime("%Y%H%M%S")
        nuevoNombreFoto= tiempo + '_' + _foto.filename
        _foto.save("src/uploads/" + nuevoNombreFoto)
    
    sql= f'SELECT foto FROM empleados where id={id}'
    cursor.execute(sql)

    nombreFoto= cursor.fetchone()[0]

    os.remove(os.path.join(app.config['UPLOADS'], nombreFoto))


    conn= mysql.connect()
    cursor= conn.cursor()
    #NOTA -> Reescribimos la variable sql (reutilizar)
    sql= f'UPDATE empleados SET Nombre={_nombre}, Correo={_correo} WHERE ID={id}'
    cursor.execute(sql)
    conn.commit()





#NOTA - creamos un if para que muestre los errores que vayan ocurriendo mientras cargamos código
if __name__ == '__main__':
    app.run(debug=True)