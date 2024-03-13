from flask import Flask, render_template, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from flask_mysqldb import MySQL
import bcrypt

app = Flask(__name__)

### MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_login4'
app.secret_key = 'your_secret_key_here'

mysql = MySQL(app)

### wtforms Definition
# wtforms doc : https://wtforms.readthedocs.io/en/3.1.x/
# - https://flask-docs-kr.readthedocs.io/latest/patterns/wtforms.html
class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[
        validators.DataRequired(),
        validators.Length(min=3, max=20)
    ])
    email = StringField("Email", validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField("Password", validators=[
        validators.DataRequired(),
        validators.Length(min=3, max=25),
        validators.EqualTo('passwordCheck', message='Passwords must match')
    ])
    passwordCheck = PasswordField("Confirm Password", validators=[validators.DataRequired()])
    submit = SubmitField("Register")

    def validate_email(self, field):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users where email=%s",(field.data,))
        user = cursor.fetchone()
        cursor.close()
        if user:
            raise ValidationError('Email Already Taken')
       
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[validators.DataRequired(), validators.Email()])
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
        passwordCheck = form.passwordCheck.data

        hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
        # print(hashed_password)
        
        # store data into database 
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s,%s,%s)",(name, email, hashed_password))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():      # if methods = 'POST'
        email = form.email.data
        password = form.password.data

        cursor = mysql.connection.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE email=%s",(email,))
            user = cursor.fetchone()
        except MySQLdb.OperationalError as detail:
            (error_code, msg) = detail.args
            # plugin already loaded, nothing to do.
            if error_code != MYSQL_ERROR_FUNCTION_EXISTS:
                raise
        cursor.close()
        
        print(user)
        if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
            session['user_id'] = user[0]
            return redirect(url_for('dashboard'))
        else:
            flash("Login failed. Please check your email and password")
            return redirect(url_for('login'))

    return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users where id=%s",(user_id,))
        user = cursor.fetchone()
        cursor.close()

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
    
