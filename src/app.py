from flask import Flask
from flask import render_template
from flaskext.mysql import MySQL

app= Flask(__name__)
mysql= MySQL()

app.config['MYSQL_DATABASE_HOST']= 'localhost'
app.config['MYSQL_DATABASE_USER']= 'root'
app.config['MYSQL_DATABASE_PASSWORD']= ''
app.config['MYSQL_DATABASE_BD']= 'empleados'

mysql.init_app(app)

@app.route('/')
def index():
    sql= "INSERT INTO `empleados`.`empleados` (`Nombre`, `Correo`, `Foto`) VALUES ('Juan', 'juan@gmail.com', 'fotojuan.jpg');"
    conn= mysql.connect()
    cursor= conn.cursor()
    cursor.execute(sql)
    
    conn.commit()

    return render_template('empleados/index.html')

#NOTA - creamos un if para que muestre los errores que vayan ocurriendo mientras cargamos código
if __name__ == '__main__':
    app.run(debug=True)