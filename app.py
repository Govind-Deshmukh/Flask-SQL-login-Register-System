#flask app template 
from flask import Flask,render_template,request,redirect,url_for,flash,session,g,jsonify
import mysql.connector

app = Flask(__name__)
app.secret_key = 'iamgoodboi'

mydb = mysql.connector.connect(
	host = "remotemysql.com",
	user = "VWRnLTM6RW",
	password = "HdCZfdhdbw",
    database = "VWRnLTM6RW"
)
cursor = mydb.cursor()
@app.route('/' , methods=['GET','POST'])
def login():
    if request.method == 'POST':               
        username = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT * FROM users WHERE username = '"+username+"' AND password = '"+password+"';")
        data = cursor.fetchall()
        if len(data) == 0:
            flash(f'Invalid username or password','danger')
            return redirect(url_for('login'))
        else:
            session['username'] = username
            return redirect(url_for('dashboard'))
    if request.method == 'GET':
        return render_template('index.html')

@app.route('/register' , methods=['GET','POST'])
def register():
    if request.method == 'POST':
        #check confirm passowrd and password
        if request.form['password'] != request.form['confpassword']:
            flash(f'Password does not match','danger')
            return redirect(url_for('register'))
        #check if username already exists
        else:
            username = request.form['username']
            cursor.execute("SELECT * FROM users WHERE username = %s", [username])
            user = cursor.fetchone()
            if user:
                flash(f'User already exists')
                return redirect(url_for('login'))
            else:
                name = request.form['name']
                email = request.form['email']
                contact = request.form['contact']
                username = request.form['username']
                password = request.form['password']
                cursor.execute("INSERT INTO users (name,email,contact,username,password) VALUES (%s,%s,%s,%s,%s)",(name,email,contact,username,password))
                mydb.commit()
                flash(f'You are now registered and can log in','success')
                return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('register.html')

@app.route('/dashboard' , methods=['GET','POST'])
def dashboard():
    if 'username' in session:
        cursor.execute("SELECT * FROM users WHERE username = '"+session['username']+"';")
        data = cursor.fetchall()
        return render_template('home.html',data=data)
    else:
        flash(f'You are not logged in','danger')
        return redirect(url_for('login'))

if '__main__' == __name__:
    app.run()
    