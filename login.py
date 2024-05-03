import pymysql
from tkinter import *
from tkinter import messagebox
import sqlite3

#creates teh window for the text, buttons and entry fields to be displayed on

windows = Tk()
windows.title('registration')
windows.geometry('550x400+200+10')
windows.resizable(0,0)

#function relating to the go to registration button , taking you to the registration page if you have not made an account

def register():
    windows.destroy()
    import registration

#login function checking your details against the databse to make sure the correct credentials have been entered,
#which will then take you onto the login page

def login():
    conn = sqlite3.connect("regLog.db")
    cursor = conn.cursor()

    find_user = 'SELECT * FROM regLog WHERE Email = ? and Password = ?'
    cursor.execute(find_user, [(emailentry.get()), (passwordentry.get())])

    result = cursor.fetchall()
    if result:
        #show_frame(Homepage)
        messagebox.showinfo("Success", 'Logged in Successfully.')


    else:
        #messagebox.showinfo(result.get)
        messagebox.showerror("Wrong Login details, please try again.")



#frame design

frame = Frame(windows,width = 610,height=640,bg='#ffccff',bd = 8)
frame.place(x=0,y=0)

heading = Label(frame, text = 'login', fg ='black',bg = '#ffccff',font = ('calibre',20,'bold'))
heading.place(x=90, y = 30)

#login labels

emaillbl = Label(frame, text = 'email: ', fg ='black',bg = '#ffccff',font = ('calibre',20,'bold'))
emaillbl.place(x=10, y = 130)

emailentry = Entry(frame,width = 30, borderwidth = 2 )
emailentry.place(x=100, y = 140)

passwordlbl = Label(frame, text = 'password: ', fg ='black',bg = '#ffccff',font = ('calibre',20,'bold'))
passwordlbl.place(x=10, y = 160)

passwordentry = Entry(frame,width = 30, borderwidth = 2 )
passwordentry.place(x=160, y = 170)

#login buttons to go to the registration page, to got to landing page and to the forgot password page

submitbtn = Button(frame, text = 'login', width = 15, borderwidth = 5, height = 2 ,bg = 'purple', fg = 'white',
                   cursor = 'hand2', border = 2, command =login)
submitbtn.place(x = 220, y =300)

toregisterbtn = Button(frame, text = 'make an account', width = 15, borderwidth = 5, height = 2 ,bg = 'purple', fg = 'white',
                   cursor = 'hand2', border = 2, command =register)
toregisterbtn.place(x = 80, y =300)

topassbtn = Button(frame, text = 'forgot password?', width = 15, borderwidth = 5, height = 2 ,bg = 'purple', fg = 'white',
                   cursor = 'hand2', border = 2, command =register)
topassbtn.place(x = 350, y =300)



windows.mainloop()
