from flask import Flask, request, make_response, jsonify, g, render_template, session, redirect, url_for
import jwt
import datetime
from functools import wraps
import mysql.connector
import secrets
from util import *

app = Flask(__name__)

secret = secrets.token_urlsafe()

app.secret_key = secret
app.config['SECRET_KEY'] = secret
app.config['DB_USER'] = 'root'
app.config['DB_PWD'] = 'root'
app.config['DB'] = 'employee'
app.config['DB_HOST'] = 'localhost'


employees = []
users = []
groups = []
passwords = {}

def get_db():
    if not hasattr(g, "_database"):
        g._database = mysql.connector.connect(
            user = app.config['DB_USER'],
            host = app.config['DB_HOST'],
            password = app.config['DB_PWD'],
            database = app.config['DB']
        )
    return g._database

@app.teardown_appcontext

def teardown_db(error):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


# populates local structures with initial data from the database
def get_current_data(db):
   # employees.clear()
    #users.clear()
    #groups.clear()
    #passwords.clear()

    employees, passwords = get_employee_list(get_db())
    users = get_user_list(get_db())
    groups = get_group_list(get_db())

    return (groups, employees, users, passwords)

# AUTHENTICATION #
"""
def generate_auth_token():
    pass

# token verification
def verify_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message': 'No token provided!'}), 401
        try:
            result = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Invalid token!'}), 403

        return f(*args, **kwargs)
    return decorated

def correct_password(pwd):
    return True
    """

@app.route("/")
def index():

    groups, employees, users, passwords = get_current_data(get_db())
    return render_template("index.html", groups=groups, employees=employees, users=users, user={"group_id": 0, "access_level": 0})

# future endpoints

# GET - returns the list of all users, POST creates a new one
@app.route('/users', methods=['GET'])
def get_users():
    # token required, all auth lvls
    return jsonify(users)


@app.route('/users', methods=['POST'])
def create_user(emp_id):
    # protected: auth=0 can create admins, 1,2 - only users
    return ""


# get all information about a user by employee ID
@app.route('/users/<emp_id>', methods=['GET'])
def get_user(emp_id):
    # token required, auth lvls < 2
    return ""

@app.route('/users/<emp_id>', methods=['PUT'])
def edit_user(emp_id):
    # change user auth lvl, requires auth lvl 0
    return ""

@app.route('/users/<emp_id>', methods=['DELETE'])
def delete_user(emp_id):
    # remove existing user, requires auth lvl 0
    return ""

@app.route('/employees', methods=['GET'])
def get_emloyees():
    return jsonify(employees)

@app.route('/employees', methods=['POST'])
def add_emloyee():
    # auth = 0 or group = 1, auth = 1 (HR)
    return ""

@app.route('/employees/<emp_id>', methods=['GET'])
def get_emloyee(emp_id):
    return ""


@app.route('/employees/<emp_id>', methods=['PUT'])
def edit_employee(emp_id):
    # auth = 0 or group=1 auth=1
    return ""

@app.route('/employee/<emp_id>', methods=['DELETE'])
def delete_employee(emp_id):
    # remove existing user, requires auth lvl 0
    return ""

@app.route('/groups')
def get_groups():
    return jsonify(groups)

@app.route("/login", methods=['POST'])
#@verify_token
# sort out token auth, then replace session auth with it
def login():
    session.pop('user', None)
    if request.form['username'] in passwords.keys(): #valid user
        if request.form['password'] == passwords[request.form['username']]: # valid password - check with hashing later
            #token = jwt.encode({'user': request.form['username'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
            session['user'] = request.form['username']
            #session['token'] = token #jsonify({'token': token.decode('UTF-8')})
            #find out group and access level
            group = access = ''
            for employee in employees:
                if employee["username"] == session['user']:
                    group = employee['employee_group_id']
                    access = employee['access_level']

            return render_template("index.html", groups=groups, employees=employees, users=users, user={"group_id": group, "access_level": access})

        return make_response('Wrong password!', 401)
    return make_response('Authentication failed!', 401)


@app.route("/logout", methods=['POST'])
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


@app.route("/addEmployee", methods=["POST"])
def addEmployee():
    emp_name = request.form.get("emp_name")
    emp_group = request.form.get("emp_group")
    success = True
    db = get_db()
    cur =db.cursor()
    try:
        cur.execute(queries["add_employee"], emp_name, emp_group)
        cur.commit()
    except mysql.connector.Error as err:
        print("Error {}".format(err.msg))
        success = False
    finally:
        cur.close()

    if success is True:
        print("Successful")
        return render_template("")

    else:
        print("Failure")


@app.route("/update/employee")
def update(emp_id):

    pass

if __name__ == '__main__':
    app.run(debug=True)
