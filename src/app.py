from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL
from datetime import datetime

app= Flask(__name__)
mysql= MySQL()

app.config['MYSQL_DATABASE_HOST']= 'localhost'
app.config['MYSQL_DATABASE_USER']= 'root'
app.config['MYSQL_DATABASE_PASSWORD']= ''
app.config['MYSQL_DATABASE_BD']= 'empleados'

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


@app.route('/route_name')
def method_name():
    pass


#NOTA - creamos un if para que muestre los errores que vayan ocurriendo mientras cargamos código
if __name__ == '__main__':
    app.run(debug=True)