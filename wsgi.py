import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.controllers.Admin import create_admin, create_staff
from App.controllers.Staff import get_all_staff
from App.database import db, get_migrate
from App.models import *
from App.main import create_app
from App.controllers import *


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

@user_cli.command("create_admin", help="Creates an admin")
@click.argument("username", default="jane")
@click.argument("password", default="doe")
def create_admin_command(username, password):
    create_admin(username, password)
    print(f'{username} created!')

@user_cli.command("create_staff", help="Creates a staff")
@click.argument("firstName", default="jane")
@click.argument("lastName", default="doe")
def create_staff_command(firstName, lastName):
    create_staff(firstName, lastName)
    print(f'{firstName} created!')

@user_cli.command("list_staff", help="Lists staff members in the database")
@click.argument("format", default="string")
def list_staff_command(format):
    if format == 'string':
        print(get_all_staff())

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)