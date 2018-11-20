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


### Building

If your project needs some additional steps for the developer to build the
project after some code changes, state them here. for example:

```shell
./configure
make
make install
```

Here again you should state what actually happens when the code above gets
executed.

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

If the api is external, link to api documentation. If not describe your api including authentication methods as well as explaining all the endpoints with their required parameters.


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
