from flask import Flask, request, make_response, jsonify, g, render_template, session, redirect, url_for
import jwt
import datetime
from functools import wraps
import mysql.connector
import secrets

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

# populate from database #

queries = {
    "get_all_employees" : "SELECT emp_id, emp_name, group_id FROM employee ORDER BY group_id",
    "get_all_users" : "SELECT emp_id, username, pass, access_lvl FROM users ORDER BY emp_id",
    "get_employee_groups" : "SELECT group_id, group_name FROM employee_group ORDER BY group_id"
    # or join on emp_id
}

def get_current_data(db):
    employees.clear()
    users.clear()
    groups.clear()
    passwords.clear()

    cur = db.cursor()
    try:
        cur.execute(queries["get_employee_groups"])
        for (group_id, group_name) in cur:
            groups.append({
                "group_id": str(group_id),
                "group_name": str(group_name)
            })
        cur.execute(queries["get_all_employees"])
        for (emp_id, emp_name, group_id) in cur:
            group = groups[group_id-1]["group_name"]
            employees.append({
                "employee_id": str(emp_id),
                "name" : str(emp_name),
                "employee_group_id": str(group_id),
                "employee_group": str(group),
                "username": "",
                "access_level": ""
            })
        cur.execute(queries["get_all_users"])
        for (emp_id, username, pwd, access_lvl) in cur:
            users.append({
                "employee_id": str(emp_id),
                "username": str(username),
                "password": str(pwd), # remove after the test stage
                "access_level": str(access_lvl)
            })
            passwords[username] = str(pwd)
            employees[emp_id-1]["username"] = str(username)
            employees[emp_id-1]["access_level"] = str(access_lvl)
    finally:
        cur.close()
    return(groups, employees, users, passwords)
   


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

# HR admin access #
"""
def add_user(name, username, pwd, group, lvl):
    return ""

def remove_user(name):
    #remove from users
    return ""

def remove_employee(name):
    #remove from users, then from employees
    return ""

def update_group(name):
    #change the employee group
    return ""

def update_access(username):
    #change access lvl
    return ""
"""

@app.route("/", methods=['GET', 'POST'])
def index():
    
    groups, employees, users, passwords = get_current_data(get_db()) 
    return render_template("index.html", groups=groups, employees=employees, users=users, user={"group_id": 4, "access_level": 1})

@app.route("/login", methods=['POST'])
#@verify_token
def login():
    session.pop('user', None)
    if request.form['username'] in passwords.keys(): #valid user
        if request.form['password'] == passwords[request.form['username']]: # valid password - check with hashing later
            token = jwt.encode({'user': request.form['username'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
            session['user'] = request.form['username']
            session['token'] = token #jsonify({'token': token.decode('UTF-8')})
            #find out group and access level
            group = access = ''
            for employee in employees:
                if employee["username"] == session['user']:
                    print(employee)
                    group = employee['employee_group_id']
                    access = employee['access_level']

            return render_template("index.html", groups=groups, employees=employees, users=users, user={"group_id": group, "access_level": access})
            
        return make_response('Wrong password!', 401)
    return make_response('Authentication failed!', 401)

@app.route("/logout", methods=['POST'])
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
