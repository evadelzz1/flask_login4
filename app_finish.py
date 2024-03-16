from flask import Flask, render_template, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import bcrypt, pickle
import Config, ClassForm, DB

app = Flask(__name__)

###################################################
############### MySQL Configuration ###############
app.config.from_object('Config.DevelopmentConfig')
DB.init_db(app)  # DB 모듈 초기화


###################################################
############### Function Definition ###############
def save_object_in_session(obj, key):           # 객체 직렬화 및 세션에 저장
    session[key] = pickle.dumps(obj).hex()

def get_object_from_session(key):               # 세션에서 객체 역직렬화하여 추출
    return pickle.loads(bytes.fromhex(session[key]))


###################################################
###############   Route Definition  ###############
@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    form = ClassForm.RegisterForm()
    if form.validate_on_submit():      # if methods = 'POST'
        name = form.name.data
        email = form.email.data
        password = form.password.data
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        res = DB.insert_user(name, email, hashed_password)
        if res:
            flash('Your account has been created! You are now able to log in', 'success')
            return redirect(url_for('login'))
        else:
            return render_template('error.html', title='Error')

    return render_template('register.html', title='Register', form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    form = ClassForm.LoginForm()
    if form.validate_on_submit():      # if methods = 'POST'
        email = form.email.data
        password = form.password.data

        user = DB.get_user_by_email(email)
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
            session['user_id'] = user[0]
            session['user'] = pickle.dumps(user).hex()
            return redirect(url_for('dashboard'))
        else:
            flash("Login failed. Please check your email and password")
            return redirect(url_for('login'))

    return render_template('login.html', title='Login', form=form)

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        user2 = pickle.loads(bytes.fromhex(session['user']))
        
        user = DB.get_user_by_userid(user_id)
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
