![Logo of the project](./src/employee_db/static/images/logo.png)

# Employee &middot; [![Build Status](https://img.shields.io/travis/npm/npm/latest.svg?style=flat-square)](https://travis-ci.org/npm/npm) [![npm](https://img.shields.io/npm/v/npm.svg?style=flat-square)](https://www.npmjs.com/package/npm) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com) [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://github.com/your/your-project/blob/master/LICENSE)
> Employee is a service for logging in employees based on access_level. Admins can add, edit and delete employees.

## Installing / Getting started

A quick introduction of the minimal setup you need to get a hello world up &
running.

```shell
commands here
```

Here you should say what actually happens when you execute the code above.

## Developing

### Built With
  * Python 3.6
  * MySQL 8.0
  * Flask 0.12
  * PyJWT 1.6.4

### Prerequisites
  * [Docker](https://www.docker.com/)
  * [GIT](https://git-scm.com/downloads)

### Setting up Dev
```shell
git clone https://github.com/DAT210/Employee.git
cd Employee/src/employee_db
docker-compose up --build
```

The container should be visible at:

http://192.168.99.100:5000/   (Docker-toolbox)

http://127.0.0.1:5000/ ("Normal" Docker)

What happens when you execute these commands:
1. Clones the project to your computer
2. Change directory into the project you just cloned
3. Docker installs requirements
4. Docker sets up the database
5. Docker runs the flask app


### Deploying / Publishing
give instructions on how to build and release a new version
In case there's some step you have to take that publishes this project to a
server, this is the right time to state it.

```shell
packagemanager deploy your-project -s server.com -u username -p password
```

And again you'd need to tell what the previous code actually does.

## Versioning

We can maybe use [SemVer](http://semver.org/) for versioning. For the versions available, see the [link to tags on this repository](/tags).


## Configuration

Here you should write what are all of the configurations a user can enter when
using the project.

## Tests

Describe and show how to run the tests with code examples.
Explain what these tests test and why.

```shell
Give an example
```

## Style guide

Explain your code style and show how to check it.

## Api Reference

[API Documentation](https://documenter.getpostman.com/view/5782719/RzZDhws9)

PARAMETERS:  
{employeeID} : ID of the employee, used for retrieving, updating, and deleting employee and user information. Type: integer  
{groupID} : ID of the employee group, used for retrieving a list of employees belonging to a certain group. Type: integer   

*Login as HR admin to get access to full employee API functionality.  
Username: hr_admin  
Password: pass*

#### POST

***http://<i></i>127.0.0.1:500/login***  
Log in with 'admin' username 'admin' password to get full access.   
Log in with 'pass' password to test user groups and authority levels.   
A browser cookie with a 'token' field will be added, token payload contains all the information on user, including name, ID, employee group and authority level. The token will expire in 30 minutes. Use the public key provided to decode the token.

Example request:  
*http://<i></i>127.0.0.1:5000/login*
```shell
curl --request POST \
  --url http://127.0.0.1:5000/login \
  --header 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
  --form username=admin \
  --form password=admin123
```  


***http://<i></i>127.0.0.1:5000/logout***  
Use to log out. Pops the session, replaces the token cookie with the one that will contain no viable token and expire instantly.


***http://<i></i>127.0.0.1:5000/employees***  
POST request to /employees with json formatted request.   
Required fields: { "name" : employee name string, "group" : employee group int}   
Required authority level: 0 or 1

Example request:  
*http://<i></i>127.0.0.1:5000/employees*
```shell
curl --request POST \
  --url http://127.0.0.1:5000/employees \
  --header 'Content-Type: application/json' \
  --data '{
	"name" : "Test API Employee",
	"group" : 22

}'
```


***http://<i></i>127.0.0.1:5000/users***  
POST to /users will create a new user if an employee with provided ID exists in the database.   
Required JSON fields: { "ID" : employee ID int, "username" : desired username string, "password" : desired password string, "auth" : authority level int }   
Will return error message if employee with given ID does not exist, if user for that employee is already created or if username is already taken.


#### GET
***http://<i></i>127.0.0.1:5000/groups***  
Will return the full list of all existing employee groups


***http://<i></i>127.0.0.1:5000/group-employees/{groupID}***   
To get the list of all employees belonging to provided group number.   
Parameters: groupID - integer

Example request:  
*http://<i></i>127.0.0.1:5000/group-employees/2*
```shell
curl --request GET \
  --url http://127.0.0.1:5000/group-employees/2
```

***http://<i></i>127.0.0.1:5000/employees***   
To get the list of all the existing employees in the database.


***http://<i></i>127.0.0.1:5000/employees/{employeeID}***   
Provide an employee ID to get information about a given employee, including name, group, username, and authority level.   
If a user for that employee is not yet created, returns null values in the corresponding fields.   
Returns an error status if non-existing employee requested.   
Parameters: employeeID - integer


***http://<i></i>127.0.0.1:5000/users***   
GET request to /users to get the list of all existing users with corresponding authority levels. Protected.   
Requires authority level 0 or 1.

Example request:  
*http://<i></i>127.0.0.1:5000/users*
```shell
curl --request GET \
  --url http://127.0.0.1:5000/users \
  --header 'Content-Type: application/json'
```

***http://<i></i>127.0.0.1:5000/users/{employeeID}***   
Provide an employee ID in GET request to /users/{employeeID} to get information about a specific user.   
Returns 500 status code if non-existing employee requested.   
Protected, requires authority level 0 or 1.


#### PUT
***http://<i></i>127.0.0.1:5000/employees/{employeeID}***   
PUT to employees/{employeeID} will update the name of an employee with provided ID if they exist, will return an error message if not.   
Required JSON fields: { "name" : new name string }  
Will return 204 status code on success.  
Protected: requires authority level 0 or 1.

Example request:  
*http://<i></i>127.0.0.1:5000/employees/10*
```shell
curl --request PUT \
  --url http://127.0.0.1:5000/employees/103 \
  --header 'Content-Type: application/json' \
  --data '{
	"name" : "New API Test Name"
}'
```

<br>
***http://<i></i>127.0.0.1:5000/users/{employeeID}***   
PUT to /users/{employeeID} will change authority level for user associated with the provided ID.   
If user or employee with that ID does not exist, will return status code 400.   
Will return status code 204 on success.  
Required fields: { "auth" : new authority level, integer }  
Parameters: employeeID - integer  
Protected: requires authority level 0 or 1


#### DELETE
***http://<i></i>127.0.0.1:5000/users/{employeeID}***   
DELETE to users/{employeeID} will delete the user associated with the employee with provided ID.  
Returns status code 204 on success.  
Protected: requires authority level 0 or 1.  
Parameters: employeeID: integer

Example request:  
*http://<i></i>127.0.0.1:5000/users/11*
```shell
curl --request DELETE \
  --url http://127.0.0.1:5000/users/11 \
  --header 'Content-Type: application/json'
```

<br>
***http://<i></i>127.0.0.1:5000/employees/{employeeID}***  
DELETE to employees/{employeeID} will delete the employee with provided ID.   
If a user associated with the employee exists in the database, it will be deleted first.  
Protected: requires authority level 0 or 1.  
Returns 204 on success.  
Parameters: {employeeID}: integer  

<br>
See [API Documentation](https://documenter.getpostman.com/view/5782719/RzZDhws9) for more request and response examples.

## Database
[MySQL 8.0](https://dev.mysql.com/downloads/workbench/)

The database has 5 tables:

access_level:
* access_lvl INT PRIMARY KEY
* access_code VARCHAR

employee_group:
* group_id INT PRIMARY KEY
* group_name VARCHAR

employee:
* emp_ip INT PRIMARY KEY
* emp_name VARCHAR
* group_id INT FOREIGN KEY

users:
* emp_ip INT FOREIGN KEY
* username VARCHAR PRIMARY KEY
* pass VARCHAR
* access_lvl INT FOREIGN KEY

timesheet:
* emp_id INT FOREIGN KEY
* work_date DATE PRIMARY KEY
* work_start TIME
* work_finish TIME
* clock_in TIME
* clock_out TIME


## Licensing

State what the license is and how to find the text version of the license.
