from flask import Flask
import mysql.connector


queries = {
    "get_all_employees" : "SELECT * FROM employee JOIN users ON employee.emp_id=users.emp_id ORDER BY employee.emp_id",
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
    "remove_employee": ["DELETE FROM users WHERE username=%s", "DELETE FROM employee WHERE emp_id=%s"], # remove the user too
    # add restrictions on username (or check that they work as expected)
    "update_employee" : "UPDATE employee SET emp_name=%s, group_id=%s", # needs some restrictions on what can or cannot be changed
    "update_access_level" : "UPDATE users SET access_lvl=%s WHERE username=%s " # on user

}

# employee management methods, must go to a separate file

def add_user(emp_id, username, password, access_level):
    return ""

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