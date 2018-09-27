#Node Template
#Author: James Baffoni
#Date: 2018

#Script to create a basic API in node.js using the express generator as a starting point
#Assumes python and npm are already installed
#Place this file in desired project location (it will create project folder)
#Run with: sudo python node-template.py

import os
import mysql.connector
from mysql.connector import errorcode
import subprocess

project_name = ''
db_user = ''
db_password = ''
db_address = ''
db_name = ''
table_names = []
column_names = {}
cnx = None

def installPackages():

    #Install necessary packages for API to be launch-ready when script completes
    print("Installing packages...")
    os.system("cd " + project_name + " && sudo npm install")
    os.system("cd " + project_name + " && sudo npm install mysql")
    print("Finished.")

def getAll(table_name):

    #Create route for HTML 'get' to return all columns from all rows in the table
    return ("\n\n// Retrieve all" +
            "\nrouter.get('/', function(req, res) {" +
            "\n\n\tmc.query('SELECT * FROM " + table_name + "', function (error, results, fields) {" +
            "\n\t\tif( error) throw error;" +
            "\n\t\tres.send(results);" +
            "\n\t});" +
            "\n});"
        )

def getSingle(table_name):

    #Create route for HTML 'get' where first column matches given parameter
    column_name = column_names[table_name][0]
    return ("\n\n// Retrieve by first column" +
            "\nrouter.get('/:id', function(req, res) {" +
            "\n\tlet id = req.params.id;" +
            "\n\n\tmc.query('SELECT * FROM " + table_name + " WHERE " + column_name + "=?', id, function (error, results, fields) {" +
            "\n\t\tif( error) throw error;" +
            "\n\t\tres.send(results);" +
            "\n\t});" +
            "\n});"
        )

def getDeletes(table_name):

    #Create route for HTML 'delete' to delete row where first column matches given parameter
    column_name = column_names[table_name][0]
    return ("\n\n// Delete by first column" +
            "\nrouter.delete('/:id', function(req, res) {" +
            "\n\tlet id = req.params.id;" +
            "\n\n\tmc.query('DELETE FROM " + table_name + " WHERE " + column_name + "=?', id, function (error, results, fields) {" +
            "\n\t\tif( error) throw error;" +
            "\n\t\tres.send(results);" +
            "\n\t});" +
            "\n});"
        )

def getCreates(table_name):

    #Create route for HTML 'post' to create new row from body JSON
    first_column = column_names[table_name][0]
    stmt = ""
    for column_name in column_names[table_name]:
        stmt = stmt + column_name + ": " + column_name + ", "
        
    return ("// Create" +
            "\nrouter.post('/', function(req, res) {" +
            getLetStatements(table_name) +
            "\n\n\tmc.query('INSERT INTO " + table_name + " SET?', {" + stmt + "}, function (error, results, fields) {" +
            "\n\t\tif( error) throw error;" +
            "\n\t\tres.send(results);" +
            "\n\t});" +
            "\n});")

def getUpdates(table_name):

    #Create route for HTML 'put' to update existing row based on first column
    first_column = column_names[table_name][0]
    stmt = ""
    count = 0
    for column_name in column_names[table_name]:
        if count != 0:
            stmt = stmt + column_name + ": " + column_name + ", "
        count += 1
        
    return ("// Update" +
            "\nrouter.put('/', function(req, res) {" +
            getLetStatements(table_name) +
            "\n\n\tmc.query('UPDATE " + table_name + " SET ? WHERE " + first_column + "=?', [{" + stmt + "}, " + first_column + "], function (error, results, fields) {" +
            "\n\t\tif( error) throw error;" +
            "\n\t\tres.send(results);" +
            "\n\t});" +
            "\n});")

def getLetStatements(table_name):

    #Return assignment statements between HTML body and mysql query items
    toreturn = ""
    for column_name in column_names[table_name]:
        toreturn = toreturn + "\n\tlet " + column_name + " = req.body.data." + column_name + ";"
    return toreturn

def getTablesAndColumns():

    #Connect to database and link column names to table names for later use
    print("Reading Database...")
    cursor = cnx.cursor()
    cursor.execute("SHOW TABLES")
    global table_names
    tables = cursor.fetchall()
    for (table_name,) in tables:
        table_names.append(table_name)
        cursor.execute("SHOW columns FROM " + table_name)
        columnsToAdd = []
        columns = cursor.fetchall()
        for column in columns:
            columnsToAdd.append(column[0])
        column_names[table_name] = columnsToAdd
    

def createRoutes():

    #Create a route file for each table in specified database
    print("Creating routes...")
    print(len(table_names))
    for table_name in table_names:
        print("Creating " + table_name)
        f = open(project_name + "/routes/" + table_name + ".js","w+")
        f.write("var express = require('express');")
        f.write("\nvar router = express.Router();")
        f.write("\nvar mysql = require('mysql');")
        f.write("\nvar mc = mysql.createConnection({" +
                "\n\thost: '" + db_address + "'," +
                "\n\tuser: '" + db_user + "'," +
                "\n\tpassword: '" + db_password + "'," +
                "\n\tdatabase: '" + db_name + "'," +
                "\n});")
        f.write("\n\nmc.connect();")
        
        #Create basic CRUD functionality for API
        f.write(getAll(table_name) + "\n\n")
        f.write(getSingle(table_name) + "\n\n")
        f.write(getDeletes(table_name) + "\n\n")
        f.write(getCreates(table_name) + "\n\n")
        f.write(getUpdates(table_name) + "\n\n")
        f.write("\n\nmodule.exports = router;")
        f.close()
    createApp()

def getRouters():

    #Return routing statements for app.js file
    toreturn = ""
    for table_name in table_names:
        toreturn = toreturn + "\nvar " + table_name + "Router = require('./routes/" + table_name + "');"
    return toreturn
        
def getUseStatements():

    #Return use statements for app.js file
    toreturn = ""
    for table_name in table_names:
        toreturn = toreturn + "\napp.use('/" + table_name + "', " + table_name + "Router);"
    return toreturn

def createApp():

    #Write a new app.js file using all newly created routes and listen on port 4200
    print("Creating app...")
    f = open(project_name + "/app.js", "w+")
    f.write("var createError = require('http-errors');" +
            "\nvar express = require('express');" +
            "\nvar path = require('path');" +
            "\nvar cookieParser = require('cookie-parser');" +
            "\nvar logger = require('morgan');")
    f.write("\n\nvar indexRouter = require('./routes/index');")
    f.write(getRouters())
    f.write("\n\nvar app = express();" +
            "\n\n// view engine setup" +
            "\napp.set('views', path.join(__dirname, 'views'));" +
            "\napp.set('view engine', 'pug');" +
            "\n\napp.use(logger('dev'));" +
            "\napp.use(express.json());" +
            "\napp.use(express.urlencoded({ extended: false }));" +
            "\napp.use(cookieParser());" +
            "\napp.use(express.static(path.join(__dirname, 'public')));")
    f.write("\n\napp.use('/', indexRouter);")
    f.write(getUseStatements())
    f.write("\n\n// error handler" +
            "\napp.use(function(err, req, res, next) {" +
            "\n\t// set locals, only providing error in development" +
            "\n\tres.locals.message = err.message;" +
            "\n\tres.locals.error = req.app.get('env') === 'development' ? err : {};" +
            "\n\n\t// render the error page" +
            "\n\tres.status(err.status || 500);" +
            "\n\tres.render('error');" +
            "\n});" +
            "\n\nvar port = 4200;" +
            "\napp.listen(port, function(){" +
            "\n\t  console.log('hello world');" +
            "\n})" +
            "\n\nmodule.exports = app;")
    f.close()
    installPackages()

def expressGenerator():
    
    #Create an express project using the generator
    global project_name
    project_name = raw_input("What is the project name? ")
    print("Creating express project...")
    os.system("express --view=pug " + project_name)
    print("Modifying express project...")
    path = project_name + "/routes"
    
    #Destroy auto-generated files that will be re-written
    os.remove(path + "/users.js")
    os.remove(project_name + "/app.js")
    getTablesAndColumns()
    createRoutes()


def getDatabaseDetails():
    
    #Get database credentials from command line
    global db_user, db_password, db_address, db_name, cnx
    db_user = raw_input("What is the database username? ")
    db_password = raw_input("What is the database password? ")
    db_address = "127.0.0.1"
    input_address = raw_input("What is the database address? (Default: 127.0.0.1) ")
    if input_address: db_address = input_address
    db_name = raw_input("What is the database name? ")
    
    #Check mysql is running on 3306
    try:
      cnx = mysql.connector.connect(user=db_user,
                                    password=db_password,
                                    host=db_address,
                                    database=db_name
                                )
      print("Database connection OK")
      expressGenerator()
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
      else:
        print(err)

#start process
getDatabaseDetails()
