from flask import Flask, request, make_response, jsonify, g, render_template, session, redirect, url_for
import jwt
import datetime
from functools import wraps
import mysql.connector
import secrets
from werkzeug.security import generate_password_hash, check_password_hash
#from util import *
from testutil import *

app = Flask(__name__)

# change for the real keys on deployment
app.secret_key = open('jwtRS256.key').read()  
app.public_key = open('jwtRS256.key.pub').read()
app.config['DB_USER'] = 'root'
app.config['DB_PWD'] = 'root'
app.config['DB'] = 'employee'
app.config['DB_HOST'] = 'localhost'


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


# AUTHENTICATION #

# user logged in
def verify_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        
        token = request.cookies.get('token')
        
        if not token:
            return jsonify({'message': 'No token provided!'}), 401
        try:
            result = jwt.decode(token, app.public_key, algorithms=['RS256'])
        except:
            return jsonify({'message': 'Invalid token!'}), 403

        return f(*args, **kwargs)
    return decorated

# user logged in and is admin
def verify_admin_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            return jsonify({'message': 'No token provided!'}), 401
        try:
            payload = jwt.decode(token, app.public_key, algorithms=['RS256'])
            
        except:
            return jsonify({'message': 'Invalid token!'}), 403

        if payload['auth'] > 1:
            return jsonify({'message': 'Insufficient authority level!'})

        return f(*args, **kwargs)
    return decorated
        
# front end routes #

@app.route("/")
def index():

    groups, employees, users, _ = get_current_data(get_db())
    if session.get('token') and request.cookies.get('token'):
        user = session.get('user')
        return render_template("index.html", groups=groups, employees=employees, users=users, user=user)
    return render_template('login.html', users=users)

    #resp = make_response(render_template("index.html", groups=groups, employees=employees, users=users, user={"group_id": 666, "access_level": 666}))
    #resp.set_cookie('token', '', max_age=-1)
    #return resp


@app.route("/login", methods=['GET', 'POST'])
def login():
    groups, employees, users, passwords = get_current_data(get_db())
    if request.method == 'POST':
        session.pop('token', None)
        session.pop('user', None)
        
        if request.form['username'] in passwords.keys(): #valid user
            if check_password_hash(passwords[request.form['username']], request.form['password']): # valid password
                group = auth = ''
                for employee in employees:
                    if employee["username"] == request.form['username']:
                        group = employee['employee_group_id']
                        auth = employee['access_level']
                        # set claims
                        payload = {
                            'role' : "employee" , 
                            'user': request.form['username'], 
                            'group' : group , 
                            'auth' : auth,  
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
                            }
                        token = jwt.encode(payload, app.secret_key, algorithm='RS256').decode('utf-8')
                        session['token'] = token
                        session['user'] = {"group_id": group, "access_level": auth}
                resp = make_response(render_template("index.html", groups=groups, employees=employees, users=users, user={"group_id": group, "access_level": auth}))
                resp.set_cookie('token', token)
                return resp
            return make_response('Wrong password!', 401)
        return make_response('Authentication failed!', 401)
    else:
        token = request.cookies.get('token')
        if not token:
            try:
                payload = session['token']
            except:
                return jsonify("Please log in!")
        else:
            try:
                payload = jwt.decode(token, app.secret_key, algorithm='RS256').decode('utf-8')
            except:
                return jsonify("No token provided!")
        return render_template("index.html", groups=groups, employees=employees, users=users, user={"group_id": payload['group'], "access_level": payload['auth']})


@app.route("/logout", methods=['POST'])
def logout():
    session.pop('token', None)
    session.pop('user', None)
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('token', '', max_age=0)
    return resp


@app.route('/delete_employee_form/<emp_id>', methods=['POST'])
@verify_admin_token
def delete_employee_form(emp_id):
    _ = remove_employee_by_id(get_db(), emp_id)
    return redirect(url_for('login'))


# API endpoints #

## Employees ##

@app.route('/employees', methods=['GET'])
@verify_token
def get_employees():
    employees, _ = get_employee_list(get_db())
    return jsonify({"Employees" : employees })

@app.route('/employees', methods=['POST'])
@verify_admin_token
def add_an_employee():
    got = request.get_json()
    if got : #got functional json
        resp = add_employee(get_db(), got['name'], got['group'])
    else:
        resp = add_employee(get_db(), request.form['name'], request.form['group'])
    return jsonify(resp)

@app.route('/employees/<emp_id>', methods=['GET'])
@verify_token
def get_one_employee(emp_id):
    resp = get_employee(get_db(), emp_id)
    return jsonify(resp)

@app.route('/employees/<emp_id>', methods=['PUT'])
@verify_admin_token
def edit_employee(emp_id):
    got = request.get_json()
    if got:
        name = got['name']
    else:
        name = request.forms['name']
    resp = update_employee(get_db(), emp_id, name)
    return jsonify(resp)

@app.route('/employees/<emp_id>', methods=['DELETE'])
@verify_admin_token
def delete_employee(emp_id):
    resp = remove_employee_by_id(get_db(), emp_id)
    return jsonify(resp)

## Users ##

@app.route('/users', methods=['GET'])
@verify_admin_token
def get_users():
    users = get_user_list(get_db())
    return jsonify({"Users" : users})

@app.route('/users', methods=['POST'])
@verify_admin_token
def create_user():
    got = request.get_json()    
    if got:
        id = got['ID']
        pwd = got['password']
        username = got['username']
        auth = got['auth']
    else:
        id = request.form['emp_id']
        pwd = request.form['password']
        username = request.form['username']
        auth = request.form['auth']

    
    if not check_employee(get_db(), id):
        return jsonify("No employee with ID " + id)

    saltypass = generate_password_hash(pwd, method='sha256', salt_length=10)
    resp = add_user(get_db(), id, username, saltypass, auth)

    return jsonify(resp)

# get all information about a user by employee ID
@app.route('/users/<emp_id>', methods=['GET'])
@verify_admin_token
def get_one_user(emp_id):
    resp = get_user(get_db(), emp_id)

    return jsonify(resp)

@app.route('/users/<emp_id>', methods=['PUT'])
@verify_admin_token
def edit_user(emp_id):
    got = request.get_json()
    resp = update_user(get_db(), emp_id, got['auth'])
    return jsonify(resp)

@app.route('/users/<emp_id>', methods=['DELETE'])
@verify_admin_token
def delete_user(emp_id):
    resp = remove_user_by_id(get_db(), emp_id)
    return jsonify(resp)

## Misc ##

@app.route('/groups')
@verify_token
def get_groups():
    groups = get_group_list(get_db())
    return jsonify({"Employee groups" : groups})

@app.route('/group_employees/<group_id>', methods=['GET'])
@verify_token
def get_by_groups(group_id):
    resp = get_employees_by_group(get_db(), group_id)
    return jsonify(resp)


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
