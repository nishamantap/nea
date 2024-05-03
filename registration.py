import pymysql
from tkinter import *
from tkinter import messagebox
import sqlite3

#creates the window for the text, buttons and entry fields to be displayed on
windows = Tk()
windows.title('registration')
windows.geometry('550x400+200+10')
windows.resizable(0,0)

#function linked to thego to login button , taking you from registaration to login
def gotologin():
    windows.destroy()
    import login


#database connection using sqlite3, making a database with email, firstname,password and confirm password as the fields
connection = sqlite3.connect('regLog.db')
cur = connection.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS regLog(email TEXT , fname TEXT, password TEXT,cpassword TEXT)")
connection.commit()
connection.close()

# event handling , if any of the following fields are empty, they send an alert that everything has to be filled in
#function linked with the submit button , creating a new account

def submit():
    check_counter = 0
    warn = ""
    if fnameentry.get() == "":
        warn = "Full Name can't be empty"
    else:
        check_counter += 1

    if emailentry.get() == "":
        warn = "Email Field can't be empty"
    else:
        check_counter += 1

    if passwordentry.get() == "":
        warn = "Password can't be empty"
    else:
        check_counter += 1

    if cpasswordentry.get() == "":
        warn = "Sorry, can't sign up make sure all fields are complete"
    else:
        check_counter += 1

    if passwordentry.get() != cpasswordentry.get():
        warn = "Passwords didn't match!"
    else:
        check_counter += 1

    if check_counter == 5:
        try:
            connection = sqlite3.connect("regLog.db")
            cur = connection.cursor()
            cur.execute("INSERT INTO regLog(email, fname, password, cpassword) VALUES (?, ?, ?, ?)",
            (emailentry.get(), fnameentry.get(), passwordentry.get(), cpasswordentry.get()))
            connection.commit()
            connection.close()
            messagebox.showinfo("Success", "New account created successfully")

        except Exception as ep:
            messagebox.showerror('', ep)
    else:
        messagebox.showerror('Error', warn)



#functions relating to the checkboxes to hide or unhide the password upon entering

def show1():
    passwordentry.configure(show = '*')
    check1.configure(command = hide1)

def hide1():
    passwordentry.configure(show='')
    check1.configure(command = show1)

def show2():
    cpasswordentry.configure(show = '*')
    check2.configure(command = hide2)

def hide2():
    cpasswordentry.configure(show='')
    check2.configure(command = show2)



#main frame
frame = Frame(windows,width = 610,height=640,bg='#ffccff',bd = 8)
frame.place(x=0,y=0)

#labeles for login page
heading = Label(frame, text = 'registration', fg ='black',bg = '#ffccff',font = ('calibre',20,'bold'))
heading.place(x=90, y = 30)

fnamelbl = Label(frame, text = 'first name: ', fg ='black',bg = '#ffccff',font = ('calibre',20,'bold'))
fnamelbl.place(x=10, y = 70)

fnameentry = Entry(frame,width = 30, borderwidth = 2 )
fnameentry.place(x=240, y = 80)

emaillbl = Label(frame, text = 'email: ', fg ='black',bg = '#ffccff',font = ('calibre',20,'bold'))
emaillbl.place(x=10, y = 100)

emailentry = Entry(frame,width = 30, borderwidth = 2 )
emailentry.place(x=240, y = 110)

passwordlbl = Label(frame, text = 'password: ', fg ='black',bg = '#ffccff',font = ('calibre',20,'bold'))
passwordlbl.place(x=10, y = 130)

passwordentry = Entry(frame,width = 30, borderwidth = 2 )
passwordentry.place(x=240, y = 140)

cpasswordlbl = Label(frame, text = 'confirm password: ', fg ='black',bg = '#ffccff',font = ('calibre',20,'bold'))
cpasswordlbl.place(x=10, y = 160)

cpasswordentry = Entry(frame,width = 30, borderwidth = 2 )
cpasswordentry.place(x=270, y = 170)



#button to register
submitbtn = Button(frame, text = 'register', width = 15, borderwidth = 5, height = 2 ,bg = 'purple', fg = 'white',
                   cursor = 'hand2', border = 2, command =submit )
submitbtn.place(x = 220, y =300)

Lbtn = Button(frame, text = 'go to login', width = 15, borderwidth = 10, height = 2 ,bg = 'purple', fg = 'white',
                   cursor = 'hand2', border = 2, command = gotologin)

Lbtn.place(x = 0, y =325)
#button to swicth the password to asteriks
check1 = Checkbutton(frame, text ='', bg ='#ffccff',command = show1)
check1.place(x=430, y = 140)

check2 = Checkbutton(frame, text ='', bg ='#ffccff', command = show2)
check2.place(x=460, y = 170)



windows.mainloop()
