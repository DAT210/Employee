from flask import Flask
import mysql.connector


queries = {
    "get_all_employees" : "SELECT * FROM employee LEFT JOIN users ON employee.emp_id=users.emp_id ORDER BY employee.emp_id",
    "get_all_users" : "SELECT emp_id, username, pass, access_lvl FROM users ORDER BY emp_id",
    "get_employee_groups" : "SELECT group_id, group_name FROM employee_group ORDER BY group_id",
    "get_employee_by_id" : "SELECT employee.*, users.username, users.access_lvl FROM employee JOIN users ON users.emp_id = employee.emp_id WHERE emp_id=%s",
     # collect info about the employee from employee table + username, access lvl from users table
    # or join on emp_id for get_all_users
    # add queries for insert / update employee
    "get_emp_id" : "SELECT emp_id FROM users WHERE username=%s",
    "add_employee" : "INSERT INTO employee (emp_name, group_id) VALUES (%s, %s)",
    "add_user" : "INSERT INTO users (emp_id, username, pass, access_lvl) VALUES(%s, %s, %s, %s)",
    # check for valid employee
    "remove_user_by_id": "DELETE FROM users WHERE emp_id=%s",
    "remove_employee_by_id": "DELETE FROM employee WHERE emp_id=%s",
    "remove_employee": ["DELETE FROM users WHERE username=%s", "DELETE FROM employee WHERE emp_id=%s"], # remove the user too
    # add restrictions on username (or check that they work as expected)
    "update_employee" : "UPDATE employee SET emp_name=%s WHERE emp_id=%s", # needs some restrictions on what can or cannot be changed
    "update_access_level" : "UPDATE users SET access_lvl=%s WHERE emp_id=%s " # on user

}

# TEMP for testing

def get_employee_list(db):
    the_list = []
    passwords = {}
    cur = db.cursor()
    try:        
        cur.execute(queries["get_all_employees"])
        for (emp_id, emp_name, group_id, dupl, username, password, access_lvl) in cur:
            the_list.append({
                "employee_id": emp_id,
                "name": emp_name,
                "employee_group_id": group_id,
                #"employee_group": groups[group_id],
                "username": username,
                "access_level": access_lvl
            })
            passwords[username] = password
    finally:
        cur.close()
    return(the_list, passwords)

def get_user_list(db):
    the_list = []
    cur = db.cursor()
    try:
        cur.execute(queries["get_all_users"])
        for (emp_id, username, pwd, access_lvl) in cur:
            the_list.append({
                "employee_id": emp_id,
                "username": username,
                "password": pwd, # remove after the test stage
                "access_level": access_lvl
            })
    finally:
        cur.close()
    return the_list

def get_group_list(db):
    the_list = {}
    cur = db.cursor()
    try:
        cur.execute(queries["get_employee_groups"])
        for (group_id, group_name) in cur:
            the_list[group_id] = group_name
    finally:
        cur.close()
    return the_list

def get_auth_list():
    pass


def check_employee(db, emp_id): 

    emp_list, _ = get_employee_list(db)
    for emp in emp_list:
        if emp['employee_id'] == emp_id:
            return True
    return False


def add_employee(db, name, group_id):
    cur = db.cursor()
    try:
        cur.execute(queries["add_employee"], (name, group_id))
        db.commit()
    except mysql.connector.Error as err:
        return "Error {}".format(err.msg)
    finally:
        cur.close()
    return "Created new employee!"


def add_user(db, emp_id, username, password, access_level):
    if not check_employee(db, emp_id):
        return "Cannot create a new user: no employee with that id"
    
    cur = db.cursor()
    try:
        cur.execute(queries["add_user"], (emp_id, username, password, access_level))
        db.commit()
    except mysql.connector.Error as err:
        print("Error {}".format(err.msg))
        return "Error {}".format(err.msg)
    finally:
        cur.close()

    return "User successfully created"

def get_user(db, emp_id):
    user_list = get_user_list(db)
    for user in user_list:
        if user['employee_id'] == int(emp_id):
            return user
    return "User not found"    

def get_employee(db, emp_id):
    emp_list, _ = get_employee_list(db)
    for emp in emp_list:
        if emp['employee_id'] == int(emp_id):
            return emp
    return "Employee not found"

def remove_employee_by_id(db, emp_id):
    if not check_employee:
        return "No such employee"
    emp = get_employee(db, emp_id)
    if emp['username']:
        remove_user_by_id(db, emp_id)
    cur = db.cursor()
    try:
        cur.execute(queries["remove_employee_by_id"] % emp_id)
        db.commit()
    except mysql.connector.Error as err:
        
        return ("Error {}".format(err.msg))
    finally:
        cur.close()
    return "Employee successfully deleted"

def remove_user_by_id(db, emp_id):
    cur = db.cursor()
    try:
        cur.execute(queries["remove_user_by_id"] % emp_id)
        db.commit()
    except mysql.connector.Error as err:
        print("Error {}".format(err.msg))
        return ("Error {}".format(err.msg))
    finally:
        cur.close()
    return "User successfully deleted!"

def update_user(db, emp_id, auth):
    cur = db.cursor()
    print("Auth now: ", auth)
    try:
        cur.execute(queries['update_access_level'], (auth, emp_id))
        db.commit()
    except mysql.connector.Error as err:
        return "Error {}".format(err.msg)
    finally:
        
        cur.close()
    return "User access level updated!"


def update_employee(db, emp_id, name):
    if not check_employee(db,emp_id):
        return "No employee with that name!"
    cur = db.cursor()
    try:
        cur.execute(queries['update_employee'], (name, emp_id))
        db.commit()
    except mysql.connector.Error as err:
        return "Error {}".format(err.msg)
    finally:
        
        cur.close()
    return "Employee ", name, " updated!"

# END OF TEMP





def remove_user(db, username):
    cur = db.cursor()
    try:
        cur.execute(queries["remove_user"], username)
        db.commit()
    except mysql.connector.Error as err:
        print("Error {}".format(err.msg))
    finally:
        cur.close()
    #remove from users - restrictions must be enforced by the db
    #check for error

def remove_employee(db, username):
    remove_user(db, username)
    emp_id = get_emp_id(db, username)
    cur = db.cursor()
    try:
        cur.execute(queries["remove_employee"], username)
        db.commit()
    except mysql.connector.Error as err:
        print("Error {}".format(err.msg))
    finally:
        cur.close()
    #remove from users, then from employees
    # get user, remove, then remove the employee
    return ""

def update_group(emp_id):
    #change the employee group
    return ""




def update_access(username):
    #change access lvl
    return ""

def get_emp_id(db, username):
    emp_id = []
    cur = db.cursor()
    try:
        cur.execute(queries["get_emp_id"], username)
        for emp_id in cur:
            emp_id.append({
                "employee_id": str(emp_id)
            })
    finally:
        cur.close()
    return(emp_id[0])