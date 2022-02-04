import tkinter as tk
from tkinter import Frame, StringVar, Toplevel
from tkinter import messagebox as mb
import bcrypt
from mysqlx import Row
from connection import *
from mysql.connector import Error

import random
from codebase import *


window = tk.Tk()
window.geometry('400x350')
window.title('Welcome Page')
window.configure(bg='#001f3f')
# window.eval('tk::PlaceWindow . center')

base_frame = Frame(window,bg='#001f3f').pack()
login_frame = Frame(window,bg='#001f3f')
register_frame = Frame(window,bg='#001f3f')
home_frame = Frame(window,bg='#001f3f')
login_frame = Frame(window)

# Create connection to database
connection = db_connect()
try :
    connection
except Error as e:
    print(e)

cursor = connection.cursor()
frames = {}
frames_list = [home_frame,register_frame,login_frame]

###################################

for F in frames_list:
    frame = F
    
    frames[F] = frame
    
def home():

    current = home_frame
    tk.Button(current,text='Login',bg='green',fg='#fff',command=lambda:show_frame(login_frame)).pack(pady=3)
    tk.Button(current,text='Register',command=lambda:show_frame(register_frame)).pack()

def login():
    current = login_frame

    tk.Label(login_frame,text='Email address',bg='#001f3f',fg='#fff').pack()
    email_str = tk.StringVar()
    email_entry = tk.Entry(login_frame,textvariable=email_str)
    email_entry.pack()
    email_entry.focus_set()

    tk.Label(current,text='Password',bg='#001f3f',fg='#fff').pack()
    password = tk.StringVar()
    tk.Entry(current,textvariable=password,show='*').pack()
    
    def login_user():
        email = email_str.get()
        u_pass = password.get()
        if email == '':
            mb.showinfo('Information','Please Enter Email address')
        if u_pass == '':
            mb.showinfo('Information','Please Enter Password')
        g_query = """
            SELECT password FROM users
            WHERE email = '%s'
            """ %(email)
        cursor =connection.cursor()
        cursor.execute(g_query)

        res = []
        for pdt in cursor.fetchall():
                u,*z = pdt
                res.append(u)

        if len(res) != 0 :
            if bcrypt.checkpw(u_pass.encode('utf-8'),res[0].encode()):
                mb.showinfo('Information','Login Successful')
                # login_screen.destroy()
                get_fname = """
                    SELECT firstname FROM users
                    WHERE email = '%s'
                """%(email)
                cursor.execute(get_fname)
                result = []
                for pdt in cursor.fetchall():
                    u,*z = pdt
                    result.append(u)
                dashboard(result[0])
            else:
                mb.showerror('Error!','Invalid login credentials')
        else:
            mb.showerror('Error!','Invalid login credentials')
        
    # login_screen.bind('<Return>',login_user)      
    
    tk.Button(login_frame,text='Login User',command=login_user).pack(pady=3)
    tk.Button(login_frame,text='A new User ? Register',command=lambda:show_frame(register_frame),bg='#001f3f',fg='#fff').pack()
    
def register():
    current = register_frame

 
    global email_str
    global password

    password = StringVar()
    email = StringVar()
    firstname = StringVar()
    lastname = StringVar()
    
    tk.Label(register_frame,text='Firstname',bg='#001f3f',fg='#fff').pack()
    tk.Entry(register_frame,textvariable=firstname).pack()

    tk.Label(register_frame,text='Lastname',bg='#001f3f',fg='#fff').pack()
    tk.Entry(register_frame,textvariable=lastname).pack()

    tk.Label(register_frame,text='Email',bg='#001f3f',fg='#fff').pack()
    tk.Entry(register_frame,textvariable=email).pack()

    tk.Label(register_frame,text='Password',bg='#001f3f',fg='#fff').pack()
    tk.Entry(register_frame,textvariable=password,show='*').pack()

    def register_user():
        pass_u = password.get()
        fname = firstname.get()
        lname = lastname.get()
        mail = email.get()
        user = User(fname,lname,mail,pass_u)
        user.create_user()

    tk.Button(register_frame,text='Register User',command=register_user).pack(pady=4)
    tk.Button(register_frame,text='Already a User ? Login',command=lambda:show_frame(login_frame),bg='#001f3f',fg='#fff').pack()

###################################

tk.Button(window,text='Back to Home',bg='#001f3f',fg='#fff').pack()

def show_frame(name):
    name.pack()

show_frame(home_frame)
print(frames)
window.mainloop()



def listStockProducts():
    stock_window = Toplevel(window)
    stock_window.geometry('420x540')
    stock_window.title('Stock Products')
    # stock_window.eval('tk::PlaceWindow . center')

    tk.Label(stock_window,text='S/N').grid(row=0,column=0)
    tk.Label(stock_window,text='Barcode').grid(row=0,column=1)
    tk.Label(stock_window,text='Title').grid(row=0,column=2)
    tk.Label(stock_window,text='Quantity').grid(row=0,column=3)
    get_stock = """ 
       SELECT barcode,title,quantity
       FROM stock
       """
    cursor.execute(get_stock)
    products = cursor.fetchall()

    for count,product in enumerate(products):
        tk.Label(stock_window,text=count+1).grid(row=count+1,column=0)
        tk.Label(master=stock_window,text=product[0]).grid(row=count+1,column=1)
        tk.Label(master=stock_window,text=product[1]).grid(row=count+1,column=2)
        tk.Label(master=stock_window,text=product[2]).grid(row=count+1,column=3)
    #     # # # ock_btn = tk.Button(window,text='View Stocks',bg='red',fg='#fff').pack(pady=2)

def dashboard(user):
    
    dash_window = Toplevel()
    dash_window.geometry('420x540')
    dash_window.title('Dashboard')

    username = f'User : {user}!'
    user_label = tk.Label(dash_window,text=username,font=('Arial',12))
    user_label.grid(row=0,column=0)

    tk.Label(dash_window,text='Barcode').grid(row=1,column=0)
    tk.Label(dash_window,text='Quantity').grid(row=1,column=2)