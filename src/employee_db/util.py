from flask import Flask
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
    "update_employee" : "UPDATE employee SET emp_name=%s, group_id=%s WHERE emp_id=%s",
    "update_access_level" : "UPDATE users SET access_lvl=%s WHERE emp_id=%s "
}


def get_current_data(db):

    employees, passwords = get_employee_list(db)
    users = get_user_list(db)
    groups = get_group_list(db)

    return (groups, employees, users, passwords)


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


def check_employee(db, emp_id):
    emp_list, _ = get_employee_list(db)
    for emp in emp_list:
        if emp['employee_id'] == int(emp_id):
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
    return "Employee created"


def add_user(db, emp_id, username, password, access_level):
    cur = db.cursor()
    if not check_employee(db, emp_id):
        return "Cannot create a new user: no employee with that id"
    try:
        cur.execute(queries["add_user"], (emp_id, username, password, access_level))
        db.commit()
    except mysql.connector.Error as err:
        print("Error {}".format(err.msg))
    finally:
        cur.close()
    return "User created"


def get_employee(db, emp_id):
    emp_list = get_employee_list(db)
    for emp in emp_list:
        if emp['employee_id'] == int(emp_id):
            return emp
    return "Employee not found"

def get_user(db, emp_id):
    user_list = get_user_list(db)
    for user in user_list:
        if user['employee_id'] == int(emp_id):
            return user
    return "User not found" 

def remove_user(db, emp_id):
    cur = db.cursor()
    try:
        cur.execute(queries["remove_user"], emp_id)
        db.commit()
    except mysql.connector.Error as err:
        print("Error {}".format(err.msg))
    finally:
        cur.close()
    return "User deleted"

def remove_employee_by_id(db, emp_id):
    if not check_employee(db, emp_id):
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

def remove_employee(db, emp_id):
    if not check_employee(db, emp_id):
        return "No such employee"
    emp = get_employee(db, emp_id)
    if emp['username']:
        remove_user(db, emp_id)
    cur = db.cursor()
    try:
        cur.execute(queries["remove_employee"], emp_id)
        db.commit()
    except mysql.connector.Error as err:
        print("Error {}".format(err.msg))
    finally:
        cur.close()
    return "Employee deleted"


def update_employee(db, emp_id, name, group_id):
    #change the employee group
    cur = db.cursor()
    if not check_employee(db, emp_id):
        return "No such employee"
    try:
        cur.execute(queries['update_employee'], (name, group_id, emp_id))
        db.commit()
    except mysql.connector.Error as err:
        return "Error {}".format(err.msg)
    finally:
        cur.close()
    return "Employee ", name, " updated"


def update_employee_name(db, emp_id, name):
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



def update_access(db, emp_id, access_lvl):
    #change access lvl
    cur = db.cursor()
    try:
        cur.execute(queries['update_access_level'], (access_lvl, emp_id))
        db.commit()
    except mysql.connector.Error as err:
        return "Error {}".format(err.msg)
    finally:
        cur.close()
    return "User access level updated"

def get_employees_by_group(db, group_id):
    resp = []
    employees, _ = get_employee_list(db)
    for emp in employees:
        if emp['employee_group_id'] == int(group_id):
            resp.append(emp)
    return resp