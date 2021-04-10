import mysql.connector

passwo = input("Enter your password for your SQL server: ")

myDB = mysql.connector.connect(
  host = "localhost",
  user = "root",
  password = passwo,
)
mycursor = myDB.cursor()
mycursor.execute("DROP DATABASE JIS_Database")
mycursor.execute("CREATE DATABASE JIS_Database")

myDB = mysql.connector.connect(
  host = "localhost",
  user = "root",
  password = passwo,
  database = "JIS_Database"
)

mycursor = myDB.cursor()
mycursor.execute("CREATE TABLE users (username VARCHAR(255) UNIQUE PRIMARY KEY NOT NULL, password VARCHAR(255))")
mycursor.execute("ALTER TABLE users ADD COLUMN name VARCHAR(255)")
mycursor.execute("ALTER TABLE users ADD COLUMN type VARCHAR(255)")
mycursor.execute("ALTER TABLE users ADD COLUMN money INT(255) DEFAULT -1")

sql = "INSERT INTO users (username, password, name, type) VALUES (%s, %s, %s, %s)"
val = [
  ('JISS_Admin', 'Admin2021', 'Registrar', 'reg')
]
mycursor.executemany(sql, val)
myDB.commit()

mycursor.execute("CREATE TABLE cases (CIN INT(255) UNIQUE PRIMARY KEY NOT NULL, defendentName VARCHAR(255))")
mycursor.execute("ALTER TABLE cases ADD COLUMN defendentAddress VARCHAR(255)")
mycursor.execute("ALTER TABLE cases ADD COLUMN crimeType VARCHAR(255)")
mycursor.execute("ALTER TABLE cases ADD COLUMN crimeDate VARCHAR(255)")
mycursor.execute("ALTER TABLE cases ADD COLUMN crimeLocation VARCHAR(255)")
mycursor.execute("ALTER TABLE cases ADD COLUMN officerName VARCHAR(255)")
mycursor.execute("ALTER TABLE cases ADD COLUMN arrestDate VARCHAR(255)")
mycursor.execute("ALTER TABLE cases ADD COLUMN judgeName VARCHAR(255)")
mycursor.execute("ALTER TABLE cases ADD COLUMN lawyerName VARCHAR(255)")
mycursor.execute("ALTER TABLE cases ADD COLUMN prosecutorName VARCHAR(255)")
mycursor.execute("ALTER TABLE cases ADD COLUMN startingDate VARCHAR(255)")
mycursor.execute("ALTER TABLE cases ADD COLUMN caseStatus VARCHAR(255)")
mycursor.execute("ALTER TABLE cases ADD COLUMN caseSummary VARCHAR(255)")
mycursor.execute("ALTER TABLE cases ADD COLUMN endDate VARCHAR(255)")
mycursor.execute("ALTER TABLE cases ADD COLUMN dateOfHearing VARCHAR(255)")
mycursor.execute("ALTER TABLE cases ADD COLUMN adjourments VARCHAR(255)")
mycursor.execute("ALTER TABLE cases ADD COLUMN hearings VARCHAR(255)")
mycursor.execute("ALTER TABLE cases ADD COLUMN caseJudgement VARCHAR(255)")

mycursor.execute("CREATE TABLE slots (date VARCHAR(255) UNIQUE PRIMARY KEY NOT NULL)")
mycursor.execute("ALTER TABLE slots ADD COLUMN slot1 BIT(1) DEFAULT 0")
mycursor.execute("ALTER TABLE slots ADD COLUMN slot2 BIT(1) DEFAULT 0")
mycursor.execute("ALTER TABLE slots ADD COLUMN slot3 BIT(1) DEFAULT 0")
mycursor.execute("ALTER TABLE slots ADD COLUMN slot4 BIT(1) DEFAULT 0")
mycursor.execute("ALTER TABLE slots ADD COLUMN slot5 BIT(1) DEFAULT 0")
mycursor.execute("ALTER TABLE slots ADD COLUMN slot6 BIT(1) DEFAULT 0")

print("Database created succesfully.")
print("Also, check out Database.py in Databases folder. Change the password in it to your password.")
print("There are two passwords in there btw.")
print("To create a few sample accounts and cases, run create.py file.")
print("That's all for now byeee")