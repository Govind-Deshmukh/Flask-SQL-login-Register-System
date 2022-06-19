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
def home():
    if request.method == 'POST':               
        username = request.form['username']
        password = request.form['password']
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM users WHERE username = '"+username+"' AND password = '"+password+"';")
        data = cursor.fetchall()
        if len(data) == 0:
            flash('Invalid username or password')
            return redirect(url_for('home'))
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
            flash('Password does not match')
            return redirect(url_for('register'))
        #check if username already exists
        else:
            cursor.execute("SELECT * FROM users WHERE username = %s", (request.form['username'],))
            user = cursor.fetchone()
            if user:
                flash('User already exists')
                return redirect(url_for('home'))
            else:
                name = request.form['name']
                email = request.form['email']
                contact = request.form['contact']
                username = request.form['username']
                password = request.form['password']
                cursor.execute("INSERT INTO users (name,email,contact,username,password) VALUES (%s,%s,%s,%s,%s)",(name,email,contact,username,password))
                mydb.commit()
                flash('You are now registered and can log in','success')
                return redirect(url_for('home'))

    if request.method == 'GET':
        return render_template('register.html')

@app.route('/dashboard' , methods=['GET','POST'])
def dashboard():
    if 'username' in session:

        cursor.execute("SELECT * FROM users WHERE username = '"+session['username']+"';")
        data = cursor.fetchall()
        return render_template('home.html',data=data)
    else:
        flash('You are not logged in','danger')
        return redirect(url_for('home'))

if '__main__' == __name__:
    app.run(host='0.0.0.0', debug=True)
    