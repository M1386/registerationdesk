from flask import Flask, render_template, request, session, redirect,url_for
from flask_mysqldb import MySQL
from flask_mail import Mail, Message

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'data'
app.config['SECRET_KEY'] = 'your_secret_key'

mysql = MySQL(app)



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def project():
    return render_template('projects.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    message=''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        # cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        print("Entered Password:", password)
        print("Database Password:", user[2])

        if password == user[2]:
            # return 'Logged in successfully!'
            message = "Login successful!"
            return redirect(url_for('home'))
        else:
            message='Invalid Email or password'
        
        
    return render_template("login.html",message=message)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        mysql.connection.commit()
        cur.close()
        
        # return 'You have successfully registered!'
        return redirect(url_for('login'))
    
    
    
    return render_template('registeration.html')








if __name__ == '__main__':
    app.run(debug=True)
