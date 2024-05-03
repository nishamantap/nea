import pymysql
from tkinter import *
from tkinter import messagebox
import sqlite3

#creates teh window for the text, buttons and entry fields to be displayed on

windows = Tk()
windows.title('registration')
windows.geometry('550x400+200+10')
windows.resizable(0,0)

#function relating to the go to login button , taking you to the login page after the password has been reset

def backtologin():
    windows.destroy()
    import login

# function that update the details in the databse , changing the password field if the email matches
def changepassword():
    conn = sqlite3.connect("regLog.db")
    cursor = conn.cursor()

    email = emailentry.get()  # Retrieve the email entered by the user
    new_password = passwordentry.get()  # Retrieve the new password entered by the user

    # Update the password in the database for the given email
    sql_update_query = """UPDATE reglog.db SET password = ? WHERE email = ?"""
    messagebox.showinfo('alert','password changed')
    cursor.execute(sql_update_query, (new_password, email))

    conn.commit()  # Commit the changes
    conn.close()

#frame design
frame = Frame(windows,width = 610,height=640,bg='#ffccff',bd = 8)
frame.place(x=0,y=0)

heading = Label(frame, text = 'change password', fg ='black',bg = '#ffccff',font = ('calibre',20,'bold'))
heading.place(x=90, y = 30)

#labels for the window

emaillbl = Label(frame, text = 'email: ', fg ='black',bg = '#ffccff',font = ('calibre',20,'bold'))
emaillbl.place(x=10, y = 130)

emailentry = Entry(frame,width = 30, borderwidth = 2 )
emailentry.place(x=100, y = 140)

passwordlbl = Label(frame, text = 'password: ', fg ='black',bg = '#ffccff',font = ('calibre',20,'bold'))
passwordlbl.place(x=10, y = 160)

passwordentry = Entry(frame,width = 30, borderwidth = 2 )
passwordentry.place(x=160, y = 170)

#buttons taking you from forgot password to login page , or directly logging in
Lbtn = Button(frame, text = 'change password', width = 15, borderwidth = 10, height = 2 ,bg = 'purple', fg = 'white',
                   cursor = 'hand2', border = 2, command = changepassword)

Lbtn.place(x = 170, y =300)

gotoLtn = Button(frame, text = 'back to login', width = 15, borderwidth = 10, height = 2 ,bg = 'purple', fg = 'white',
                   cursor = 'hand2', border = 2, command = backtologin)

gotoLtn.place(x = 0, y =325)





windows.mainloop()
