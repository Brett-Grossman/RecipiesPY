from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.accounts import accounts_class
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register',methods=['POST'])
def register():

    if not accounts_class.validate_account(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = accounts_class.save_account(data)
    session['accounts_id'] = id

    return redirect('/welcome')



@app.route('/login',methods=['POST'])
def login():
    accounts = accounts_class.get_by_email(request.form)

    if not accounts:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(accounts.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['accounts_id'] = accounts.id
    return redirect('/welcome')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')