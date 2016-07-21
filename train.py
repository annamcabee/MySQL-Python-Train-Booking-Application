import pymysql

try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *
import datetime
import tkinter.messagebox as messagebox

import random


class Reservation:

    def __init__(self):
        self.bwin=Toplevel()
        self.bwin.title("Train System New User Registration")
        self.register(self.bwin)
        self.bwin.withdraw()
        self.loginpage(win)

    def connect(self):
        try:
            conn = pymysql.connect(host='academic-mysql.cc.gatech.edu', passwd='3XrNmXqK', user='cs4400_Team_74', db='cs4400_Team_74')
            return(conn)
        except:
            messagebox.showwarning(title="Excuse Me",message="Please check your internet connection")



    def loginpage(self,win):
        self.win=win
        self.labeluser=Label(self.win,text="Username")
        self.labelpass=Label(self.win,text="Password")
        self.entry1=Entry(self.win,width=30)
        bullet = "\u2022"
        self.entry2=Entry(self.win,show=bullet,width=30)
        self.labeluser.grid(row=0,column=0)
        self.labelpass.grid(row=1,column=0)
        self.entry1.grid(row=0,column=1)
        self.entry2.grid(row=1,column=1)
        self.button1=Button(self.win,text="Login",command=self.LoginCheck)
        self.button2=Button(self.win,text="Register",command=self.unhide)
        self.button1.grid(row=3,column=0)
        self.button2.grid(row=3,column=1)


    def unhide(self):
        self.win.withdraw()
        self.bwin.deiconify()

    def register(self,bwin):
        self.reguser=Label(bwin,text="Username")
        self.email=Label(bwin,text="Email Address")
        self.password=Label(bwin,text="Password")
        self.confirm=Label(bwin,text="Confirm Password")
        self.createbutton=Button(bwin,text="Create",command=self.confirmregistration)
        self.reguser.grid(row=1,column=0)
        self.email.grid(row=2,column=0)
        self.password.grid(row=3,column=0)
        self.confirm.grid(row=4,column=0)
        self.createbutton.grid(row=5,column=0,sticky=E+W,columnspan=2)
        self.userentry=Entry(bwin,width=30)
        self.emailentry=Entry(bwin,width=30)
        self.passentry=Entry(bwin,width=30)
        self.confirmpassentry=Entry(bwin,width=30)
        self.userentry.grid(row=1,column=1)
        self.emailentry.grid(row=2,column=1)
        self.passentry.grid(row=3,column=1)
        self.confirmpassentry.grid(row=4,column=1)
        self.titlelabel=Label(bwin,text="NEW USER REGISTRATION")
        self.titlelabel.grid(row=0,column=0,sticky=E+W,columnspan=2)
        #Need to pull from entry with info in new window




    def LoginCheck(self):
        #try:
            user=self.entry1.get()
            self.username = user
            psswrd=self.entry2.get()
            print("Beginning login check")
            print(user)
            print(psswrd)
            #Needs to check database for login info
            #If not error and retry
            #db = pymysql.connect(host='academic-mysql.cc.gatech.edu', passwd='3XrNmXqK', user='cs4400_Team_74', db='cs4400_Team_74')
            db = self.connect()

            c = db.cursor()
            sql = "SELECT USERNAME, Password FROM USER WHERE Username = %s AND Password = %s"
            loginResult = c.execute(sql, (user, psswrd))
            c = db.cursor()
            sql = "SELECT * from USER natural JOIN MANAGER WHERE Username = %s and Password = %s"
            manager= c.execute(sql,(user,psswrd))
            print(loginResult)
            print(manager)
            if loginResult == 0 and manager ==0:
                messagebox.showwarning("Invalid Username/Password", "You have entered an unrecognizable username/password combination. Please try again.")
            elif manager!=0:
                self.win.withdraw()
                self.managerfunction()
            else:
                self.win.withdraw()
                self.choose()
            return None
       # except:
            messagebox.showwarning("Invalid Username/Password", "You have entered an unrecognizable username/password combination. Please try again.")
        



    def confirmregistration(self):
        print("Hello")
        #Confirm email unique
        self.username = self.userentry.get()
        #a = self.entry1.get()
        #print(a)
        self.username = self.username

        password = self.passentry.get()
        if self.username=="":
            messagebox.showwarning("Invalid Username","Please enter a username")
            return
        if "@" not in self.emailentry.get():
            messagebox.showwarning("Invalid Email","Please enter a valid Email")
            return

        self.password = password
        db = self.connect()

        print(password)
        #db = pymysql.connect(host='academic-mysql.cc.gatech.edu', passwd='3XrNmXqK', user='cs4400_Team_74', db='cs4400_Team_74')
        #db = self.connect()
        # check is username exists
        c = db.cursor()

        sqlCheck = "SELECT USERNAME FROM USER WHERE Username = %s"
        registerCheck = c.execute(sqlCheck, (self.username))

        sqlCheck2 = "SELECT EMAIL FROM CUSTOMER WHERE Email = %s"
        emailCheck = c.execute(sqlCheck2, (self.emailcheck))

        sqlCheck3 = "SELECT EMAIL FROM MANAGER WHERE Email = %s"
        emailCheck2 = c.execute(sqlCheck2, (self.emailcheck))

        print(emailCheck)
        if emailCheck == 1:
            messagebox.showwarning("Invalid Email","This email already has an account")
        elif emailCheck2 == 1:
            messagebox.showwarning("Invalid Email","This email already has an account")

        print(sqlCheck)
        print(registerCheck)
        registerSQL = None
        if registerCheck == 1:
            messagebox.showwarning("Invalid Username", "This username is already taken")
        elif password != self.confirmpassentry.get() or password=="":
                messagebox.showwarning("Invalid Password", "Passwords must match")
        else:
            registerSQL = "INSERT INTO USER VALUES (%s,%s)"
            c.execute(registerSQL, (self.username, password))
            if "admin" not in self.username:
                print("Creating customer")
                createCustomer = "INSERT INTO CUSTOMER VALUES (%s, %s, %s)"
                isStudent = False
                if ".edu" in self.emailentry.get():
                    isStudent = True
                    print("Student discount")
                c.execute(createCustomer, (self.username, self.emailentry.get(), isStudent))
            else:
                print("Creating manager")
                createManager = "INSERT INTO CUSTOMER VALUES (%s)"
                c.execute(createManager, (username))
            self.bwin.withdraw()
            self.choose()
        #self.choose(win)
            #self.choose(win)
        #print(registerSQL)



    def managerfunction(self):
        self.manwin=Toplevel()
        self.mantitle=Label(self.manwin,text="Choose Functionality").grid(row=0,column=0)
        self.revbutton=Button(self.manwin,text="View Revenue Report",command=self.revreport).grid(row=1,column=0)
        self.routereport=Button(self.manwin,text="View Popular Route Report",command=self.routereport).grid(row=2,column=0)
        self.logoutman=Button(self.manwin,text="Log Out",command=self.logout1).grid(row=3,column=0)


    def logout1(self):
        self.manwin.withdraw()
        self.entry1.delete(0,'end')
        self.entry2.delete(0,'end')
        self.win.deiconify()
        
    def revreport(self):
        self.manwin.withdraw()
        self.revwin=Toplevel()
        self.viewrevlabel=Label(self.revwin,text="View Revenue Report").grid(row=0,column=0,columnspan=2)
        self.monthlabel=Label(self.revwin,text="Month").grid(row=1,column=0)
        self.revlabel=Label(self.revwin,text="Revenue").grid(row=1,column=1)
        #Need last 3 month revenue report
        db = self.connect()
        c = db.cursor()
        today = datetime.datetime.now()
        yr = today.year
        month = today.month
        if month - 3 == -2:
            first = 10
            sec = 11
            third = 12
            year1 = yr - 1
            year2 = yr - 1
            year3 = yr - 1
        elif month - 3 == -1:
            first = 11
            sec = 12
            third = 1
            year1 = yr - 1
            year2 = yr - 1
            year3 = yr
        elif month - 3 == 0:
            first = 12
            sec = 1
            third = 2
            year1 = yr - 1
            year2 = yr
            year3 = yr
        else:
            first = month - 3
            sec = month - 2
            third = month - 1
            year1 = yr
            year2 = yr
            year3 = yr
        if first == 1 or first == 3 or first == 5 or first == 7 or first == 8 or first == 10 or first == 12:
            day1 = 31
        elif first == 2:
            day1 = 28
        else:
            day1 = 30
        if sec == 1 or sec == 3 or sec == 5 or sec == 7 or sec == 8 or sec == 10 or sec == 12:
            day2 = 31
        elif sec == 2:
            day2 = 28
        else:
            day2 = 30
        if third == 1 or third == 3 or third == 5 or third == 7 or third == 8 or third == 10 or third == 12:
            day3 = 31
        elif third == 2:
            day3 = 28
        else:
            day3 = 30
        if first == 1:
            m1 = "January"
            m2 = "February"
            m3 = "March"
        elif first == 2:
            m1 = "February"
            m2 = "March"
            m3 = "April"
        elif first == 3:
            m1 = "March"
            m2 = "April"
            m3 = "May"
        elif first == 4:
            m1 = "April"
            m2 = "May"
            m3 = "June"
        elif first == 5:
            m1 = "May"
            m2 = "June"
            m3 = "July"
        elif first == 6:
            m1 = "June"
            m2 = "July"
            m3 = "August"
        elif first == 7:
            m1 = "July"
            m2 = "August"
            m3 = "September"
        elif first == 8:
            m1 = "August"
            m2 = "September"
            m3 = "October"
        elif first == 9:
            m1 = "September"
            m2 = "October"
            m3 = "November"
        elif first == 10:
            m1 = "October"
            m2 = "November"
            m3 = "December"
        elif first == 11:
            m1 = "November"
            m2 = "December"
            m3 = "January"
        elif first == 12:
            m1 = "December"
            m2 = "January"
            m3 = "February"
        sql = "Select TrainNumber, Class, FirstClassPrice, SecondClassPrice from TRAIN_ROUTE Natural Join RESERVES Where DepartureDate Between %s and %s GROUP BY TrainNumber, Class"
        start = datetime.date(year1, first, 1)
        end = datetime.date(year1, first, day1)
        c.execute(sql, (start,end))
        total = 0
        #Label(self.viewWin, text = "{}".format(m1)).grid(row=1, column=0)
        for record in c:
            tr = record[0]
            print(tr)
            cl = record[1]
            fc = record[2]
            sc = record[3]
            if cl == 'First':
                total = total + fc
            elif cl == 'Second':
                total = total + sc
        Label(self.revwin, text = m1).grid(row = 2, column = 0)
        Label(self.revwin, text = "${}".format(total)).grid(row = 2, column = 1)
        total = 0
        sql = "Select TrainNumber, Class, FirstClassPrice, SecondClassPrice from TRAIN_ROUTE Natural Join RESERVES Where DepartureDate Between %s and %s GROUP BY TrainNumber, Class"
        start = datetime.date(year2, sec, 1)
        end = datetime.date(year2, sec, day2)
        c.execute(sql, (start,end))
        #Label(self.viewWin, text = "{}".format(m2)).grid(row=count, column=0)
        for record in c:
            tr = record[0]
            cl = record[1]
            fc = record[2]
            sc = record[3]
            if cl == 'First':
                total = total + fc
            elif cl == 'Second':
                total = total + sc
        Label(self.revwin, text = m2).grid(row = 3, column = 0)
        Label(self.revwin, text = "${}".format(total)).grid(row = 3, column = 1)
        total = 0
        sql = "Select TrainNumber, Class, FirstClassPrice, SecondClassPrice from TRAIN_ROUTE Natural Join RESERVES Where DepartureDate Between %s and %s GROUP BY TrainNumber, Class"
        start = datetime.date(year3, third, 1)
        end = datetime.date(year3, third, day3)
        c.execute(sql, (start,end))
        #Label(self.viewWin, text = "{}".format(m3)).grid(row=count, column=0)
        for record in c:
            tr = record[0]
            cl = record[1]
            fc = record[2]
            sc = record[3]
            if cl == 'First':
                total = total + fc
            elif cl == 'Second':
                total = total + sc
        Label(self.revwin, text = m3).grid(row = 4, column = 0)
        Label(self.revwin, text = "${}".format(total)).grid(row = 4, column = 1)
        total = 0
        db.close()
        
        self.backtoman1=Button(self.revwin,text="Back",command=self.backtoman1).grid(row=7,column=0,columnspan=2)



    def backtoman1(self):
        self.revwin.withdraw()
        self.manwin.deiconify()

    def routereport(self):
        print("Finding route report")
        self.manwin.withdraw()
        self.viewWin = Toplevel()
        Label(self.viewWin, text = "Month").grid()
        Label(self.viewWin, text = "Location").grid(row=0, column=1)
        Label(self.viewWin, text = "Total # of Reservations").grid(row=0, column=2)
        db = self.connect()
        c = db.cursor()
        today = datetime.datetime.now()
        yr = today.year
        month = today.month
        if month - 3 == -2:
            first = 10
            sec = 11
            third = 12
            year1 = yr - 1
            year2 = yr - 1
            year3 = yr - 1
        elif month - 3 == -1:
            first = 11
            sec = 12
            third = 1
            year1 = yr - 1
            year2 = yr - 1
            year3 = yr
        elif month - 3 == 0:
            first = 12
            sec = 1
            third = 2
            year1 = yr - 1
            year2 = yr
            year3 = yr
        else:
            first = month - 3
            sec = month - 2
            third = month - 1
            year1 = yr
            year2 = yr
            year3 = yr
        if first == 1 or first == 3 or first == 5 or first == 7 or first == 8 or first == 10 or first == 12:
            day1 = 31
        elif first == 2:
            day1 = 28
        else:
            day1 = 30
        if sec == 1 or sec == 3 or sec == 5 or sec == 7 or sec == 8 or sec == 10 or sec == 12:
            day2 = 31
        elif sec == 2:
            day2 = 28
        else:
            day2 = 30
        if third == 1 or third == 3 or third == 5 or third == 7 or third == 8 or third == 10 or third == 12:
            day3 = 31
        elif third == 2:
            day3 = 28
        else:
            day3 = 30
        if first == 1:
            m1 = "January"
            m2 = "February"
            m3 = "March"
        elif first == 2:
            m1 = "February"
            m2 = "March"
            m3 = "April"
        elif first == 3:
            m1 = "March"
            m2 = "April"
            m3 = "May"
        elif first == 4:
            m1 = "April"
            m2 = "May"
            m3 = "June"
        elif first == 5:
            m1 = "May"
            m2 = "June"
            m3 = "July"
        elif first == 6:
            m1 = "June"
            m2 = "July"
            m3 = "August"
        elif first == 7:
            m1 = "July"
            m2 = "August"
            m3 = "September"
        elif first == 8:
            m1 = "August"
            m2 = "September"
            m3 = "October"
        elif first == 9:
            m1 = "September"
            m2 = "October"
            m3 = "November"
        elif first == 10:
            m1 = "October"
            m2 = "November"
            m3 = "December"
        elif first == 11:
            m1 = "November"
            m2 = "December"
            m3 = "January"
        elif first == 12:
            m1 = "December"
            m2 = "January"
            m3 = "February"
            
        sql = "Select TrainNumber, Count(*) from RESERVATION Natural Join RESERVES Where DepartureDate Between %s and %s GROUP BY TrainNumber"
        start = datetime.date(year1, first, 1)
        end = datetime.date(year1, first, day1)
        c.execute(sql, (start,end))
        count = 1
        Label(self.viewWin, text = "{}".format(m1)).grid(row=1, column=0)
        for record in c:
            l = record[0]
            num = record[1]
            Label(self.viewWin, text = l).grid(row=count, column=1)
            print(record)
            Label(self.viewWin, text = str(num)).grid(row=count, column=2)
            count = count + 1
        sql = "Select TrainNumber, Count(*) from RESERVATION Natural Join RESERVES Where DepartureDate Between %s and %s GROUP BY TrainNumber"
        start = datetime.date(year2, sec, 1)
        end = datetime.date(year2, sec, day2)
        c.execute(sql, (start,end))
        Label(self.viewWin, text = "{}".format(m2)).grid(row=count, column=0)
        count = count + 1
        for record in c:
            l = record[0]
            num = record[1]
            Label(self.viewWin, text = l).grid(row=count, column=1)
            print(record)
            Label(self.viewWin, text = str(num)).grid(row=count, column=2)
            count = count + 1
        sql = "Select TrainNumber, Count(*) from RESERVATION Natural Join RESERVES Where DepartureDate Between %s and %s GROUP BY TrainNumber"
        start = datetime.date(year3, third, 1)
        end = datetime.date(year3, third, day3)
        c.execute(sql, (start,end))
        Label(self.viewWin, text = "{}".format(m3)).grid(row=count, column=0)
        count = count + 1
        for record in c:
            l = record[0]
            print("record[0] is")
            print(l)
            num = record[1]
            Label(self.viewWin, text = l).grid(row=count, column=1)
            print(record)
            Label(self.viewWin, text = str(num)).grid(row=count, column=2)
            count = count + 1
        db.close()
        #self.viewrevlabel=Label(self.revwin,text="View Revenue Report").grid(row=0,column=0,columnspan=2)
 #       self.monthlabel=Label(self.revwin,text="Month").grid(row=1,column=0)
 #      self.revlabel=Label(self.revwin,text="Revenue").grid(row=1,column=1)
        #sqlGetRevenue = "SELEC"
        #Need last 3 month revenue report 
 #       self.backtoman1=Button(self.viewWin,text="Back",command=self.backtoman1


    def backtomain2(self):
        self.routerep.withdraw()
        self.manwin.deiconify()


 
    def choose(self):
        print(self.username)
        self.reslist=[]
        self.cwin=Toplevel()
        self.cwin.title("Choose Functionality")
        self.title1=Label(self.cwin,text="Choose Functionality")
        self.title1.grid(row=0,column=0)
        self.view1=Button(self.cwin,text="View Train Schedule",command=self.view)
        self.new1=Button(self.cwin,text="Make a New Reservation",command=self.registerback)
        self.update1=Button(self.cwin,text="Update a Reservation",command=self.update)
        self.cancel1=Button(self.cwin,text="Cancel a Reservation",command=self.cancel)
        self.givereview1=Button(self.cwin,text="Give Review",command=self.givereview)
        self.viewreview1=Button(self.cwin,text="View Review",command=self.viewReview)
        self.addschool1=Button(self.cwin,text="Add School Information (Student Discount",command=self.addschool)
        self.view1.grid(row=1,column=0)
        self.new1.grid(row=2,column=0)
        self.update1.grid(row=3,column=0)
        self.cancel1.grid(row=4,column=0)
        self.givereview1.grid(row=5,column=0)
        self.addschool1.grid(row=7,column=0)
        self.viewreview1.grid(row=6, column=0)
        self.logout1=Button(self.cwin,text="Log Out", command=self.logout).grid(row=8,column=0)



    def view(self):
        self.cwin.withdraw()
        self.viewwin=Toplevel()
        print(1)
        self.viewwin.title("View Train Schedule")
        self.l1 = Label(self.viewwin, text="Train Number")
        self.l1.grid(row=0,column=0,sticky=EW)
        self.val1 = StringVar()
        self.val1.set('')
        self.e1 = Entry(self.viewwin, textvariable=self.val1, state=NORMAL,width=30)
        self.e1.grid(row=0,column=1,sticky=EW)
        self.b1 = Button(self.viewwin,text='Search',command=self.viewcheck)
        self.b2 = Button(self.viewwin,text='Back',command=self.backFromView)
        self.b2.grid(row=2,column=1)
        self.b1.grid(row=2,column=0)

    def backFromView(self):
        self.viewwin.withdraw()
        self.choose()
    



    def viewcheck(self):
        self.trainnum=self.val1.get()
        print()
        db=self.connect()
        c=db.cursor()
        sqltraincheck="SELECT * FROM STOP Where TrainNumber = %s ORDER BY ArrivalTime"
        result=c.execute(sqltraincheck,self.trainnum)
        if result ==0:
            messagebox.showwarning("Invalid Train Number","Please enter a valid train number!")
            return
        else:
            self.viewwin.withdraw()
            self.schedulewin=Toplevel()
            self.viewtitle=Label(self.schedulewin,text="View Train Schedule")
            self.viewtitle.grid(row=0,column=0,columnspan=4)
            self.traintable=Label(self.schedulewin, text= "Train")
            self.arrivaltable=Label(self.schedulewin,text="Arrival Time")
            self.departuretable=Label(self.schedulewin,text="Departure Time")
            self.station=Label(self.schedulewin,text="Station")
            self.traintable.grid(row=1,column=0)
            self.arrivaltable.grid(row=1,column=1)
            self.departuretable.grid(row=1,column=2)
            self.station.grid(row=1,column=3)
            self.numberlable=Label(self.schedulewin,text=self.trainnum).grid(row=2,column=0)
            count=0
            for i in c:
                print(i)
                self.arrivallab=Label(self.schedulewin,text=i[0]).grid(row=2+count,column=1)
                self.departlab=Label(self.schedulewin,text=i[1]).grid(row=2+count,column=2)
                self.stationlab=Label(self.schedulewin,text=i[3]).grid(row=2+count,column=3)
                count=count+1
            self.back1=Button(self.schedulewin,text="Back",command=self.back1)
            self.back1.grid(row=2+count,column=2)


    def back1(self):
        self.schedulewin.withdraw()
        self.viewwin.deiconify()
        self.view
        self.val1.set("")


    def viewschedule(self):
        self.cwin.withdraw()
        self.viewschedule=Toplevel()
        print(1.5)
        self.viewschedule.title("View Train Schedule")
        self.l1 = Label(self.viewschedule,text="View Train Schedule")
        self.l1.grid(row=0,column=0,columnspan=4)
        self.b1 = Button(self.viewschedule,text="Back",command=self.back)
        self.b1.grid(row=1,column=0)
        #make table from SQL

    def back(self):
        self.viewschedule.withdraw()
        self.viewwin.deiconify()

    def registerback(self):
        print("Hi")
        #pull info on departure options, arrival options, and day options
        self.new()



    def new(self):
        self.cwin.withdraw()
        self.newwin=Toplevel()
        self.header1=Label(self.newwin,text="Search Train")
        self.label1=Label(self.newwin,text="Departs From")
        self.label2=Label(self.newwin,text="Arrives At")
        self.label3=Label(self.newwin,text="Departure Date (YYYY-MM-DD)")
        self.header1.grid(row=0,column=0,columnspan=2)
        self.label1.grid(row=1,column=0)
        self.label2.grid(row=2,column=0)
        self.label3.grid(row=3,column=0)
        self.var1=StringVar(win)
        self.var1.set("")
        self.var2=StringVar(win)
        self.var2.set("")
        self.var3=StringVar(win)
        self.var3.set("")
        self.option1=OptionMenu(self.newwin,self.var1,"Pixie Dust Station","Tech Trolley Stop","Swarles Barkley", "Midtown Marta", "Fire Depot", "Big Red Spot")
        self.option2=OptionMenu(self.newwin,self.var2,"Pixie Dust Station","Tech Trolley Stop","Swarles Barkley", "Midtown Marta", "Fire Depot", "Big Red Spot")
        self.dateentry=Entry(self.newwin)
        self.option1.grid(row=1,column=1)
        self.option2.grid(row=2,column=1)
        self.dateentry.grid(row=3,column=1)
        self.findtrain=Button(self.newwin,text="Find Trains",command=self.selectcheck)
        self.findtrain.grid(row=4,column=0,columnspan=2)


    def selecttrain(self):
        # takes the results of selectcheck()
        # displays them
        self.newwin.withdraw()
        self.select=Toplevel()
        trainPos = self.trainPosibilities
        self.selectheader=Label(self.select,text="Results")
        self.selectheader.grid(row=0,column=0,columnspan=3)
        self.selectTrainNumLabel=Label(self.select,text="Train Number")
        self.selectTrainNumLabel.grid(row=1,column=0)
        self.timeheader=Label(self.select,text="Time").grid(row=1,column=1)
        self.firstClassLabel=Label(self.select,text="First Class Price")
        self.firstClassLabel.grid(row=1,column=2)
        self.secondClassLabel=Label(self.select,text="Second Class Price")
        self.secondClassLabel.grid(row=1,column=3)
        count = 0
        self.var=StringVar()
        self.var.set("Hello")
        for i in trainPos:
            trainNumber=i[0]
            self.trainNumber=Label(self.select,text=i[0]).grid(row=2+count,column=0)
            self.timeduration=Label(self.select,text="Duration is " +str(i[3])+ ", Departure Time is " + str(i[4]) + " Arrival Time is " +str(i[5])).grid(row=2+count,column=1)
            self.firstClassPricebut=Radiobutton(self.select,text=i[1],variable=self.var,value=str(i[0])+"_"+str(i[1])).grid(row=2+count,column=2)
            self.SecondClassPricebut=Radiobutton(self.select,text=i[2],variable=self.var,value=str(i[0])+"_"+str(i[2])).grid(row=2+count,column=3)
            count=count+1
        self.trainNumNewReservation = trainNumber
        self.back=Button(self.select,text="Back",command=self.goback)
        self.next=Button(self.select,text="Next",command=self.addbaginfo)
        self.back.grid(row=count+5,column=0)
        self.next.grid(row=count+5,column=2)





    def addbaginfo(self):
        print(self.var.get())
        if self.var.get()=="Hello":
            messagebox.showerror("Please choose a train","Please choose a train")
            return

        print(self.var.get())
        self.select.withdraw()
        self.bagwin=Toplevel()
        self.passinfolab=Label(self.bagwin,text="Travel Extras and Passenger Info").grid(row=0,column=0,columnspan=2)
        self.numbaglab=Label(self.bagwin,text="Number of Bags").grid(row=1,column=0)
        self.infolab=Label(self.bagwin,text="Every passenger can bring up to 4 baggage. 2 free of charge, 2 for $30 per bag.")
        self.passname=Label(self.bagwin,text="Passengername").grid(row=2,column=0)
        self.bagvar=IntVar()
        self.bagvar.set(0)
        self.bagoption=OptionMenu(self.bagwin,self.bagvar,0,1,2,3,4).grid(row=1,column=1)
        self.passnameentry=Entry(self.bagwin)
        self.passnameentry.grid(row=2,column=1)
        self.confirmbags=Button(self.bagwin,text="Next",command=self.gatherinfo).grid(row=3,column=1)
        self.backfrombags=Button(self.bagwin,text="Back",command=self.backfrombag).grid(row=3,column=0)

    def backfrombag(self):
        print("hi")


    def gatherinfo(self):
        print(self.passnameentry.get())
        values=self.var.get()
        split = values.split("_")
        trainnum=split[0]
        print(trainnum)
        dicttrainnum=int(trainnum)
        self.arrivaltime=self.arrivaltimedict.get(dicttrainnum,"none")
        print(self.arrivaltime)
        self.depttime=self.depttimedict.get(dicttrainnum,"hi")
        self.totaltime=self.arrivaltime-self.depttime
        print(self.depttime)
        print(self.totaltime)        
        price=split[1]
        db=self.connect()
        c=db.cursor()
        d=db.cursor()
        departstationsql="SELECT NAME FROM `STOP` WHERE TRAINNUMBER = %s  AND DEPARTURETIME IS NULL"
        arrivalstationsql= "SELECT NAME FROM `STOP` WHERE TRAINNUMBER =%s  AND ARRIVALTIME IS NULL"
        departstation=c.execute(departstationsql,trainnum)
        arrivalstation=d.execute(arrivalstationsql,trainnum)
        for i in c:
           departstation= i[0]
        for i in d:
           arrivalstation=i[0]
        self.numbags=self.bagvar.get()
        e=db.cursor()
        #Check if first or second class
        trainnum=int(trainnum)
        price=int(price)
        firstclasssql="SELECT * FROM `TRAIN_ROUTE` WHERE TrainNumber = %s AND FirstClassPrice IN(%s)"
        firstclass=e.execute(firstclasssql,(trainnum,price))
        if firstclass==0:
            trainclass="second class"
        elif firstclass==1:
            trainclass="First Class"
        print(trainclass)
        
        name=self.passnameentry.get()
        if name=="":
            messagebox.showwarning("Check your name","Please enter a name")
            return
        print(self.reslist)
        #check if user is student
        f=db.cursor()
        studentsql="SELECT * FROM CUSTOMER WHERE USERNAME = %s AND IsStudent =1"
        studentsql=f.execute(studentsql,self.username)
        print(studentsql)
        if studentsql==1:
            self.student=1
        elif studentsql==0:
            self.student=0
        timelist=[]
        timelist.append(self.arrivaltime)
        timelist.append(self.depttime)
        timelist.append(self.totaltime)
        #for use in calculating discount
        #for use in calculating discount
        self.reslist.append([trainnum,timelist,departstation,arrivalstation,trainclass,price,self.numbags,name,self.userdateforlater])
        self.calculatecost()

        
        
        #appending all values for make reservation page in order
        
       

    def calculatecost(self):
        self.bagwin.withdraw()
        self.makeres=Toplevel()
        self.makereshead=Label(self.makeres,text="Make Reservation").grid(row=0,column=1,columnspan=7)
        currentlySelected=Label(self.makeres,text="Currently Selected").grid(row=1,column=0,)
        self.trainnum=Label(self.makeres,text="Train").grid(row=2,column=0)
        self.timeres=Label(self.makeres,text="Time").grid(row=2,column=1)
        self.departsres=Label(self.makeres,text="Departs From").grid(row=2,column=2)
        self.arrivesat=Label(self.makeres,text="Arrives At").grid(row=2,column=3)
        self.trainclass=Label(self.makeres,text="Class").grid(row=2,column=4)
        self.priceofres=Label(self.makeres,text="Price").grid(row=2,column=5)
        self.numofbags=Label(self.makeres,text="# of Baggages").grid(row=2,column=6)
        self.passname=Label(self.makeres,text="Passenger Name").grid(row=2,column=7)
        self.remove=Label(self.makeres,text="Remove").grid(row=2,column=8)
        self.costcount=3
        totalcost=0
        for i in self.reslist:
            self.trainval=Label(self.makeres,text=i[0]).grid(row=self.costcount,column=0)
            self.timeval=Label(self.makeres,text="The train departs on "+ str(i[8]) + " at " + str(i[1][1]) + " and arrives at " + str(i[1][0]) + " and has a total time of " + str(i[1][2]),wraplength=250).grid(row=self.costcount,column=1)
            self.departval=Label(self.makeres,text=i[2]).grid(row=self.costcount,column=3)
            self.arrivalval=Label(self.makeres,text=i[3]).grid(row=self.costcount,column=2)
            self.trainclassval=Label(self.makeres,text=i[4]).grid(row=self.costcount,column=4)
            self.priceval=Label(self.makeres,text=i[5]).grid(row=self.costcount,column=5)
            self.bagval=Label(self.makeres,text=i[6]).grid(row=self.costcount,column=6)
            self.nameval=Label(self.makeres,text=i[7]).grid(row=self.costcount,column=7)
            self.remove=Button(self.makeres,text="Remove").grid(row=self.costcount,column=8,command=self.remove)
            self.costcount=self.costcount+1
            totalcost=totalcost+i[5]
            if self.numbags==3:
                totalcost=totalcost+30
            elif self.numbags==4:
                print(totalcost)
                totalcost=totalcost+60

        if self.student==1:
            self.studentdisclabel=Label(self.makeres,text="Student Discount Applied").grid(row=self.costcount,column=0)
            self.costcount=self.costcount+1
        self.totcostlab=Label(self.makeres,text="Total Cost").grid(row=self.costcount,column=0)
        self.usecardlab=Label(self.makeres,text="Use Card").grid(row=self.costcount+1,column=0)
        if self.student==1:
            totalcost=.8*totalcost
        else:
            totalcost=totalcost
        self.totalcostentry=Label(self.makeres,text=totalcost).grid(row=self.costcount,column=1)
        self.buttontoaddcard=Button(self.makeres,text="Add Card",command=self.addCreditCard).grid(row=self.costcount+1,column=2)
        self.continueaddingtrain=Button(self.makeres,text="Continue adding a train",command=self.backtoselect).grid(row=self.costcount+2,column=0)
        self.backtobagbutton=Button(self.makeres,text="Back",command=self.backtobag).grid(row=self.costcount+3,column=0)
        self.submitresbutton=Button(self.makeres,text="Submit",command=self.submitres).grid(row=self.costcount+3,column=1)
        ccoption=[123444,202404,1230419]
        db=self.connect()
        a=db.cursor()
        ccsql="SELECT `CardNumber` FROM `PAYMENT_INFORMATION` WHERE `Username` = %s"
        ccresult=a.execute(ccsql,self.username)
        ccoption=[]
        for i in a:
            ccoption.append(i[0])
        print(ccoption)
        self.ccvar=IntVar()
        self.totalcost=totalcost
        self.ccvar.set(ccoption[0])
        self.cardoptionmenu=OptionMenu(self.makeres,self.ccvar,*ccoption)
        self.cardoptionmenu.grid(row=self.costcount+1,column=3)


    def remove(self):
        print("Hello")


    def backtobag(self):
        reslistcount=len(self.reslist)-1
        del self.reslist[reslistcount]
        self.makeres.destroy()
        self.backtobag=self.bagwin.destroy()
        self.addbaginfo()



    def submitres(self):
        print("hello")
        db = self.connect()
        c = db.cursor()
        #Insert into table values from above
        revID = random.randrange(1000, 10000)
        sql = "SELECT 'ReservationID' FROM RESERVATION"
        c.execute(sql)
##        self.answer = IntVar()
##        self.answer.set('0')
        print(revID)
        count = 0
        for record in c:
            if record[0] == revID:
                submitres(self)
            else:
                self.answer = revID
               # print(self.answer)
##                self.answer.set(revID)

        self.confirmation()


    def confirmation(self):
        print("confirming")
        self.bagwin.withdraw()
        self.makeres.withdraw()
        self.confirmwin=Toplevel()
        #answer = self.answer.get()
        self.ID = IntVar()
        self.ID.set(self.answer)
        self.L1 = Label(self.confirmwin,text="Confirmation")
        self.L1.grid(row=0,column=0,columnspan=2)
        self.L2 = Label(self.confirmwin,text="Reservation ID")
        self.L2.grid(row=1,column=0)
        self.L3 = Entry(self.confirmwin,textvariable= self.ID,state="readonly")
        self.L3.grid(row=1,column=1)
        self.L4 = Label(self.confirmwin,text="Thank you for your purchase! Please save reservation ID for your records.")
        self.L4.grid(row=2,column=0,columnspan=2)
        self.B1 = Button(self.confirmwin,text="Go back to choose functionality",command=self.backtohome)
        self.B1.grid(row=3,column=0,columnspan=2)

        print(self.reslist)
        #self.reslist.append([trainnum,timelist,departstation,arrivalstation,trainclass,price,numbags,name])
#        self.reslist.append(self.answer)
       # print(self.reslist)

        db = self.connect()
        c = db.cursor()
####help with date stuff for self.date
        sql1 = 'INSERT INTO RESERVES VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        #self.totalcost
        print(self.userdateforlater)
        stuff = (self.userdateforlater,self.reslist[0][6],self.reslist[0][4],self.reslist[0][7],self.reslist[0][2],self.reslist[0][3],self.answer,self.reslist[0][0])
        print(stuff)
        for i in range(len(self.reslist)):
            result = c.execute(sql1,(self.reslist[i][8],self.reslist[i][6],self.reslist[i][4],self.reslist[i][7],self.reslist[i][2],self.reslist[i][3],self.answer,self.reslist[i][0],self.totalcost))
        stuff = (self.userdateforlater,self.reslist[0][6],self.reslist[0][4],self.reslist[0][7],self.reslist[0][2],self.reslist[0][3],self.answer,self.reslist[0][0])
        print(stuff)
        print(str(self.userdateforlater))

        sql2 = 'INSERT INTO RESERVATION VALUES(%s,%s,%s,%s)'
        card = self.ccvar.get()
        print(card)
        stuffagain = (self.answer,0,card,self.username)
        print(stuffagain)

        result2 = c.execute(sql2,(self.answer,0,card,self.username))



    
    def backtohome(self):
        print('hi')
        self.makeres.destroy()
        self.bagwin.destroy()
        self.select.destroy()
        self.newwin.destroy()
        self.confirmwin.destroy()
        self.choose() 

    
        

    def backtoselect(self):
        self.makeres.destroy()
        self.bagwin.destroy()
        self.select.destroy()
        self.newwin.destroy()
        self.new()
        


    
        
        
            
    def goback(self):
        self.select.withdraw()
        self.new()

    def selectcheck(self):
        try:
            self.userdateforlater=self.dateentry.get()
            # called from new()
            # Query
            self.resdate=self.dateentry.get()
            datet = self.resdate.split("-")
            yr = datet[0]
            month = datet[1]
            day = datet[2]
            date2 = datetime.datetime(int(yr), int(month), int(day), 11, 30, 59).date()
            today = datetime.datetime.now().date()
            if today > date2:
                messagebox.showwarning("Date Passed", "A train cannot be booked for a date that has already passed.")
                return()

            print(self.resdate)
            print(len(self.resdate))
            if len(self.resdate)!=10:
                messagebox.showerror("Check your entry","Invalid Date")
                return()
            dList=self.resdate.split("-")
            print(dList)
            print(len(dList))
            if len(dList)!=3:
                messagebox.showerror("Check your entry","Invalid Date")
                return()



            print("Hi")
            arrivalStation=self.var2.get()
            departureStation=self.var1.get()
            if arrivalStation==departureStation:
                messagebox.showwarning("Check your entry","Please make sure the arrival and departure locations are different and a date is entered!")
                return
            print("arrival station:" + arrivalStation)
            print("departure station: " + departureStation)
            db = self.connect()
            c = db.cursor()
            
            # qeury part 1, loosking at departure station
            dictDeptTimes = dict() # train number to departure time
            sqlQueryUserInfo = "SELECT ArrivalTime, DepartureTime, TrainNumber, Name FROM STOP WHERE Name = %s"
            # get the possible train number value
            result=c.execute(sqlQueryUserInfo, departureStation)
            print(result)
            if result != 0:
                data = c.fetchall()
                possTrainNums = []
                print(possTrainNums)
                for d in data:
                
                    if (d[1] != None):
                        print(d[2])
                        possTrainNums.append(d[2])
                        dictDeptTimes[d[2]]= d[1]
                
                        
                # query part 2, looking at arrival station
                dictArrTimes = dict() # train number to departure time
                sqlQueryUserInfo2 = "SELECT ArrivalTime, DepartureTime, TrainNumber, Name FROM STOP WHERE Name = %s"
                # get the possible train number value
                c.execute(sqlQueryUserInfo2, arrivalStation)
                data = c.fetchall()
                matchingTrainNums = []

                for d in data:
                    if d[2] in possTrainNums and d[0] != None:
                        matchingTrainNums.append(d[2])
                        dictArrTimes[d[2]]= d[0]

                # query part 3, look at times
                trainNum = ""
                dur = 0
                finaltrainList=[]
                for k in dictArrTimes.keys():
                    trainval=[]
                    # compare arrival and departure times for train numbers
                    if dictArrTimes[k] > dictDeptTimes[k]: 
                        trainNum = k
                        dur = dictArrTimes[k] - dictDeptTimes[k] # diff between times
                        trainval.append(k)
                        trainval.append(dur)
                        trainval.append(dictDeptTimes[k])
                        trainval.append(dictArrTimes[k])
                        finaltrainList.append(trainval)
                print(finaltrainList)
                        
                # now we have the train number that matches user query
                # need to get the necessary information
                self.allinfo=[]
                for i in finaltrainList:
                    sqlGet= "SELECT TrainNumber, FirstClassPrice, SecondClassPrice FROM TRAIN_ROUTE WHERE TrainNumber = %s"
                    trainRouteInfoResult = c.execute(sqlGet, i[0])
                    data = c.fetchall()
                    count=0
                    for d in data:
                        littlelist=[]
                        trainNum = d[0]
                        firstClassPrice = d[1]
                        secondClassPrice = d[2]
                        littlelist.append(trainNum)
                        littlelist.append(firstClassPrice)
                        littlelist.append(secondClassPrice)
                        littlelist.append(i[1])
                        littlelist.append(i[2])
                        littlelist.append(i[3])
                        self.allinfo.append(littlelist)

                self.arrivaltimedict=dictArrTimes
                self.depttimedict=dictDeptTimes
                        
                ##Get Train number, duration, 1st class price, 2nd class price from departure station,arrival station, and date
                self.trainPosibilities=self.allinfo
                self.selecttrain()
            else:
                    messagebox.showwarning("Invalid Train Number","Please enter valid parameters")
                    return
        except:
            messagebox.showwarning("Invalid Train Number","Please enter valid parameters")            




    def addCreditCard(self):
        # anna did this GUI stuff, so not sure if its right
        self.select.withdraw()
        self.creditCardWin=Toplevel()
        trainNum = self.trainNumNewReservation
        self.newWinRestLabel=Label(self.creditCardWin,text=" Credit Card Information")
        self.creditCardNum=Label(self.creditCardWin,text="Enter Card Number:")
        self.creditCardEntry=Entry(self.creditCardWin)
        self.cvvLabel=Label(self.creditCardWin,text="Enter CVV:")
        self.cvvEntry=Entry(self.creditCardWin)
        self.nameOnCardLabel=Label(self.creditCardWin,text="Enter Name On Card:")
        self.nameOnCardEntry=Entry(self.creditCardWin)
        self.expDateLabel=Label(self.creditCardWin,text="Enter Expiration Data:")
        self.expDateEntry=Entry(self.creditCardWin)
        self.newWinRestLabel.grid(row=0,column=0,columnspan=2)
        self.creditCardNum.grid(row=1,column=0)
        self.creditCardEntry.grid(row=1,column=1)
        self.cvvLabel.grid(row=2,column=0)
        self.cvvEntry.grid(row=2,column=1)
        self.nameOnCardLabel.grid(row=3,column=0)
        self.nameOnCardEntry.grid(row=3,column=1)
        self.expDateLabel.grid(row=4,column=0)
        self.expDateEntry.grid(row=4,column=1)
        self.addCreditCard=Button(self.creditCardWin,text="Add Credit Card Info",command=self.checkAddCard)
 #       self.backToMainButton=Button(self.creditCardWin,text="Back",command=self.backFromNewCreditCard)
        self.addCreditCard.grid(row=5,column=0)
#        self.backToMainButton.grid(row=5, column=1)
        print(trainNum)

        self.L1 = Label(self.creditCardWin,text="Delete Card")
        self.L1.grid(row=0,column=2,columnspan=2)
        self.L2 = Label(self.creditCardWin,text="Card Number")
        self.L2.grid(row=1,column=2)

        db=self.connect()
        a=db.cursor()
        ccsql="SELECT `CardNumber` FROM `PAYMENT_INFORMATION` WHERE `Username` = %s"
        ccresult=a.execute(ccsql,self.username)
        ccoption=[]
        for i in a:
            ccoption.append(i[0])
        print(ccoption)
        self.ccvar2=IntVar()
        self.ccvar2.set(ccoption[0])
        self.cardoptionmenu=OptionMenu(self.creditCardWin,self.ccvar2,*ccoption)
        self.cardoptionmenu.grid(row=1,column=3)


        self.B1 = Button(self.creditCardWin,text="Delete Credit Card",command=self.deleteCard)
        self.B1.grid(row=5,column=2)

##        self.backToMainButton=Button(self.creditCardWin,text="Submit",command=self.backFromNewCreditCard)
##        self.addCreditCard.grid(row=5,column=0)
##        self.backToMainButton.grid(row=5, column=1)
##        print(trainNum)

    def deleteCard(self):
##need to recall at end so updates
        print("deleting card")
        usr = self.username
        db = self.connect()
        c = db.cursor()
        sqlDeleteCard = "DELETE FROM PAYMENT_INFORMATION WHERE CardNumber = %s"

        cardNum = self.ccvar2.get()
        print(cardNum)

 #       cardNum = cardNum[0]
        deleting = c.execute(sqlDeleteCard,cardNum)
        self.creditCardWin.withdraw()
        self.makeres.destroy()
        self.calculatecost()


        
    def backFromNewCreditCard(self):
        print("Hi")
        
    def update(self):
        # update a reservation, called from choose()
        # needs some work
        self.cwin.withdraw()
        self.updateWin=Toplevel()
        usr = self.username
        db = self.connect()
        c = db.cursor()
        self.updateWinHeader=Label(self.updateWin,text="Update Reservation")
        self.resIdLabel=Label(self.updateWin,text="Enter Reservation: ")
        self.resIdEntry=Entry(self.updateWin)
        self.reservationNextButton=Button(self.updateWin,text="Search for Reservation",command=self.lookForReservation)
        self.updateWinHeader.grid(row=0, column=0, columnspan=2)
        self.resIdLabel.grid(row=1, column=0)
        self.resIdEntry.grid(row=1, column=1)
        self.reservationNextButton.grid(row=2, column=1)
        self.backButton=Button(self.updateWin,text="Back",command=self.backFromUpdate).grid(row=2, column=0)

    def backFromUpdate(self):
        self.updateWin.withdraw()
        self.choose()

        
    def lookForReservation(self):
        db= self.connect()
        c = db.cursor()
        resID = self.resIdEntry.get()
        usr = self.username
        print("searching for: " + resID)
        sqlCheckUser = "SELECT * FROM RESERVATION WHERE (ReservationID=%s AND Username=%s)"
        print("Checking for username")
        checkUser = c.execute(sqlCheckUser, (resID, usr))
        print(checkUser)
        if (checkUser == 0):
            messagebox.showwarning("Error ", "No Reservations Match that ID or Your username does not match the username of the reservation.")
            self.updateWin.withdraw()
            self.choose()
        else:
            print("searching for: " + resID)
            sqlGet= "SELECT * FROM RESERVES WHERE ReservationID = %s"
            reservationResult = c.execute(sqlGet, resID)
            print(reservationResult)
            data = c.fetchall()
            if (len(data) == 0):
                messagebox.showwarning("Invalid", "No Reservations Match that ID.")
                return
            else:
                for d in data:
                    print(d)
                self.updateWin.withdraw()
                self.chooseTicketWin=Toplevel()
                self.chooseTicketHeader=Label(self.chooseTicketWin,text="Select Which Ticket to Update")
                self.chooseTicketHeader.grid(row=0, column=0, columnspan=8)
                self.trainNumberHeader=Label(self.chooseTicketWin,text="Train Number:").grid(row=1, column=1)
                self.reservationIDHeader=Label(self.chooseTicketWin,text="Departure Date:").grid(row=1, column=2)

                self.reservationIDHeader=Label(self.chooseTicketWin,text="ReservationID:").grid(row=1, column=0)
                self.departureHeader=Label(self.chooseTicketWin,text="Departure Location:").grid(row=1, column=3)
                self.arrivalHeader=Label(self.chooseTicketWin,text="Arrival Location:").grid(row=1, column=4)
                self.classHeader=Label(self.chooseTicketWin,text="Class:").grid(row=1, column=5)
                self.passNameHeader=Label(self.chooseTicketWin,text="Passenger Name:").grid(row=1, column=6)


                count = 0
                self.varPassName=StringVar()
                self.varPassName.set("Hello")
                for i in data:
                    print("Found i")
                    trainNumber=i[0]
                    print(i)
                    self.reservationIDButton=Radiobutton(self.chooseTicketWin,text=i[6],variable=self.varPassName,value=str(i[6])+"_"+str(i[3])+"_"+str(i[0])+"_"+str(i[4])+"_"+str(i[5])+"_"+str(i[7])+"_"+str(i[8])).grid(row=2+count,column=0)
                    #self.reservationID=Label(self.chooseTicketWin,text=i[6]).grid(row=2+count,column=0)
                    self.trainNumberLab=Label(self.chooseTicketWin,text=i[7]).grid(row=2+count,column=1)
                    self.departDate=Label(self.chooseTicketWin,text=i[0]).grid(row=2+count,column=2)
                    self.departureLocation=Label(self.chooseTicketWin,text=i[4]).grid(row=2+count,column=3)
                    self.arrivalLocation=Label(self.chooseTicketWin,text=i[5]).grid(row=2+count,column=4)
                    self.classOfTicket=Label(self.chooseTicketWin,text=i[2]).grid(row=2+count,column=5)
                    self.passNameLabel= Label(self.chooseTicketWin,text=i[3]).grid(row=2+count,column=6)
                    #self.passNameButton=Radiobutton(self.chooseTicketWin,text=i[3],variable=self.varPassName,value=str(i[6])+"_"+str(i[3])).grid(row=2+count,column=4)
                    count=count+1
                self.nextBut=Button(self.chooseTicketWin,text="Update Selected Ticket",command=self.updateSpecificTicket).grid(row=2+count, column=6)
            print(3)


    
    def updateSpecificTicket(self):
            self.chooseTicketWin.withdraw()
            self.updateTicketWin=Toplevel()
            self.updateTicketWinLabel=Label(self.updateTicketWin,text="Update Reservation")
            self.updateTicketWinLabel.grid(row=0, column=0, columnspan=8)
            self.currentTicketLabel=Label(self.updateTicketWin,text="Current Train Ticket").grid(row=1, column=0)

            self.trainNumberHeader=Label(self.updateTicketWin,text="Train Number:").grid(row=2, column=1)
            self.reservationIDHeader=Label(self.updateTicketWin,text="Departure Date:").grid(row=2, column=2)
            self.reservationIDHeader=Label(self.updateTicketWin,text="ReservationID:").grid(row=2, column=0)
            self.departureHeader=Label(self.updateTicketWin,text="Departure Location:").grid(row=2, column=3)
            self.arrivalHeader=Label(self.updateTicketWin,text="Arrival Location:").grid(row=2, column=4)
 #           self.classHeader=Label(self.updateTicketWin,text="Class:").grid(row=1, column=5)
            self.passNameHeader=Label(self.updateTicketWin,text="Passenger Name:").grid(row=2, column=5)
            # get selected information
            choosenTicketInfo= self.varPassName.get()
            values = choosenTicketInfo.split("_")
            self.updateValues=values
            reservationNum=values[0]
            passName=values[1]
            departDate=values[2]
            departLocation=values[3]
            arrivalLocation=values[4]
            trainNumb = values[5]
            totalCost= values[6]
            self.trainNumberLabel=Label(self.updateTicketWin,text=trainNumb).grid(row=3, column=1)
            self.reservationLabel=Label(self.updateTicketWin,text=reservationNum).grid(row=3, column=0)
            self.dateLabel=Label(self.updateTicketWin,text=departDate).grid(row=3, column=2)
            self.departLabel=Label(self.updateTicketWin,text=departLocation).grid(row=3, column=3)
            self.arrivalLabel=Label(self.updateTicketWin,text=arrivalLocation).grid(row=3, column=4)
            self.passNameLabel=Label(self.updateTicketWin, text=passName).grid(row=3, column=5)
            
            self.newDeptDate=Label(self.updateTicketWin, text="New Departure Date YYYY-MM-DD").grid(row=4, column=0)
            self.newDeptDateEntry=Entry(self.updateTicketWin)
            self.newDeptDateEntry.grid(row=4, column=1)
            self.searchNewDate=Button(self.updateTicketWin, text="Search Availability", command=self.searchAvailability).grid(row=4,column=2)
 #           self.classLabel=Label(self.updateTicketWin, text=passName).grid(row=2, column=6)
            self.v = StringVar()
            self.updatedTicketLabel1=Label(self.updateTicketWin,text="Updated Train Ticket").grid(row=5, column=0)
            self.trainNumberLabel1=Label(self.updateTicketWin,text=trainNumb).grid(row=6, column=1)
            self.reservationLabel1=Label(self.updateTicketWin,text=reservationNum).grid(row=6, column=0)
            self.dateLabel1=Label(self.updateTicketWin,textvariable=self.v).grid(row=6, column=2)
            self.departLabel1=Label(self.updateTicketWin,text=departLocation).grid(row=6, column=3)
            self.arrivalLabel1=Label(self.updateTicketWin,text=arrivalLocation).grid(row=6, column=4)
            self.passNameLabel1=Label(self.updateTicketWin, text=passName).grid(row=6, column=5)
            # need to get the current price of the reservation
            # @matt
            newTotalCost = int(totalCost)+50
            self.changeFeeLabel=Label(self.updateTicketWin, text="Change Fee").grid(row=8, column=0)
            self.changeFeeValueLabel=Label(self.updateTicketWin, text = "$50").grid(row=8, column=1)
            self.totalNewPrice=Label(self.updateTicketWin, text="New Total Price").grid(row=9, column=0)
            self.totalNewPriceValue=Label(self.updateTicketWin, text="$"+str(newTotalCost)).grid(row=9, column=1)
            self.cancelBut=Button(self.updateTicketWin, text="Cancel Update", command=self.cancelUpdate).grid(row=8, column=5)
            self.submitButton=Button(self.updateTicketWin, text="Submit Changes", command=self.processUpdate).grid(row=9, column=5)
 #           dateLabel1.set()
 #           self.trainNumberLabel1=Label(self.updateTicketWin,text=trainNumb).grid(row=5, column=1)                

                

    def searchAvailability(self):
        # need to check if new date is within one date of current day
        # @matt
        newDate=self.newDeptDateEntry.get()
        self.newDateForUpdate=newDate
        self.v.set(newDate)        
        return
    
    def cancelUpdate(self):
        self.updateTicketWin.withdraw()
        self.choose()

    def processUpdate(self):
        db = self.connect()
        c = db.cursor()
        print("Processing")
        #date =  self.newDateForUpdate
        values = self.updateValues
        reservationNum=values[0]
        passName=values[1]
        departLocation=values[3]
        arrivalLocation=values[4]
        trainNumb = values[5]
        sql = "SELECT TotalCost FROM RESERVES WHERE ReservationID=%s"
        c.execute(sql, reservationNum)
        tc = c.fetchall()[0][0]
        today = datetime.datetime.now().date()
        sql = "SELECT DepartureDate FROM RESERVES WHERE ReservationID=%s"
        c.execute(sql, reservationNum)
        depdate = c.fetchall()[0][0]
        delta = depdate - today
        if delta.days <= 1:
            messagebox.showwarning("Cannot Update", "A Reservation cannot be updated the day before departure.")
        else:
            sql = "UPDATE RESERVES SET TotalCost = %d WHERE (ReservationID=%s AND PassengerName=%s AND TrainNumber=%s AND DepartsFrom=%s)"
            c.execute(sql, (tc+50, reservationNum, passName, trainNumb, departLocation))
            sql = "UPDATE RESERVES SET DepartureDate = %s WHERE (ReservationID=%s AND PassengerName=%s AND TrainNumber=%s AND DepartsFrom=%s)"
            resultOfUpdate = c.execute(sql, (date,reservationNum, passName, trainNumb, departLocation))
            if (resultOfUpdate == 1):
                messagebox.showwarning("Update Successful", "Your Reservation has successfully been updated.")
                self.updateTicketWin.withdraw()
                self.choose()
            else:
                messagebox.showwarning("Update Failed", "The update failed. Please try again.")
                self.updateTicketWin.withdraw()
                self.update()

       

    def checkAddCard(self):
        # adds credit card to cb, called from addCreditCard()
        # needs work - need to check if data is valid
        print("Checking Add Credit Card")
        usr = self.username
        creditCardNum = self.creditCardEntry.get()
        cvv = self.cvvEntry.get()
        nameOnCard = self.nameOnCardEntry.get()
        expDate = self.expDateEntry.get()
        db = self.connect()
        c = db.cursor()
        sqlInsertCredit = "INSERT INTO PAYMENT_INFORMATION VALUES(%s, %s, %s, %s, %s)"
        tryToAddCredit = c.execute(sqlInsertCredit, (creditCardNum, cvv, nameOnCard, expDate,usr))
        if (tryToAddCredit == 0):
            print("success")
        self.creditCardWin.withdraw()
        self.makeres.destroy()
        self.calculatecost()

        
        

    def cancel(self):
        self.cwin.withdraw()
        self.cancelWin=Toplevel()
        usr = self.username
        db = self.connect()
        c = db.cursor()
        self.cancelWinHeader=Label(self.cancelWin,text="Cancel Reservation")
        self.resIdLabel=Label(self.cancelWin,text="Enter Reservation: ")
        self.resIdEntry=Entry(self.cancelWin)
        self.reservationNextButton=Button(self.cancelWin,text="Search for Reservation",command=self.lookForReservationCancel)
        self.cancelWinHeader.grid(row=0, column=0, columnspan=2)
        self.resIdLabel.grid(row=1, column=0)
        self.resIdEntry.grid(row=1, column=1)
        self.reservationNextButton.grid(row=2, column=1)
        self.backButton=Button(self.cancelWin,text="Back",command=self.backFromCancel).grid(row=2, column=0)

    def backFromCancel(self):
        self.cancelWin.withdraw()
        self.choose()
            
    def lookForReservationCancel(self):
        db= self.connect()
        c = db.cursor()
        resID = self.resIdEntry.get()
        usr = self.username
        print("searching for: " + resID)
        sqlCheckUser = "SELECT * FROM RESERVATION WHERE (ReservationID=%s AND Username=%s)"
        print("Checking for username")
        checkUser = c.execute(sqlCheckUser, (resID, usr))
        print(checkUser)
        if (checkUser == 0):
            messagebox.showwarning("Already Cancelled", "No Reservations Match that ID or Your username does not match the username of the reservation.")
            self.cancelWin.withdraw()
            self.choose()
        else:
            sqlGet= "SELECT * FROM RESERVES WHERE ReservationID = %s"
            reservationResult = c.execute(sqlGet, resID)
            print(reservationResult)
            data = c.fetchall()
            if (len(data) == 0):
                messagebox.showwarning("Invalid", "No Reservations Match that ID or Your username does not match the username of the reservation.")
                return
            else:
                for d in data:
                    print(d)
                self.cancelWin.withdraw()
                self.chooseTicketCancelWin=Toplevel()
                self.chooseTicketHeader=Label(self.chooseTicketCancelWin,text="Select Which Ticket to Update")
                self.chooseTicketHeader.grid(row=0, column=0, columnspan=8)
                self.trainNumberHeader=Label(self.chooseTicketCancelWin,text="Train Number:").grid(row=1, column=1)
                self.reservationIDHeader=Label(self.chooseTicketCancelWin,text="Departure Date:").grid(row=1, column=2)

                self.reservationIDHeader=Label(self.chooseTicketCancelWin,text="ReservationID:").grid(row=1, column=0)
                self.departureHeader=Label(self.chooseTicketCancelWin,text="Departure Location:").grid(row=1, column=3)
                self.arrivalHeader=Label(self.chooseTicketCancelWin,text="Arrival Location:").grid(row=1, column=4)
                self.classHeader=Label(self.chooseTicketCancelWin,text="Class:").grid(row=1, column=5)
                self.passNameHeader=Label(self.chooseTicketCancelWin,text="Passenger Name:").grid(row=1, column=6)
                count = 0
                self.varPassName1=StringVar()
                self.varPassName1.set("Hello")
                self.reservationToCancel=resID
                for i in data:
                    print("Found i")
                    trainNumber=i[0]
                    print(i)
                    self.reservationIDButton=Label(self.chooseTicketCancelWin,text=i[6]).grid(row=2+count,column=0)
                    #self.reservationID=Label(self.chooseTicketWin,text=i[6]).grid(row=2+count,column=0)
                    self.trainNumberLab=Label(self.chooseTicketCancelWin,text=i[7]).grid(row=2+count,column=1)
                    self.departDate=Label(self.chooseTicketCancelWin,text=i[0]).grid(row=2+count,column=2)
                    self.departureLocation=Label(self.chooseTicketCancelWin,text=i[4]).grid(row=2+count,column=3)
                    self.arrivalLocation=Label(self.chooseTicketCancelWin,text=i[5]).grid(row=2+count,column=4)
                    self.classOfTicket=Label(self.chooseTicketCancelWin,text=i[2]).grid(row=2+count,column=5)
                    self.passNameLabel= Label(self.chooseTicketCancelWin,text=i[3]).grid(row=2+count,column=6)
                    #self.passNameButton=Radiobutton(self.chooseTicketWin,text=i[3],variable=self.varPassName,value=str(i[6])+"_"+str(i[3])).grid(row=2+count,column=4)
                    count=count+1
                # @ matt
                # need to get total cost of a reservation
                sql = "SELECT MIN(DepartureDate) FROM RESERVES WHERE ReservationID=%s"
            c.execute(sql, resID)
            depdate = c.fetchall()[0][0]
            today = datetime.datetime.now().date()
            delta = depdate - today
            sql = "SELECT SUM(TotalCost) FROM RESERVES WHERE ReservationID=%s"
            c.execute(sql, resID)
            tc = c.fetchall()
            tc = tc[0][0]
            ref = 0
            if delta.days <= 7 and delta.days > 1:
                ref = tc*0.5 - 50
            elif delta.days >7:
                ref = tc*0.8 - 50
            if ref < 0:
                ref = 0
            self.totalCostLabel=Label(self.chooseTicketCancelWin, text="Total Cost of Reservation").grid(row=2+count, column=0)
            self.totalCostVal=Label(self.chooseTicketCancelWin, text="${}".format(tc)).grid(row=2+count, column=1)
            # need to get current date
            self.dateOfCancel=Label(self.chooseTicketCancelWin, text="Date Of Cancellation").grid(row=3+count, column=0)
            self.dateOfCancelValue=Label(self.chooseTicketCancelWin, text="{}".format(today)).grid(row=3+count, column=1)
            # need to compare dates, calculate amount to be refunded
            self.refundLabel=Label(self.chooseTicketCancelWin, text="Amount to be Refunded").grid(row=4+count, column=0)
            self.refundVal=Label(self.chooseTicketCancelWin, text="${}".format(ref)).grid(row=4+count, column=1)

                
            self.nextBut=Button(self.chooseTicketCancelWin,text="Cancel Selected Rervation",command=self.cancelSpecificTicket).grid(row=2+count, column=6)
            self.back=Button(self.chooseTicketCancelWin,text="Back",command=self.backFromCancelSpecific).grid(row=2+count, column=5)
                
            print(3)
            #self.chooseTicketCancelWin.withdraw()
            #self.cancelwin=Toplevel()
            print(4)

        
    def cancelSpecificTicket(self):
        db = self.connect()
        c = db.cursor()
        today = datetime.datetime.now()
        yr = today.year
        month = today.month
        day = today.day
        print("Processing the cancel")
        reservationNum=self.reservationToCancel
        sql = "SELECT isCancelled FROM RESERVATION WHERE ReservationID=%s"
        c.execute(sql, reservationNum)
        data = c.fetchall()
        print(data[0][0])
        if data[0][0] == 1:
            messagebox.showwarning("Already Cancelled", "This reservation has already been cancelled.")
            self.chooseTicketCancelWin.withdraw()
            self.choose()
        else:
            sql = "SELECT MIN(DepartureDate) FROM RESERVES WHERE ReservationID=%s"
            c.execute(sql, reservationNum)
            res = c.fetchall()
            print(res[0][0])
            if yr == res[0][0].year:
                if month == res[0][0].month:
                    if (day + 1) == res[0][0].day:
                        messagebox.showwarning("Cannot Cancel", "Reservations cannot be cancelled the day before departure.")
            else:
                sql = "UPDATE RESERVATION SET isCancelled = 1 WHERE ReservationID=%s"
                resultOfCancel = c.execute(sql, (reservationNum))
                print(resultOfCancel)
            if (resultOfCancel == 1):
                messagebox.showwarning("Cancel Successful", "Your Reservation has successfully been cancelled.")
                self.chooseTicketCancelWin.withdraw()
                self.choose()
            else:
                messagebox.showwarning("Cancel Failed", "Failed to cancel reservation.  Please try again.")
                self.chooseTicketCancel


    
    def backFromCancelSpecific(self):
        self.chooseTicketCancelWin.withdraw()
        self.cancel()


    def givereview(self):
        self.cwin.withdraw()
        self.reviewwin=Toplevel()
        self.givereviewheader=Label(self.reviewwin,text="Give Review")
        self.trainnumreview=Label(self.reviewwin,text="Train Number")
        self.ratingreview=Label(self.reviewwin,text="Rating")
        self.reviewcomment=Label(self.reviewwin,text="Comment")
        self.givereviewheader.grid(row=0,column=0,columnspan=2)
        self.trainnumreview.grid(row=1,column=0)
        self.ratingreview.grid(row=2,column=0)
        self.reviewcomment.grid(row=3,column=0)
        self.reviewnumentry=Entry(self.reviewwin)
        self.reviewnumentry.grid(row=1,column=1)
        self.reviewtrainnum=self.reviewnumentry.get()
        self.commententry=Entry(self.reviewwin)
        self.commententry.grid(row=3,column=1)
        self.var4=StringVar(self.reviewwin)
        self.var4.set("")
        self.ratingentry=OptionMenu(self.reviewwin,self.var4,"Very Good","Good","Neutral","Bad","Verybad")
        self.ratingentry.grid(row=2,column=1)
        self.submitcomment=Button(self.reviewwin,text="Submit",command=self.checkreview)
        self.submitcomment.grid(row=5,column=0)
        self.backFromRev=Button(self.reviewwin,text="Back",command=self.backFromGiveReview)
        self.backFromRev.grid(row=5,column=1)

        
    def backFromGiveReview(self):
        self.reviewwin.withdraw()
        self.choose()


    def checkreview(self):
        db = self.connect()
        c = db.cursor()
        usr = self.username
        reviewID = random.randint(1, 375)
        reviewTrainNum = self.reviewnumentry.get()
        comment = self.commententry.get()
        rating = self.var4.get()
        print(reviewTrainNum)
        print(comment)
        print(rating)
        sqlAddReview = "INSERT INTO REVIEW VALUES (%s, %s, %s, %s, %s)"
        addReviewResult= c.execute(sqlAddReview, (reviewID, comment, rating, usr, reviewTrainNum))
        print(addReviewResult)
        print("added review")
        #SQL Checking if train in table
        #insert comment entry in
        #print(self.var4)


    def addschool(self):
        self.cwin.withdraw()
        self.addschool=Toplevel()
        self.addlabel=Label(self.cwin,text="Add School Info")
        self.schoollabel=Label(self.addschool,text="School Email Address")
        self.text1=Label(self.addschool,text="Your school email address ends with .edu")
        self.schoolemailentry=Entry(self.addschool)
        self.back1=Button(self.addschool,text="Back",command=self.choose)
        self.submit1=Button(self.addschool,text="Submit",command=self.emailcheck)
        self.addlabel.grid(row=0,column=0,columnspan=2)
        self.schoollabel.grid(row=1,column=0)
        self.text1.grid(row=2,column=0)
        self.schoolemailentry.grid(row=1,column=1)
        self.back1.grid(row=3,column=0)
        self.submit1.grid(row=3,column=2)

    def addschool(self):
        self.cwin.withdraw()
        self.addschool=Toplevel()
        self.addlabel=Label(self.cwin,text="Add School Info")
        self.schoollabel=Label(self.addschool,text="School Email Address")
        self.text1=Label(self.addschool,text="Your school email address ends with .edu")
        self.schoolemailentry=Entry(self.addschool)
        self.back1=Button(self.addschool,text="Back",command=self.backfromaddschool)
        self.submit1=Button(self.addschool,text="Submit",command=self.emailcheck)
        self.addlabel.grid(row=0,column=0,columnspan=2)
        self.schoollabel.grid(row=1,column=0)
        self.text1.grid(row=2,column=0)
        self.schoolemailentry.grid(row=1,column=1)
        self.back1.grid(row=3,column=0)
        self.submit1.grid(row=3,column=2)
        
    def backfromaddschool(self):
        self.addschool.destroy()
        self.choose()

    def emailcheck(self):
        db = self.connect()
        c = db.cursor()
        usr = self.username
        emailEntry = self.schoolemailentry.get()
        if ".edu" in emailEntry:
            sql = "UPDATE CUSTOMER SET isStudent = 1 WHERE Username=%s"
            addStudentResult=c.execute(sql, usr)
            if (addStudentResult != 0):
                messagebox.showwarning("Success", "Successfully Added Student Discount!")
            else:
                messagebox.showwarning("Failure", "Already had a Student Discount!")
        else:
            messagebox.showwarning("Failure", "Failed to Add Student Discount!")
        self.addschool.withdraw()
        self.choose()
    def viewReview(self):
        self.cwin.withdraw()
        self.viewReviewWin=Toplevel()
        self.viewReviewTitle=Label(self.viewReviewWin,text="View Review").grid(row=0,column=0, columnspan=2)
        self.trainNumLabel=Label(self.viewReviewWin, text="Train Number:").grid(row=1, column=0)
        self.trainNumEntry1=Entry(self.viewReviewWin)
        self.trainNumEntry1.grid(row=1, column=1)
        self.nextBut=Button(self.viewReviewWin, text="Next", command=self.viewReviewTrainNum).grid(row=2, column=1)
        self.backBut=Button(self.viewReviewWin, text="Back", command=self.backFromViewReview).grid(row=2, column=0)

    def backFromViewReview(self):
        self.viewReviewWin.withdraw()
        self.choose()
    
    def viewReviewTrainNum(self):
        trainNum = self.trainNumEntry1.get()
        self.viewReviewWin.withdraw()
        self.viewReviewResultsWin=Toplevel()
        self.viewReviewTitle=Label(self.viewReviewResultsWin,text="View Review").grid(row=0,column=0, columnspan=2)
        self.ratingTitle=Label(self.viewReviewResultsWin,text="Rating").grid(row=1,column=0)
        self.commentTitle=Label(self.viewReviewResultsWin,text="Comment").grid(row=1,column=1)
        db = self.connect()
        c = db.cursor()
        sql = "SELECT Rating, Comment FROM REVIEW WHERE TrainNumber=%s"
        reviews = c.execute(sql, trainNum)
        data = c.fetchall()
        count =0
        for i in data:
            self.trainNumberLab=Label(self.viewReviewResultsWin,text=i[0]).grid(row=2+count,column=0)
            self.departDate=Label(self.viewReviewResultsWin,text=i[1]).grid(row=2+count,column=1)
            count=count+1
        print(trainNum)
        self.backBut=Button(self.viewReviewResultsWin, text="Back", command=self.backFromViewReviewResults).grid(row=2+count, column=0)

    def backFromViewReviewResults(self):
        self.viewReviewResultsWin.withdraw()
        self.choose()
        

    def logout(self):
        self.cwin.withdraw()
        self.entry1.delete(0,'end')
        self.entry2.delete(0,'end')
        self.win.deiconify()

        
    def getTotalCost(bags, classLevel, trainNum):
        mysql = db.cursor()
        sql = """ SELECT FirstClassPrice, SecondClassPrice FROM TRAIN_ROUTE WHERE TrainNumber=%s"""
        mysql.execute(sql, str(trainNum))
        fields=mysql.fetchall()
        #print(fields)
        for f in fields:
            priceFirst=f[0]
            priceSecond=f[1]
        cost=0 
        if (classLevel=="First"):
            cost+= int(priceFirst)
        else:
            cost+= int(priceSecond)
        if bags > 2:
            if (bags == 3):
                cost+=30
                return cost
            else:
                cost+=60
                return cost
        else:
            return cost

win=Tk()
win.title("GTTrain.com")
analysis = Reservation()
win.mainloop()


