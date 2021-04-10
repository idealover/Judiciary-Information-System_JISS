### Software Engineering

## JUDICIARY INFORMATION SYSTEM

# Overview

The Judicial Information System Software (JISS) is a program to be used by the judges, lawyers and 
registrars to improve the efficiency in handling the court cases. 
	-	JISS makes cases easy to handle for the registrars by making it easy to assign dates to each case, 	
		search for pending cases on a given date etc, rather than going through a lot of physical documents to do the same.
	-	System also provides information related to the cases which have been resolved so that the judges 
		can refer to them to improve their judgements and so that the lawyers can develop their line of arguments. 
	-	JISS aims to improve the case handling system of courts by replacing physical documents and papers,
		which can sometimes be tedious to handle.

# Contents

The main folder contains several parts:
	1)	Class Folder : It contains all the files related to classes used in the project.
		-	Adjourment.py contains Adjourment class
		-	Hearing.py contains Hearing class
		-	User.py contains User class
		-	Case.py contains Case class
		-	Judge.py contains Judge subclass of User class
		-	Lawyer.py contains Lawyer subclass of User class
		-	Registrar.py contains Registrar subclass of User class
	2)	Static Folder : It contains static files
		-	CSS : It contains CSS used in the Project
	3)	Templates Folder : It contains the html files or templates of all the webpages used in our project
	4)	Documents Folder : It contains important documents corresponding to our project :
			-	SRS document
			-	UML Diagrams
			-	Test Plan Report
			-	Test Cases
			-	Test Compliance Report
	5)	Database Folder : It contains file containing Database class and all its functionalities
	5)	app.py : This file contains all the backend work of our project using Flask and python
	6)	create.py : This file contains the initialization of our Databases, containing initial users
	7)	CreateDatabase.py : This file creates the database for our project, creating tables for users, cases and slots
				It creates a registrar itself, which acts as the Administrator

# Instructions (How to run) :

Follow the steps to run the Judiciary Information System :
	1)	First run the CreateDatabase.py file to create a database in your system
		-	It will ask for your password for your MySQL server
		-	Also, check out Database.py in Databases folder. Change the password in it to your password
		-	It should be run only once, at the starting
	2)	Then run the create.py file to initialize the database created with some pre written users
		-	It should be run only once, at the starting
	3)	Then run the app.py file to create a local development server running on localhost address, which one can get 
				from terminal itself
	4)	Copy the local host address and paste on any web browser, preferably chrome
	5)	It will show our website

# Pre Requirements :

Following pre requirements are must for this project :
	1)	Internet connection and any web browser
	2)	MySQL installed and activated, password of SQL server is required


END

# Contributors:

- Esha Manideep
- Amartya Mandal (Project Leader, GAWD)
- Divyansh Bhatia
