from flask import Flask, render_template, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators, ValidationError
from flask_mysqldb import MySQL
import bcrypt

app = Flask(__name__)

### MySQL Configuration
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'scott'
app.config['MYSQL_PASSWORD'] = 'tiger'
app.config['MYSQL_DB'] = 'flask_login4'
app.secret_key = 'your_secret_key_here'

mysql = MySQL(app)

class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[
        validators.DataRequired(),
        validators.Length(min=3, max=20)
    ])
    
    email = StringField("Email", validators=[
        validators.DataRequired(),
        validators.Length(min=3, max=50),
        validators.Email()
    ])
    
    password = PasswordField("Password", validators=[
        validators.DataRequired(),
        validators.Length(min=3, max=25)
    ])
    
    passwordCheck = PasswordField("Confirm Password", validators=[
        validators.DataRequired(),
        validators.EqualTo('password', message='Passwords must match')
    ])
    
    submit = SubmitField("Register")
       
class LoginForm(FlaskForm):
    email = StringField(
        label="Email",
        validators=[
            validators.DataRequired(),
            validators.Length(min=3, max=50),
            validators.Email()
        ]
    )
    
    password = PasswordField("Password", validators=[
        validators.DataRequired(),
        validators.Length(min=3, max=25)
    ])
    
    submit = SubmitField("Login")

### route Definition
@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():      # if methods = 'POST'
        name = form.name.data
        email = form.email.data
        password = form.password.data

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        print(f">>> Hashed Password : {hashed_password}")

        try:
            with mysql.connection.cursor() as cursor:
                cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
                mysql.connection.commit()

        except Exception as e:
            mysql.connection.rollback()
            flash(f'Database connection error: {e}', 'danger')
            return render_template('error.html', title='Error')

        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():      # if methods = 'POST'
        email = form.email.data
        password = form.password.data
                
        try:
            with mysql.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
                user = cursor.fetchone()
                
                if user:
                    print(f"User Object: {user}")
                    for attribute in user:
                        print(attribute)

        except Exception as e:
            flash(f'Database connection error: {e}', 'danger')
            return render_template('error.html', title='Error')
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
            session['user_id'] = user[0]
            return redirect(url_for('dashboard'))
        else:
            flash("Login failed. Please check your email and password")
            return redirect(url_for('login'))

    return render_template('login.html', title='Login', form=form)

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
                
        try:
            with mysql.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users where id=%s",(user_id,))
                user = cursor.fetchone()
            
            if user:
                print(f"User Object: {user}")
                for attribute in user:
                    print(attribute)

        except Exception as e:
            flash(f'Database connection error: {e}', 'danger')
            return render_template('error.html', title='Error')
                
        if user:
            return render_template('dashboard.html', user=user)
    
    # return redirect(url_for('index'))
    return render_template('error.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("You have been logged out successfully.")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
