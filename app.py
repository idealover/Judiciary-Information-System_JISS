#Imports
from flask import Flask, render_template,url_for,request,redirect,abort,flash
from flask_sqlalchemy import SQLAlchemy
from Databases import *
from Class import Judge,Registrar,Lawyer
from datetime import datetime,date

# Today's date
today = date.today()

#define the flask app
app = Flask(__name__)

#global variables required for various functions
global curr_user,currcaselist,currcase

#connect to the database
database = Database()

#initially define all of them to None
currcaselist = None
currcase = None
curr_user = None

#function to verify the curruser based on username and type
def verifyuser(username,typ):
    global curr_user,currcaselist
    #check if the user is none or not logged in
    if curr_user == None or curr_user.isloggedin() == False:
        curr_user = None #set curruser to None if not logged in
        return False
    #check the username and type
    elif curr_user.getUsername() != username or curr_user.getType() != typ:
        return False

    return True


#route for home page
@app.route('/',methods = ['POST','GET'])
def home():
    global curruser
    #redirect to homepage if some user is logged in
    if curr_user!= None:
        if curr_user.getType()=="reg":
            return redirect(url_for('reghome',username = curr_user.getUsername()))
        elif curr_user.getType() == "jud":
            return redirect(url_for('judhome',username = curr_user.getUsername()))
        elif curr_user.getType() == "law":
            return redirect(url_for('lawhome',username = curr_user.getUsername()))
    if request.method == 'POST':
        return redirect(url_for('login')) #when someone clicks on login button
    #display the homepage
    return render_template('HomePage.html') #display the homepage

#route for login
@app.route('/login',methods=['POST','GET'])
def login():
    global curr_user,currcaselist #get global variables
    #redirect to home page if logged in
    if curr_user!= None:
        #check for the type and redirect to respective pages
        if curr_user.getType()=="reg":
            return redirect(url_for('reghome',username = curr_user.getUsername()))
        elif curr_user.getType() == "jud":
            return redirect(url_for('judhome',username = curr_user.getUsername()))
        elif curr_user.getType() == "law":
            return redirect(url_for('lawhome',username = curr_user.getUsername()))

    #check for input from the page
    if request.method == 'POST':
        temp = request.form.to_dict() #convert to dict. We will be using this more often from now on
        #formatting input to get type, username, password from the dict
        x = formatuserinput(temp) #check this function out in formatfuncs.py in Databases folder

        #check for the username and password
        if database.checkUser(x[1],x[2]): #if exists
            #check for type and redirect
            if database.getTypeOfUser(x[1]) == x[0]: #check the type of user
                if x[0]=="jud":
                    #get relevant details
                    x.append(database.getNameOfUser(x[1]))
                    curr_user = Judge(x) #creating curruser
                    return redirect(url_for('judhome',username=x[1]))

                elif x[0] == "law":
                    x.append(database.getNameOfUser(x[1]))
                    x.append(database.getMoneyOfUser(x[1])) #get money too for lawyer
                    curr_user = Lawyer(x) #create curruser
                    return redirect(url_for('lawhome',username=x[1])) #redirect

                else: 
                    x.append(database.getNameOfUser(x[1]))
                    curr_user = Registrar(x) #creating curruser
                    return redirect(url_for('reghome',username=x[1]))
            
            #if not same type. Remember username is unique through out all types
            else:
                return render_template('login.html',error=True) #return with error = True
        #if not valid user
        else:
            return render_template('login.html',error=True) #return with error = True
    
    return render_template('login.html') #render normal template otherwise


#homepage for judges
@app.route('/jud/<username>',methods = ['POST','GET'])
def judhome(username):
    #verify the credentials
    global curr_user,currcaselist
    if not verifyuser(username,"jud"):
        return render_template('403.html')

    #error messages for different scenarios
    msg1 = "Please enter an input"
    msg2 = "Please enter an Integer for CIN."
    msg3 = "There is no case with the given CIN number. Please try again."
    
    #if there is input from the page
    if request.method == 'POST':

        #logging out the user
        if request.form['submit_button'] == "Log Out":
            curr_user = None #set curr_user to None because we are logging out
            return redirect(url_for('home')) #redirect to home page

        #if request is for search
        elif request.form['submit_button'] == "Search":
            temp = request.form.to_dict() #converting to dict

            #if both inputs are empty
            if temp['cin']=="" and temp['key'] == "":
                return render_template('judge.html',message = curr_user.getName(),error = msg1) #print error 1

            #if cin is not empty
            elif temp['cin']!="":

                #try to convert it to integer
                try:
                    int(temp['cin'])
                #if error
                except ValueError:
                    return render_template('judge.html',message = curr_user.getName(),error = msg2) #print error 2

                #check if there is a case with that cin. CINs are assigned serially
                if int(temp['cin']) < 1 or int(temp['cin']) >= database.getNextCIN():
                    return render_template('judge.html',message = curr_user.getName(),error = msg3) #if no case, print error 3

                #if no errors, redirect to viewing of the respective cin inputted
                return redirect(url_for('view_case',CIN = int(temp['cin']))) #redirect to view_case to view the case


            #if key is not emtpy and cin is empty
            elif temp['key']!="":
                #get the list of cases from the database
                lis = database.getCaseByKeyword(temp['key'])
                #get the global currcaselist to the list returned above
                currcaselist = lis

                #redirect to the viewcaselist to view the list
                return redirect(url_for('viewcaselist'))

    #when there are no inputs, just show the homepage
    return render_template('judge.html',message = curr_user.getName())

#home page for lawyers
@app.route('/law/<username>',methods = ['POST','GET'])
def lawhome(username):
    #verification of credentials
    global curr_user,currcaselist
    if not verifyuser(username,"law"):
        return render_template('403.html')

    #error messages for various scenarios
    msg1 = "Please enter an input"
    msg2 = "Please enter an Integer for CIN."
    msg3 = "There is no case with the given CIN number. Please try again."
    msg4 = "You don't have enough money to view any case. Please consult Registrar to add money to your wallet."

    #if there is some request from the page
    if request.method == 'POST':

        #if request is to log out, log out
        if request.form['submit_button'] == "Log Out":
            curr_user = None
            return redirect(url_for('home'))

        #to search
        elif request.form['submit_button'] == "Search":
            temp = request.form.to_dict() #convert input to dict form 

            #initially check the money in the lawyer's wallet. Cannot view a case if money is less than 5
            if curr_user.getMoney()<5:
                return render_template('lawyer.html',message = curr_user.getName(),money = curr_user.getMoney(),error = msg4) #print message 4

            #if both inputs are empty
            if temp['cin']=="" and temp['key'] == "":
                return render_template('lawyer.html',message = curr_user.getName(),money = curr_user.getMoney(),error = msg1) #print message 1

            #if cin is not empty
            elif temp['cin']!="":

                #check for various errors as done in judge homepage
                try:
                    int(temp['cin'])
                except ValueError:
                    return render_template('lawyer.html',message = curr_user.getName(),money = curr_user.getMoney(),error = msg2)
                if int(temp['cin']) < 1 or int(temp['cin']) >= database.getNextCIN():
                    return render_template('lawyer.html',message = curr_user.getName(),money = curr_user.getMoney(),error = msg3)
                
                #if no errors, subtract money from lawyer's wallet, in the curruser and the database.
                curr_user.subtractMoney()
                database.subtractMoney(curr_user.getUsername())
                #redirect to viewing the case
                return redirect(url_for('view_case',CIN = int(temp['cin'])))

            #if only key is not left empty
            elif temp['key']!="":
                lis = database.getCaseByKeyword(temp['key'])
                currcaselist = lis

                #no money is charged to just view the list of cases.redirect to viewcaselist
                return redirect(url_for('viewcaselist'))

    #no input, render normal home page with all the details
    return render_template('lawyer.html',message = curr_user.getName(),money = curr_user.getMoney())

#home page for registrar
@app.route('/reg/<username>/',methods = ['POST','GET'])
def reghome(username):
    #verify credentials
    global curr_user,currcaselist
    if not verifyuser(username,"reg"):
        return render_template('403.html')

    #if there is a request from the page
    if request.method == 'POST':

        #for each of the pages, a variables "username" should be passed.
        #it is passed in all the redirects

        #if logout request
        if request.form['submit_button'] == "Log Out":
            curr_user = None #set curruser to none
            return redirect(url_for('home')) #return to home

        #if adduser button is clicked
        elif request.form['submit_button'] == "Add User":
            return redirect(url_for('signup',username = username)) #redirect to signup page

        #if delete user button is lcicked
        elif request.form['submit_button'] == "Delete User":
            return redirect(url_for('deleteuser',username = username)) #redirect to deleteuser page

        #if addmoney button is clicked
        elif request.form['submit_button'] == "Add Money":
            return redirect(url_for('addmoney',username=username)) #redirect to addmoney page

        #view case details button is clicked
        elif request.form['submit_button'] == "View Case Details":
            return redirect(url_for('viewcasedetails',username = username)) #redirect to viewcasedetails page

        #if get case status button is clicked
        elif request.form['submit_button'] == "Get Case Status":
            return redirect(url_for('getcasestatus',username = username)) #redirect to getcasestatus page

        #if add case is clicked
        elif request.form['submit_button'] == "Add Case":
            return redirect(url_for('addcase',username = username)) #redirect to addcase page

        #if update case is clicked
        elif request.form['submit_button'] == "Update Case":
            return redirect(url_for('updatecase',username = username)) #redirect to update case page
            

    #if no input display the homepage with necessary details
    return render_template('registrar.html',message = curr_user.getName())

#page for updating cases
@app.route('/reg/<username>/updatecase',methods = ['POST','GET'])
def updatecase(username):
    #verify credentials of the user
    global curr_user,currcaselist,currcase
    if not verifyuser(username,"reg"):
        return render_template('403.html')

    #various error messages for various scenarios
    msg1 = "Please Enter a valid CIN."
    msg2 = "Hearing summary cannot be left empty."
    msg3 = "Adjournment Reason cannot be left empty."
    msg4 = "You can't add hearing summary to this case right now."
    msg5 = "You cannot Update a closed Case."
    msg6 = "Judgement cannot be left empty."
    msg7 = "Case Summary cannot be left empty."
    msg8 = "Case is already closed."

    #if there is a request from the page
    if request.method == 'POST':
        temp = request.form.to_dict() #convert the input to a dict

        #if input is given on hearing tab
        if temp['tab'] == "hear":

            #try to convert into integer
            try:
                int(temp['cin'])
            #if error
            except ValueError:
                return render_template('updatecase.html',error = msg1) #display error 1

            #check if there is a case for this cin
            if int(temp['cin'])<1 or int(temp['cin'])>=database.getNextCIN():
                return render_template('updatecase.html',error = msg1) #if no case display error 1 again

            #if summary is left empty
            if temp['summary'] == "":
                return render_template('updatecase.html',error = msg2) #error 2
            
            #get the case details and store in currcase, global variable
            currcase = database.getCaseByCIN(temp['cin'])

            #if the case is closed, it can't be modified
            if currcase[12] == "Closed":
                return render_template('updatecase.html',error = msg5) #display error message

            #verify if the next hearing date of the case is before today. Registrar can't add summary if next hearing is after today
            if database.verifyDate(currcase[15])==False or database.verifyDatebeforeToday(currcase[15]): #verify if case can be edited

                #if yes, get todays date as a string
                todaydate = today.strftime("%d") + "/"+ today.strftime("%m") + "/" + today.strftime("%Y")
                currcase[17].append([todaydate,temp['summary']]) #add the hearing to the case
                
                #set the current hearing date to none, as registrar just entered a hearing summary
                currcase[15] = "" 

                #redirect to choose a slot
                return redirect(url_for('updatecase_slot',username = username))
            
            else:  #if registrar can't edit this case right now
                return render_template('updatecase.html',error = msg4) #show error 4

        #if input is give in adjournment place
        elif temp['tab'] == "adj":

            #all verifications are almost similar to hearings tab
            try:
                int(temp['cin1'])
            except ValueError:
                return render_template('updatecase.html',error = msg1)

            if int(temp['cin1'])<1 or int(temp['cin1'])>=database.getNextCIN():
                return render_template('updatecase.html',error = msg1)

            #reason canot be empty
            if temp['reason'] == "":
                return render_template('updatecase.html',error = msg3)
            
            #get case details
            currcase = database.getCaseByCIN(temp['cin1'])

            if currcase[12] == "Closed": #cant edit if closed
                return render_template('updatecase.html',error = msg5)

            #no date verification is done for adjourning a case
            todaydate = today.strftime("%d") + "/"+ today.strftime("%m") + "/" + today.strftime("%Y")
            currcase[16].append([todaydate,temp['reason']]) #update the adjournments
            currcase[15] = ""  #set current hearing date to none

            return redirect(url_for('updatecase_slot',username = username)) #redirect to choosing a slot

        #if input is given in close a case tab
        elif temp['tab'] == "clo":

            #normal verifications of cin
            try:
                int(temp['cin2'])
            except ValueError:
                return render_template('updatecase.html',error = msg1)
            
            if int(temp['cin2'])<1 or int(temp['cin2'])>=database.getNextCIN():
                return render_template('updatecase.html',error = msg1)

            #judgement tab cannot be empty
            if temp['judgement'] == "":
                return render_template('updatecase.html',error = msg6)

            #case summary tab cannot be empty
            if temp['casesummary'] == "":
                return render_template('updatecase.html',error = msg7)

            #get case details
            currcase = database.getCaseByCIN(temp['cin2'])

            #cannot close a case that's already closed
            if currcase[12] == "Closed":
                return render_template('updatecase.html',error = msg8)

            #get today's date for end date
            todaydate = today.strftime("%d") + "/"+ today.strftime("%m") + "/" + today.strftime("%Y")

            #modifying details
            currcase[14] = todaydate #end date
            currcase[12] = "Closed" #status
            currcase[18] = temp['judgement'] #judgement
            currcase[13] = temp['casesummary'] #summary
            currcase[15] = "None" #set hearing date to none

            #update the case in database
            database.updateCase(currcase)
            currcase = None #set currcase global variable to none

            #display success message upon success
            return render_template('updatecase.html',success = "Succesfully Closed the Case!")

    #display normal page if no input
    return render_template('updatecase.html')

#choose slot interface for update case with no date chosen
@app.route('/reg/<username>/updatecase/chooseslot',methods = ['POST','GET'])
def updatecase_slot(username):

    #credentials verification of the user
    global curr_user,currcaselist,currcase
    url = request.referrer 

    #additional verification is done. This page can only be accessed through redirects
    if url == None or currcase == None or not verifyuser(username,"reg"):
        return render_template('403.html')

    #error message 1
    msg1 = "Please enter a valid Date. Date can't be before today."

    #if some request is made
    if request.method == 'POST':
        temp = request.form.to_dict() #convert to dict
        
        #check if date is not before today
        if database.verifyDatefromToday(temp['date']) == False:
            return render_template('Slot.html',error = msg1) #display msg1

        #if valid date, redirect to choose slot with a date chosen
        #format date format. It is changed from dd/mm/yyyy format to dd-mm-yyyy format
        return redirect(url_for('updatecase_slotwithdate',username = username, date = formatdatetodiff(temp['date']))) 

    #if no request display normal template
    return render_template('Slot.html')

#choose a slot for update case with a slot chosen
@app.route('/reg/<username>/updatecase/chooseslot/<date>',methods = ['POST','GET'])
def updatecase_slotwithdate(username,date):
    #similar verification as above, cannot access without redirect
    global curr_user,currcaselist,currcase
    url = request.referrer
    if url == None or currcase == None or not verifyuser(username,"reg"):
        return render_template('403.html')

    #error message
    msg1 = "Please enter a valid Date. Date shouldn't be before today."

    #if request, another date is inputted or a slot is chosen
    if request.method == 'POST':
        temp = request.form.to_dict() #convert to dict

        #when some other date is enterred
        if temp['date'] != "":

            #verify the date
            if database.verifyDatefromToday(temp['date']) == False:
                return render_template('Slot.html',error = msg1) #just show error message

            #redirect to the same url with different date, format date too
            return redirect(url_for('updatecase_slotwithdate',username = username, date = formatdatetodiff(temp['date'])))
        
        #no date input, so a slot is chosen
        date = formatdifftodate(date) #get date back to dd/mm/yyyy format
        slot = int(temp['submit_button'][10:]) #get the slot chosen from the name of the button
        currcase[15] = date #set the hearing date of the curr case to selected date
        database.updateSlots(date,slot) #update the slot database about the slot selection
        database.updateCase(currcase) #update the case database with the currcase 
        currcase = None #set currcase to none

        #after updating, return to update case url with a success message
        return render_template('updatecase.html',success = "Successfully Updated the Case!")

    # if no request, show the slots available on the right
    date = formatdifftodate(date) #change the format of date back
    x = database.getEmptySlots(date) #get empty slot from database
    finalx = [] #final list saying which slots are free
    for i in range(6):
        if i in x:
            finalx.append(True)
        else:
            finalx.append(False)

    #show the slots of the chosen date
    return render_template('Slot.html',i = finalx,date = formatdatetodiff(date))

#add case webpage
@app.route('/reg/<username>/addcase',methods = ['POST','GET'])
def addcase(username):
    #credential verification
    global curr_user,currcaselist,currcase
    if not verifyuser(username,"reg"):
        return render_template('403.html')

    #error messages
    msg1 = "Please Fill all the fields. None of the fields can be empty."
    msg2 = "Please enter a valid Crime Date."
    msg3 = "Please enter a valid Arrest Date."

    #if a request from the page
    if request.method == 'POST':
        temp = request.form.to_dict() #format the input to dict 
        temp = list(temp.values()) #get the list of the values. We differentiate using the index of the input

        #check if any input is empty
        for x in temp:
            if x == "":
                return render_template('addcase.html',error = msg1) #show error 1

        #check if crimedate is before today
        if database.verifyDatebeforeToday(temp[3]) == False:
            return render_template('addcase.html',error = msg2) #if not before today show msg 2

        #check if arrest date is before today
        if database.verifyDatebeforeToday(temp[6]) == False:
            return render_template('addcase.html',error = msg3) #if not valid show msg 3

        #get todays date as string
        todaydate = today.strftime("%d") + "/"+ today.strftime("%m") + "/" + today.strftime("%Y")

        #add other parts of the new case
        temp.append(todaydate) #start date of the case
        temp.append("Pending") #Case just added
        for _ in range(3):
            temp.append("") #for case summary, end date, Date of Hearing(for now)
        temp.append([]) #no adjournments initially
        temp.append([]) #no hearings initially
        temp.append("") #case judgement
        temp.insert(0,database.getNextCIN()) #set CIN to next available CIN from the database

        #set currcase to the case.
        currcase = temp

        #if everything goes smoothly, proceed on to choosing a slot for first hearing date
        return redirect(url_for('addcase_slot',username = username))

    #if no input, show normal page
    return render_template('addcase.html')

#webpage for choosing slot in addcase with no date chosen initially. Same as the one for update case
@app.route('/reg/<username>/addcase/chooseslot',methods = ['POST','GET'])
def addcase_slot(username):
    global curr_user,currcaselist,currcase
    url = request.referrer
    if url == None or currcase == None or not verifyuser(username,"reg"):
        return render_template('403.html')

    msg1 = "Please enter a valid Date. Date shouldn't be before today."

    if request.method == 'POST':
        temp = request.form.to_dict()
        
        if database.verifyDatefromToday(temp['date']) == False:
            return render_template('Slot.html',error = msg1)

        return redirect(url_for('addcase_slotwithdate',username = username, date = formatdatetodiff(temp['date'])))

    return render_template('Slot.html')

#webpage for choosing slot in addcase with date chosen. Almost same as the one for update case
@app.route('/reg/<username>/addcase/chooseslot/<date>',methods = ['POST','GET'])
def addcase_slotwithdate(username,date):
    global curr_user,currcaselist,currcase
    url = request.referrer
    if url == None or currcase == None or not verifyuser(username,"reg"):
        return render_template('403.html')

    msg1 = "Please enter a valid Date. Date shouldn't be before today."

    if request.method == 'POST':
        temp = request.form.to_dict()

        if temp['date'] != "":
            if database.verifyDatefromToday(temp['date']) == False:
                return render_template('Slot.html',error = msg1)

            return redirect(url_for('addcase_slotwithdate',username = username, date = temp['date']))
        
        date = formatdifftodate(date)
        slot = int(temp['submit_button'][10:])
        currcase[15] = date
        database.updateSlots(date,slot)
        database.addCase(currcase) #here we add the case rather than update the case. Rest is same as updatecase chooseslot
        currcase = None

        return render_template('addcase.html',success = "Successfully Added the Case!")

    date = formatdifftodate(date)
    x = database.getEmptySlots(date)
    finalx = []
    for i in range(6):
        if i in x:
            finalx.append(True)
        else:
            finalx.append(False)

    return render_template('Slot.html',i = finalx,date = formatdatetodiff(date))


#signup page for reg
@app.route('/reg/<username>/signup',methods = ['POST','GET'])
def signup(username):
    #verify credentials
    global curr_user,currcaselist
    if not verifyuser(username,"reg"):
        return render_template('403.html')

    msg1 = "Password Length should be atleast 8 digits. Please try again."

    #if request
    if request.method == 'POST':
        temp = request.form.to_dict() #to dictionary
        x = formatsingininput(temp) #format the user based on judge/lawyer input

        #User format: type, username, password, name

        if x[0] == "":
            return render_template('signup.html',error = "Username cannot be empty. Please try again.")

        #check if username already exists
        if database.ifUserExists(x[0]):
            return render_template('signup.html',error = "Username already exists. Please try again.") #show relevant message
        
        #if adding a judge
        if x[3]=="jud":

            #check for password strength
            if len(x[1])<8: 
                return render_template('signup.html',error = msg1) #show message 1 if not strong enough password

            #create user in database if no errors
            database.createUser(x[0],x[1],x[2],x[3])

        #if lawyer input
        else:
            if len(x[1])<8: #password strength check
                return render_template('signup.html',error = msg1)
            database.createUser(x[0],x[1],x[2],x[3],"0") #another extra column for money. Initially set to 0

        #if no errors and succesfully added the user, display success message
        return render_template('signup.html',success = "Successfully Added the user!")

    #if no input just show the template
    return render_template('signup.html')

#webpage for delete user
@app.route('/reg/<username>/delete',methods = ['POST','GET'])
def deleteuser(username):
    #credential verification
    global curr_user,currcaselist
    if not verifyuser(username,"reg"):
        return render_template('403.html')

    #if request
    if request.method == 'POST':
        temp = request.form.to_dict() #to dictionary

        #error message
        msg1 = "No user with the given username exists. Please try again."
        msg2 = "Username cannot be empty. Please try again."
        msg3 = "No Judge found with the given username."
        msg4 = "No lawyer found with the given username."
        
        #if input entered in judge tab
        if temp['tab'] == "jud":

            if temp['username'] == "":
                return render_template('delete.html',error = msg2) #show error message if doesn't

            #check if user exists
            if database.ifUserExists(temp['username']) == False:
                return render_template('delete.html',error = msg1) #show error message if doesn't

            if database.getTypeOfUser(temp['username']) != "jud":
                return render_template('delete.html',error = msg3) #show error message if doesn't

            #delete user if user exists
            database.deleteUser(temp['username'])

        #input entered in lawyer tab, similar logic as for judge
        else :

            if temp['username1'] == "":
                return render_template('delete.html',error = msg2) #show error message if doesn't

            if database.ifUserExists(temp['username1']) == False:
                return render_template('delete.html',error = msg1)

            if database.getTypeOfUser(temp['username1']) != "law":
                return render_template('delete.html',error = msg4) #show error message if doesn't

            database.deleteUser(temp['username1'])

        #show success message if successfully deleted
        return render_template('delete.html',success = "Deleted Succesfully!")
    
    #just show delete template if no request
    return render_template('delete.html')

#webpage for add money
@app.route('/reg/<username>/addmoney',methods = ['POST','GET'])
def addmoney(username):
    #credentials verification
    global curr_user,currcaselist
    if not verifyuser(username,"reg"):
        return render_template('403.html')

    #if request
    if request.method == 'POST':
        temp = request.form.to_dict() #to dict

        #error messages
        msg1 = "No lawyer with the given username exists. Please try again."
        msg2 = "Please enter a valid integer for money. It should be between 1 and 1000.(Both Inclusive)"

        #check if user exists at all
        if database.ifUserExists(temp['name'])==False:
            return render_template('money.html',error = msg1) #error 1

        #check if the user is of lawyer type, if the user exists at all
        elif database.getTypeOfUser(temp['name']) != "law":
            return render_template('money.html',error = msg1) #still error 1
        
        #a lawyer exists
        else:
            #try to convert the input into string
            try:
                int(temp['amt'])
            #if error, show error
            except ValueError:
                return render_template('money.html',error = msg2) #error 2

            #check if the entered amount is between 1 and 1000
            if int(temp['amt'])<1 or int(temp['amt'])>1000:
                return render_template('money.html',error=msg2) #error 2

        #add money to the user if no errors, update in the database
        database.AddMoneyToUser(temp['name'],int(temp['amt']))

        #show success message if succesfully added money
        return render_template('money.html',success = "Successfully added Money!!")

    #show normal webpage if no request
    return render_template('money.html')

#webpage to view case details
@app.route('/reg/<username>/viewcasedetails',methods = ['POST','GET'])
def viewcasedetails(username):
    #verify credentials
    global curr_user,currcaselist
    if not verifyuser(username,"reg"):
        return render_template('403.html')

    #if rquest
    if request.method == 'POST':

        #asked for pending cases
        if request.form['submit_button'] == "Pending Cases":
            lis = database.getCaseByStatus("Pending") #get list from database
            currcaselist = lis #set currcaselist to pending 
            return redirect(url_for('viewcaselist')) #redirect to view the list

        #asked for upcoming cases
        elif request.form['submit_button'] == "Upcoming Cases":
            return redirect(url_for('getUpcomingCases',username=username)) #redirect to upcoming cases webpage

        #asked for resolved cases
        elif request.form['submit_button'] == "Resolved Cases":
            return redirect(url_for('getResolvedCases',username = username)) #redirect to resolved cases webpage

    #if no request, show normal webpage
    return render_template('viewcase.html')

#webpage for getting upcoming cases
@app.route('/reg/<username>/getUpcomingCases',methods = ['POST','GET'])
def getUpcomingCases(username):
    #credential verification
    global curr_user,currcaselist
    if not verifyuser(username,"reg"):
        return render_template('403.html')

    #if request
    if request.method == 'POST':
        temp = request.form.to_dict() #convert to dict

        #verify the date inputted. It should be after today
        if database.verifyDatefromToday(temp['date']) == False:
            return render_template('Upcoming.html',error = "Please enter a Valid date.") #show error

        #if valid date, get cases from datbase
        currcaselist = database.getCaseByDateOfHearing(temp['date']) #set global variable currcaselist = the list from database

        #redirect to viewcaselist
        return redirect(url_for('viewcaselist'))

    #if no request, show normal webpage
    return render_template('Upcoming.html')

#webpage for getResolved cases
@app.route('/reg/<username>/getResolvedCases',methods = ['POST','GET'])
def getResolvedCases(username):
    #verify credentials
    global curr_user,currcaselist
    if not verifyuser(username,"reg"):
        return render_template('403.html')

    #if request
    if request.method == 'POST':
        temp = request.form.to_dict() #to dict

        #verify both the dates. No restrictions on dates put here, both can be before or after today.
        if database.verifyDate(temp['frdate']) == False or database.verifyDate(temp['todate']) == False:
            return render_template('Resolved.html',error = "Please enter valid dates.") #if the strings are not dates, show error

        #if no error, get caselist from database
        currcaselist = database.getAllCasesBetweenTwoDates(temp['frdate'],temp['todate']) #set global currcaselist to the list from database

        #redirect to viewcaselist
        return redirect(url_for('viewcaselist'))

    #if no request, show normal page
    return render_template('Resolved.html')

#webpage to get the status of the case
@app.route('/reg/<username>/getcasestatus',methods = ['POST','GET'])
def getcasestatus(username):
    #verify credentials
    global curr_user,currcaselist
    if not verifyuser(username,"reg"):
        return render_template('403.html')

    #various error messages
    msg1 = "Please enter an input"
    msg2 = "Please enter an Integer for CIN."
    msg3 = "There is no case with the given CIN number. Please try again."

    #if request
    if request.method == 'POST':
        temp = request.form.to_dict() #to dict

        #if CIN is left empty
        if temp['cin'] == "":
            return render_template('status.html',error = msg1) #show msg 1

        #else
        else:
            #try to convert to integer
            try:
                int(temp['cin'])
            #if error
            except ValueError:
                return render_template('status.html',error = msg2) #show message 2


            #check if there is a case with given cin
            if int(temp['cin'])<1 or int(temp['cin']) >= database.getNextCIN():
                return render_template('status.html',error = msg3) #if not, show message 3

            #no error then show the status of the case in green
            return render_template('status.html',success = database.getCaseStatus(int(temp['cin'])))

    #no input, just show the normal webpage
    return render_template('status.html')

#webpage to view the case
@app.route('/view_case/<int:CIN>/',methods = ['POST','GET'])
def view_case(CIN):
    #verify credentials and also another condition. This page cannot be accessed without a redirect
    global curr_user,currcaselist
    url = request.referrer
    if url == None or curr_user == None:
        return render_template('403.html')

    #if one of the hearing or adjournments button is clicked
    if request.method == 'POST':

        #if hearings is clicked
        if request.form['submit_button'] == "View Hearings":
            return redirect(url_for('view_hearings',CIN = CIN)) #redirect to view hearings for the given CIN

        #if adjournments is clicked
        elif request.form['submit_button'] == "View Adjournments":
            return redirect(url_for('view_adjournments',CIN=CIN)) #redirect to view adjournments for the given CIN

    #if no input, then just show the case with the given CIN
    temp = database.getCaseByCIN(CIN) #get form the database
    #display it 
    return render_template('casedet.html',message = temp)

#adjournments page for a given case
@app.route('/view_case/<int:CIN>/view_adjournments')
def view_adjournments(CIN):
    #verify credentials and also another condition. This page cannot be accessed without a redirect
    global curr_user,currcaselist
    url = request.referrer
    if url == None or curr_user == None:
        return render_template('403.html')

    #get the case from the CIN
    temp = database.getCaseByCIN(CIN)

    #just display the adjournments of that case
    return render_template('adjournment.html',message = temp[16])

#hearings page for a given case
@app.route('/view_case/<int:CIN>/view_hearings')
def view_hearings(CIN):
    #verify credentials and also another condition. This page cannot be accessed without a redirect
    global curr_user,currcaselist
    url = request.referrer
    if url == None or curr_user == None:
        return render_template('403.html')

    #get the case with given CIN from the database
    temp = database.getCaseByCIN(CIN)

    #just display the hearings of that case
    return render_template('hearing.html',message = temp[17])

#viewcaselist
@app.route('/viewcaselist/',methods = ['POST','GET'])
def viewcaselist():
    #verify credentials and also another condition. This page cannot be accessed without a redirect
    global curr_user,currcaselist
    url = request.referrer
    if url == None or curr_user == None:
        return render_template('403.html')

    #error message
    msg1 = "You don't have enough balance to view a case. Please try again."
    msg2 = "No cases found."

    if currcaselist == []:
        return render_template('caselist.html',message = currcaselist,error = msg2)

    #if some button is clicked
    if request.method == 'POST':

        #get the CIN of the case requested based on the value of button
        CIN = request.form['submit_button'][11:]
        CIN = int(CIN) 
        
        #extra checking for lawyer
        if curr_user.getType() == "law":

            #if money in wallet is less than 5
            if curr_user.getMoney()<5:
                #cannot view case
                return render_template('caselist.html',message = currcaselist, error = msg1) #show error message 1

            #if enough money, money is cut for viewing a case
            curr_user.subtractMoney() #cut from curruser
            database.subtractMoney(curr_user.getUsername()) #cut from database

        #redirect to view the case chosen
        return redirect(url_for('view_case',CIN = CIN))

    #if no input, display the list 
    return render_template('caselist.html',message = currcaselist)


if __name__=="__main__":
    app.run(debug=True)