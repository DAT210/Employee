from flask import Flask, jsonify
import mysql.connector


queries = {
    "get_all_employees" : "SELECT * FROM employee LEFT JOIN users ON employee.emp_id=users.emp_id ORDER BY employee.emp_id",
    "get_all_users" : "SELECT emp_id, username, pass, access_lvl FROM users ORDER BY emp_id",
    "get_employee_groups" : "SELECT group_id, group_name FROM employee_group ORDER BY group_id",
    "get_employee_by_id" : "SELECT employee.*, users.username, users.access_lvl FROM employee JOIN users ON users.emp_id = employee.emp_id WHERE emp_id=%s",
    "get_emp_id" : "SELECT emp_id FROM users WHERE username=%s",
    "add_employee" : "INSERT INTO employee (emp_name, group_id) VALUES (%s, %s)",
    "add_user" : "INSERT INTO users (emp_id, username, pass, access_lvl) VALUES(%s, %s, %s, %s)",
    "remove_user_by_id": "DELETE FROM users WHERE emp_id=%s",
    "remove_employee_by_id": "DELETE FROM employee WHERE emp_id=%s",
    "remove_user" : "DELETE FROM users WHERE emp_id=%s",
    "remove_employee" : "DELETE FROM employee WHERE emp_id=%s",
    "update_employee" : "UPDATE employee SET emp_name=%s WHERE emp_id=%s",
    "update_access_level" : "UPDATE users SET access_lvl=%s WHERE emp_id=%s "
}

# fetch the initial data from database 

def get_current_data(db):
    
    employees, passwords = get_employee_list(db)
    users = get_user_list(db)
    groups = get_group_list(db)

    return (groups, employees, users, passwords)
    
# uses left join with users table, fetches passwords anyway. 
# Returns user:password dict for authorisation checks along with employee list
def get_employee_list(db):
    try:
        the_list = []
        passwords = {}
        cur = db.cursor()

        cur.execute(queries["get_all_employees"])
        for (emp_id, emp_name, group_id, _, username, password, access_lvl) in cur:
            the_list.append({
                "employee_id": emp_id,
                "name": emp_name,
                "employee_group_id": group_id,
                "username": username,
                "access_level": access_lvl
            })
            passwords[username] = password
        return(the_list, passwords)
    except:
        return jsonify("Internal server error"), 500
    finally:
        cur.close()


def get_user_list(db):    
    try:
        the_list = []
        cur = db.cursor()
        cur.execute(queries["get_all_users"])
        for (emp_id, username, pwd, access_lvl) in cur:
            the_list.append({
                "employee_id": emp_id,
                "username": username,
                "access_level": access_lvl
            })
        return the_list
    except:
        return jsonify("Internal server error"), 500
    finally:
        cur.close()
    
# Group code: group name dict
def get_group_list(db):
    try:
        the_list = {}
        cur = db.cursor()
    
        cur.execute(queries["get_employee_groups"])
        for (group_id, group_name) in cur:
            the_list[group_id] = group_name
        return the_list
    except:
        return jsonify("Internal server error"), 500
    finally:
        cur.close()

# to avoid attempting operations on non-existant employees or users
def check_employee(db, emp_id):
    emp_list, _ = get_employee_list(db)
    for emp in emp_list:
        if emp['employee_id'] == int(emp_id):
            return True
    return False

def check_user(db, emp_id):
    user_list = get_user_list(db)
    for user in user_list:
        if user['employee_id'] == int(emp_id):
            return True
    return False

# Employee methods #

def get_employee(db, emp_id):
    emp_list, _ = get_employee_list(db)
    for emp in emp_list:
        if emp['employee_id'] == int(emp_id):
            return emp
    return jsonify("No employee with that ID"), 400

def add_employee(db, name, group_id):
    cur = db.cursor()
    try:
        cur.execute(queries["add_employee"], (name, group_id))
        db.commit()
        return jsonify("New employee created"), 201
    except:
        return jsonify("Internal server error"), 500
    finally:
        cur.close()

def remove_employee_by_id(db, emp_id):
    if not check_employee(db, emp_id):
        return jsonify("No employee with that ID"), 400
    emp = get_employee(db, emp_id)
    if emp['username']:
        remove_user_by_id(db, emp_id)
    cur = db.cursor()
    try:
        cur.execute(queries["remove_employee_by_id"] % emp_id)
        db.commit()
        return jsonify("User succesfully deleted"), 204
    except:
        return jsonify("Internal server error"), 500
    finally:
        cur.close()


 #change the employee group
def update_employee(db, emp_id, name, group_id):
    cur = db.cursor()
    if not check_employee(db, emp_id):
        return jsonify("No employee with that ID"), 400
    try:
        cur.execute(queries['update_employee'], (name, group_id, emp_id))
        db.commit()
        return jsonify("Employee information updated"), 204
    except:
        return jsonify("Internal server error"), 500
    finally:
        cur.close()

# change the eployee name
def update_employee_name(db, emp_id, name):
    if not check_employee(db,emp_id):
        return jsonify("No employee with that ID"), 400
    cur = db.cursor()
    try:
        cur.execute(queries['update_employee'], (name, emp_id))
        db.commit()
        return jsonify("Employee name updated"), 204
    except:
        return jsonify("Internal server error"), 500
    finally:
        
        cur.close()


def get_employees_by_group(db, group_id):
    resp = []
    employees, _ = get_employee_list(db)
    for emp in employees:
        if int(emp['employee_group_id']) == int(group_id):
            resp.append(emp)
    if not resp:
        return jsonify("No employees in that group"), 400
    return jsonify(resp), 200
    

# User methods #

# it is only allowed to create users for existing employees
def add_user(db, emp_id, username, password, access_level):
    cur = db.cursor()
    if not check_employee(db, emp_id):
        return jsonify("Cannot create a new user: no employee with that id"), 400
    try:
        cur.execute(queries["add_user"], (emp_id, username, password, access_level))
        db.commit()
        return jsonify("New user created"), 201
    except:
        return jsonify("Internal server error"), 500
    finally:
        cur.close()
    
# gets user by ID
def get_user(db, emp_id):
    user_list = get_user_list(db)
    for user in user_list:
        if user['employee_id'] == int(emp_id):
            return user
    return jsonify("No user with that ID"), 400

"""
def remove_user(db, emp_id):
    cur = db.cursor()
    try:
        cur.execute(queries["remove_user"], emp_id)
        db.commit()
        return jsonify("User deleted"), 204
    except:
        return jsonify("Internal server error"), 500
    finally:
        cur.close()
        """
    

def remove_user_by_id(db, emp_id):
    if not check_employee(db, emp_id):
        return jsonify("No employee with that ID"), 400
    cur = db.cursor()
    try:
        cur.execute(queries["remove_user_by_id"] % emp_id)
        db.commit()
        return jsonify("User successfully deleted"), 204
    except:
        return jsonify("Internal server error"), 500
    finally:
        cur.close()

#change access lvl
def update_access(db, emp_id, access_lvl):
    
    if not check_employee(db, emp_id):
        return jsonify("No user with that ID"), 400
    if not check_user(db, emp_id):
        return jsonify("No active user associated with that employee"), 400
    cur = db.cursor()
    try:
        cur.execute(queries['update_access_level'], (access_lvl, emp_id))
        db.commit()
        return jsonify("User authority level updated"), 204
    except:
        return jsonify("Internal server error"), 500
    finally:
        cur.close()

