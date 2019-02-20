import tkinter as tk
from tkinter import messagebox, simpledialog,StringVar
from datetime import datetime
from tkinter import ttk
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib import animation
import pandas as pd
import os, sqlite3
import datetime as dt

from elcf_resources_and_tools import User
from elcf_resources_and_tools import Database
import numpy as np

'''
    'bmh', 'classic', 'dark_background', 'fast', 'fivethirtyeight', 'ggplot', 'grayscale',
    'seaborn-bright', 'seaborn-colorblind', 'seaborn-dark-palette', 'seaborn-dark',
    'seaborn-darkgrid', 'seaborn-deep', 'seaborn-muted', 'seaborn-notebook', 'seaborn-paper',
    'seaborn-pastel', 'seaborn-poster', 'seaborn-talk', 'seaborn-ticks', 'seaborn-white',
    'seaborn-whitegrid', 'seaborn', 'Solarize_Light2', 'tableau-colorblind10', '_classic_test'
'''

style.use('seaborn-darkgrid')


f = Figure(figsize=(8,5), dpi=100)
f.patch.set_facecolor("#513d77")
a = f.add_subplot(111)
a.tick_params(axis='x', colors='gold')
a.tick_params(axis='y', colors='gold')

# Animation function---------------------------------------------------------------------------
def animate(i):
    file = open("database_folder/data.txt", "r").read()
    data = file.split("\n")
    xs = []
    ys = []
    for line in data:
        if len(line) > 1:
            x,y = line.split(',')
            xs.append(x[2:10])
            ys.append(int(y))
    a.clear()
    a.plot_date(xs, ys, 'green',label='Sunday Attendance')
    a.legend()


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # CREATING MAIN GUI---------------------------------------------------------------------------
        self.geometry("1000x600+100+20")    # Setting window size with geometry widget
        self.title("EAST LONDON CHRISTIAN FELLOWSHIP`")  # Setting title
        self.minsize(1008, 600) # setting default wn minimum size

        time_frame = tk.Frame(self, bg="#513d77") # main frame
        time_frame.pack(side='top', fill='x')

        Database.Database()

        # Creating a timer for the window below
        self.count=0
        def time_counter(label):
            def counter():
                self.count += 1
                label.config(text=str(datetime.now().strftime("%H:%M:%S %d-%m-%Y")))
                label.after(1000, counter)
            counter()

        # Creating a time label on the top right corner of the application
        time_label = tk.Label(time_frame, fg="gold",font=("Tahoma", 11,), bg="#513d77")
        time_label.pack(side='top', anchor='e')

        time_counter(time_label)

        # Creating a container frame
        container = tk.Frame(self)
        container.pack(fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Setting up a dict for all the windows
        self.frames = {}
        for F in (PasswordPage, StartPage, Registration, Diary, Programs,Administrator,Register,Youth):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='sewn')

        self.showframe(PasswordPage)

    def showframe(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# Password page---------------------------------------------------------------------------------------------------

class PasswordPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        exit_btn = tk.Button(self, text='Exit',fg='turquoise',font=('Verdana', 11),relief='flat',bg="#514d77",
                             width=15, command=exit)
        exit_btn.pack(anchor='e')

        # configuring background color-------------------------------------------------------------------------------
        self.configure(bg='#513d77')

        def login():
            user = usr_entry.get()
            password = password_entry.get()
            access = User.User_Login.login_user(user,password)
            if access:
                usr_entry.delete(0, 'end')
                password_entry.delete(0, 'end')
                controller.showframe(StartPage)
            else:
                usr_entry.delete(0, 'end')
                password_entry.delete(0, 'end')
                messagebox.showerror('elcf password detector', "\tPASSWORD INVALID\t\t")

        # Label for the main title in home page
        label_top = tk.Label(self, text="East London Christian Fellowship", bg="#513d77",fg="yellow", font=("Tahoma", 30,))
        label_top.place(y=200)

        label_bottom = tk.Label(self, text="'Family Church'", fg="yellow", font=("Tahoma", 20,'italic'),bg="#513d77")
        label_bottom.place(y=250)

        #-------USERNAME & PASSWORD-------------------------------------------------------------------------
        usr_entry = tk.Entry(self, font=('Verdana', 14))
        usr_entry.place(y=256, x=200)

        password_entry = tk.Entry(self, font=('Verdana', 14), show='*',justify='center',width=10)
        password_entry.place(y=290, x=200)
        #-----------------------------------------------------------------------------------------------
        password_btn = tk.Button(self, text='Login' ,font=('Verdana', 11),relief='flat',bg="#51fd77",width=20,command=login)
        password_btn.place(y=253, x=450)

        mission_statement_frame = tk.Frame(self,bg="#514d77")
        mission_statement_frame.place(y=20, x=200)

        mission = tk.Label(mission_statement_frame, text = 'MISSION',bg="#514d77", font=('Arial',16,'italic'),
                           fg='turquoise')
        mission.pack()

        mission_statement = tk.Label(mission_statement_frame,font=('Arial',12,'italic'),
                            text = 'To preach the good news of the gospel of God\'s Kingdom to everyone.\n'\
                            'To equip and bring to maturity Born-again individuals preparing them to serve in God\'s Kingdom.\n'
                            ,bg="#514d77", fg="orange")
        mission_statement.pack()

        vision_statement_frame = tk.Frame(self,bg="#814d77")
        vision_statement_frame.place(y=100, x=600)

        vision = tk.Label(vision_statement_frame, text = 'VISION',bg="#814d77", font=('Arial',16,'italic'),fg='yellow')
        vision.pack()

        vision_statement = tk.Label(vision_statement_frame,font=('Arial',12,'italic'),
                        text = 'We are a church that has purposed ourselves to fulfilling the GREAT COMMISSION.\n'\
                               'Mathew 28 v 19  Col 1 v 28 - 29  Is 61 v 1 - 4 _ 8-9.\n'\
                               '1. Making disciples of all nations.\n'\
                               '2. Caring and presenting everyone mature in Christ.\n'\
                               '3. Leaving a legacy of blessings, prosperity and justice for future generations.\n'
                               ,bg="#814d77", fg="yellow")
        vision_statement.pack()

        acts_frame = tk.Frame(self,bg="#514d37")
        acts_frame.place(y=250, x=880)

        acts = tk.Label(acts_frame, text = 'Acts 13 v 2-3',bg="#514d37", font=('Arial',16,'italic'),fg='skyblue')
        acts.pack()

        acts_statement = tk.Label(acts_frame,font=('Arial',12,'italic'),
                            text = 'WE ARE A SENDING CHURCH.\n'\
                            '1. Missions.\n'\
                            '2. Church planting.\n'

                            ,bg="#514d37", fg="white")
        acts_statement.pack()

        networking_frame = tk.Frame(self,bg="#514d77")
        networking_frame.place(y=340, x=500)

        networking = tk.Label(networking_frame, text = 'NETWORKING',bg="#514d77", font=('Arial',16,'italic'))
        networking.pack()

        networking_statement = tk.Label(networking_frame,font=('Arial',12,'italic'),
                            text = '1. It is our aim to build relationships and actively interact with other Churches in our community and City.\n'
                            '2. To see the body of Christ united.\n'

                            ,bg="#514d77", fg="skyblue")
        networking_statement.pack()

# -------------------------------------------------------------------------------------------------------------------------------

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # configuring background color
        self.configure(bg="#513d77")

        # Label for the main title in home page
        label_top = tk.Label(self, text="East London Christian Fellowship", bg="#513d77",
                         fg="yellow", font=("Tahoma", 20,))
        label_top.pack()

        label_bottom = tk.Label(self, text="'Family Church'", fg="white", font=("Tahoma", 15,'italic'), bg="#513d77")
        label_bottom.pack()

        # this frame holds all the navigation buttons on the Main page
        my_btn_frame = tk.Frame(self, bg="black", relief="raised", bd=1)
        my_btn_frame.pack(anchor='n')

        # Front navigation buttons-------------------------------------------------------------------------

        def admin():
            my_font = ('Verdana', 12)
            log_in_window = tk.Tk()
            log_in_window.title('Access Window')
            log_in_window.resizable(False,False)
            log_in_window.geometry('500x120+400+250')

            def my_admin():
                access = User.User_Login.login_user(user_name_entry.get(), password_name_entry.get())
                if access:
                    user_name_entry.delete(0, 'end')
                    password_name_entry.delete(0, 'end')
                    log_in_window.destroy()
                    controller.showframe(Administrator)
                else:
                    user_name_entry.delete(0, 'end')
                    password_name_entry.delete(0, 'end')
                    messagebox.showerror('elcf password detector', '\tPASSWORD INVALID\t\t')

            user_name_entry = tk.Entry(log_in_window, font=my_font, width=40)
            user_name_entry.pack()
            user_name_label = tk.Label(log_in_window, text='Username', font=my_font)
            user_name_label.pack()

            password_name_entry = tk.Entry(log_in_window, show='*', font=my_font, justify='center')
            password_name_entry.pack()
            password_name_label = tk.Label(log_in_window, text='Password', font=my_font)
            password_name_label.pack()

            enter_button = ttk.Button(log_in_window, text='Enter', command=my_admin)
            enter_button.pack()
            log_in_window.mainloop()

        font=('Verdana', 11,)
        btn = tk.Button(my_btn_frame, text="REGISTRATION", font=font, width=15, relief="flat", bg="black",fg='gold',
                        command=lambda: controller.showframe(Registration))
        btn.pack(side='left')

        line1 = tk.Label(my_btn_frame,text='|',bg='black',fg='gold')
        line1.pack(side='left')

        btn1 = tk.Button(my_btn_frame, text="DIARY", font=font, width=15, relief="flat", bg="black",fg='gold',
                         command=lambda: controller.showframe(Diary))
        btn1.pack(side='left')

        line2 = tk.Label(my_btn_frame,text='|',bg='black',fg='gold')
        line2.pack(side='left')

        btn2 = tk.Button(my_btn_frame, text="PROGRAMMES", font=font, width=15, relief="flat", bg="black",fg='gold',
                         command=lambda: controller.showframe(Programs))
        btn2.pack(side='left')

        line3 = tk.Label(my_btn_frame,text='|',bg='black',fg='gold')
        line3.pack(side='left')

        btn3 = tk.Button(my_btn_frame, text="ADMIN", font=font, width=15, relief="flat", bg="black",fg='gold',
                         command=admin)
        btn3.pack(side='left')

        line4 = tk.Label(my_btn_frame,text='|',bg='black',fg='gold')
        line4.pack(side='left')

        btn4 = tk.Button(my_btn_frame, text="YOUTH", font=font, width=15, relief="flat", bg="black", fg='gold',
                         command=lambda: controller.showframe(Youth))
        btn4.pack(side='left')

        line5 = tk.Label(my_btn_frame, text='|', bg='black', fg='gold')
        line5.pack(side='left')

        btn5 = tk.Button(my_btn_frame, text="LOGOUT", font=font, width=15, relief="flat", bg="black",fg='gold',
                         command=lambda: controller.showframe(PasswordPage))
        btn5.pack(side='left')

        # ------------------------------------------------------------------------------------------------------
        events_frame = tk.Frame(self)
        events_frame.pack(fill='x')

        df = pd.DataFrame('',
                            ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'],
                            ['Program/Event title','Host','Venue','Time'])
        events_scr_bar = tk.Scrollbar(events_frame)
        events_scr_bar.pack(side='right')

        events_text = tk.Text(events_frame, height=4,fg='white', bg="black",yscrollcommand=events_scr_bar.set,
                              font=('Verdana',9))
        events_text.pack(expand=True,fill='x')
        events_text.insert(.0, df)
        events_scr_bar.config(command=events_text.yview)


        calendar_frame = tk.Frame(self,bg="#513d77")
        calendar_frame.pack(fill='x')


class Registration(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.configure(bg="#513d77")

        label = tk.Label(self, text="Registration", bg="#513d77", fg="yellow", font=("Tahoma", 20,))
        label.pack()

        btn = tk.Button(self, text="Home", font=("Verdana", 11),relief="groove", width=20,fg='gold', bg="#513d77",
                        command=lambda: controller.showframe(StartPage))
        btn.pack(anchor='w')

        #line_break = tk.Frame(self, bg='gold')
        #line_break.pack(fill='x')
        # FORM SEGMENT ============================================================================================
        font = ('Tahoma', 16,)

        def register():
            db = Database.Database()
            db.register_new_member(first_name_entry.get(),middle_name_entry.get(),last_name_entry.get(),
                                   phone_entry.get(),f"{date_entry.get()}/{month_entry.get()}/{year_entry.get()}",
                                   gender_entry.get(),address_number_entry.get())
            first_name_entry.delete(0, 'end')
            middle_name_entry.delete(0, 'end')
            last_name_entry.delete(0, 'end')
            phone_entry.delete(0, 'end')
            date_entry.delete(0,'end')
            month_entry.delete(0, 'end')
            year_entry.delete(0, 'end')
            gender_entry.delete(0, 'end')
            address_number_entry.delete(0, 'end')

        # Registration form------------------------------------------------------------------------------------

        form_frame = tk.Frame(self, bg="black")
        form_frame.pack(expand=True, fill='both',anchor='center')

        #first_name_var = StringVar()
        first_name_entry = tk.Entry(form_frame, width=48, font=font, fg="#513d77")
        first_name_entry.pack()

        first_name_label = tk.Label(form_frame, text="First Name: ", font=font, bg="black", fg="yellow")
        first_name_label.pack()

        #middle_name_var = StringVar()
        middle_name_entry = tk.Entry(form_frame, width=48, font=font, fg="#513d77")
        middle_name_entry.pack()

        middle_name_label = tk.Label(form_frame, text="Middle Name: ", font=font, bg="black", fg="yellow")
        middle_name_label.pack()

        #last_name_var = StringVar()
        last_name_entry = tk.Entry(form_frame, width=48, font=font, fg="#513d77")
        last_name_entry.pack()

        last_name_label = tk.Label(form_frame, text="Last Name: ", font=font, bg="black", fg="yellow")
        last_name_label.pack()

        #phone_var = StringVar()
        phone_entry = tk.Entry(form_frame, width=30,font=font, fg="#513d77")
        phone_entry.pack()

        phone_label = tk.Label(form_frame, text="Cell number: ", font=font, bg="black", fg="yellow")
        phone_label.pack()

        date_frame = tk.Frame(form_frame)
        date_frame.pack()

        #date_var = StringVar()
        date_entry = ttk.Combobox(date_frame, width=3, font=font)
        date_entry['values'] = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31)
        date_entry.pack(side='left')

        #month_var = StringVar()
        month_entry = ttk.Combobox(date_frame, width=10, font=font)
        month_entry['values'] = ('January','February','March','April','May','June','July','August','September',
                                 'October','November','December' )
        month_entry.pack(side='left')

        #year_var = StringVar()
        year_entry = ttk.Combobox(date_frame, width=5, font=font)
        year_entry['values'] = ([i for i in range(1900, 8001)])
        year_entry.pack(side='left')

        date_of_birth_label = tk.Label(form_frame, text="DOB: ", font=font, bg="black", fg="yellow")
        date_of_birth_label.pack()

        #gender_var = StringVar()
        gender_entry = ttk.Combobox(form_frame,width=6, font=font)
        gender_entry['values'] = ('Male', 'Female')
        gender_entry.pack()

        gender_label = tk.Label(form_frame, text="Gender: ", font=font, bg="black", fg="yellow")
        gender_label.pack()

        #address_var = StringVar()
        address_number_entry = tk.Entry(form_frame, width=48,font=font, fg="#513d77")
        address_number_entry.pack()

        address_number_label = tk.Label(form_frame, text='Home address', font=font, bg="black", fg="yellow")
        address_number_label.pack()

        register_btn = tk.Button(form_frame, text="Register", font=font, width=30,relief="groove", bg="gold",
                                 command=register)
        register_btn.pack()


class Diary(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.configure(bg="#513d77")

        label = tk.Label(self, text="Diary", bg="#513d77", fg="yellow", font=("Tahoma", 20,))
        label.pack()

        btn = tk.Button(self, text="Home", font=("Verdana", 11), relief="groove",fg='gold', bg="#513d77", width=20,
                        command=lambda: controller.showframe(StartPage))
        btn.pack(anchor='w')

        # Creating a notebook from ttk==========================================================
        col=ttk.Style().configure("TNotebook", background="#513d77", foreground='green', borderwidth=3,
                                  lightcolor='gold')
        notebook = ttk.Notebook(self, style=col)
        notebook.pack(fill='both', expand=True)

        # ----------------------FIRST PAGE------------------------------------------------------------------------

        font = ('Verdana', 13,)
        first_page = tk.Frame(notebook, relief='groove', bg="#513d77")
        first_page.pack()

        form_frame = tk.Frame(first_page, bg="#513d77", relief='groove', bd=1)
        form_frame.pack(expand=True)

        entry_title = tk.Label(form_frame, font=font,fg='gold', text='Entry title', bg="#513d77")
        entry_title.grid(row=0, column=0)
        entry_title_entry = tk.Entry(form_frame, font=font)
        entry_title_entry.grid(row=0, column=1, sticky='w')
        entry_title_entry = tk.Checkbutton(form_frame, font=font, text='Set datetime to now', bg="#513d77")
        entry_title_entry.grid(row=1, column=1, sticky='w')

        entry_text = tk.Label(form_frame, font=font, text='Text', bg="#513d77",fg='gold')
        entry_text.grid(row=2, column=0)
        scr_bar = tk.Scrollbar(form_frame)
        scr_bar.grid(row=3, column=2, sticky='ns')
        entry_text_entry = tk.Text(form_frame, font=font, width=60, height=12, yscrollcommand=scr_bar.set)
        entry_text_entry.grid(row=3, column=1)
        scr_bar.config(command=entry_text_entry.yview)

        update_btn = tk.Button(form_frame, text='Update diary', width=20, bg='gold', font=font)
        update_btn.grid(row=4, column=1)

        notebook.add(first_page, text='Diary Entry\t')

        # -----------------------Sunday register------------------------------------------------------------

        main_service_frame = tk.Frame(notebook, bg="#513d77")
        main_service_frame.pack()

        register_frame = tk.Frame(main_service_frame, bg="#513d77")
        register_frame.pack(side='top')

        def sunday_register():
            Database.MainServiceRegister(datetime.now(),adults_entry.get(),children_entry.get(),
                                                    visitors_entry.get(),notes_text_entry.get(0., 'end'))
            adults_entry.delete(0, 'end')
            children_entry.delete(0, 'end')
            visitors_entry.delete(0, 'end')
            notes_text_entry.delete(0., 'end')

        def fin():
            pass
            #password = simpledialog.askinteger('Password', 'Please enter authorization pin')

        clear_btn = tk.Button(register_frame, text='Clear form', relief='flat',bg="#513d78", fg='gold', font=font,
                              command=fin)
        clear_btn.grid(row=0, column=1,columnspan=2)

        adults_label = tk.Label(register_frame,text='Adults', bg="#513d77", font=font,fg='gold')
        adults_label.grid(row=1,column=0,sticky='e')
        adults_entry = tk.Entry(register_frame,)
        adults_entry.grid(row=1,column=1,sticky='w')

        children_label = tk.Label(register_frame,text='Children', bg="#513d77", font=font,fg='gold')
        children_label.grid(row=2,column=0,sticky='e')
        children_entry = tk.Entry(register_frame,)
        children_entry.grid(row=2,column=1,sticky='w')

        visitors_label = tk.Label(register_frame,text='Visitors', bg="#513d77", font=font,fg='gold')
        visitors_label.grid(row=3,column=0,sticky='e')
        visitors_entry = tk.Entry(register_frame)
        visitors_entry.grid(row=3,column=1,sticky='w')

        notes_text = tk.Label(register_frame, font=font, text='Today\'s notes', bg="#513d77",fg='gold')
        notes_text.grid(row=4, column=1)
        notes_scr_bar = tk.Scrollbar(register_frame)
        notes_scr_bar.grid(row=5, column=2, sticky='ns')
        notes_text_entry = tk.Text(register_frame, font=font, width=60, height=12, yscrollcommand=notes_scr_bar.set)
        notes_text_entry.grid(row=5, column=1)
        notes_scr_bar.config(command=notes_text_entry.yview)

        register_btn = tk.Button(register_frame, text='Update database', width=13, bg='gold', font=font,
                                 command=sunday_register)
        register_btn.grid(row=6, column=1, sticky='w')

        notebook.add(main_service_frame, text='Main Service information\t')

        #---------------------STATISTICS PAGE-----------------------------------------------------------------------
        statistics_page = tk.Frame(notebook, relief='groove', bg="#513d77")
        statistics_page.pack()

        canvas = FigureCanvasTkAgg(f, statistics_page)
        canvas.draw()

        canvas.get_tk_widget().pack(side="top", fill='both', expand=True)

        toolbar = NavigationToolbar2Tk(canvas, statistics_page)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        notebook.add(statistics_page, text='Statistics\t')

        #---------------------Programs PAGE-----------------------------------------------------------------------
        programs_page = tk.Frame(notebook, relief='groove', bg="#513d77")
        programs_page.pack()



        notebook.add(programs_page, text='Church Programs\t')

        #---------------------Events PAGE-----------------------------------------------------------------------
        events_page = tk.Frame(notebook, relief='groove', bg="#513d77")
        events_page.pack()



        notebook.add(events_page, text='Events\t')

         #---------------------Contacts PAGE-----------------------------------------------------------------------
        contacts_page = tk.Frame(notebook, relief='groove', bg="#513d77")
        contacts_page.pack()

        scroll = tk.Scrollbar(contacts_page)
        scroll.pack(side='right', fill='y')

        listbx = tk.Listbox(contacts_page, font=('Verdana', 11,), bg="#513d77", fg='turquoise', yscrollcommand=scroll.set)

        conn = sqlite3.connect("database_folder/database.db")
        cur = conn.cursor()
        data = cur.execute("SELECT * FROM members")
        for i in data.fetchall():
            listbx.insert(0, "")
            listbx.insert(0, i[3])
            listbx.insert(0, i[6])
            listbx.insert(0, i[0] +" "+i[2])


        listbx.pack(fill='both', expand=True)
        scroll.config(command=listbx.yview)

        notebook.add(contacts_page, text='Contacts\t')

class Programs(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.configure(bg="#513d77")

        label = tk.Label(self, text="Programs", bg="#513d77", fg="yellow", font=("Tahoma", 20,))
        label.pack()

        btn = tk.Button(self, text="Home", font=("Verdana", 11), relief="groove",fg='gold', bg="#513d77", width=20,
                        command=lambda: controller.showframe(StartPage))
        btn.pack(anchor='w')

        new_event = tk.Button(self, text="\t+New Event", font=("Verdana", 11),relief='flat',fg='turquoise',
                              bg="#513d77", width=20, command=lambda: controller.showframe(StartPage))
        new_event.pack(anchor='w')

        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side='right',fill='y')

        list_box = tk.Listbox(self, yscrollcommand=scrollbar.set, height=25, bg='#513d77', fg='gold',
                              font=('Verdana', 12,))
        for i in range(40):
            list_box.insert('end', f'Program: {i}')
        list_box.pack(fill='both', expand=True)
        scrollbar.config(command=list_box.yview)

class Administrator(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.configure(bg="darkblue")

        label = tk.Label(self, text="Administrator", bg="darkblue", fg="yellow", font=("Tahoma", 20,))
        label.pack()

        home_button_frame = tk.Frame(self,bg="darkblue")
        home_button_frame.pack(fill='x')

        btn = tk.Button(home_button_frame, text="Logout Administrator",font=("Verdana", 11),relief="groove",bg="gold",
                        width=20, command=lambda: controller.showframe(StartPage))
        btn.pack(side='left',padx=30)

        btn_list = tk.Frame(self, bg='black',relief='groove',bd=1)
        btn_list.pack(fill='x')

        sign_new_user = tk.Button(btn_list, text="Register new user", font=("Verdana", 11), relief="flat",fg='gold',
                                  bg="black", width=20,command=lambda: controller.showframe(Register))
        sign_new_user.pack(side='left')
        church_accounts = tk.Button(btn_list, text="Access church accounts", font=("Verdana", 11), relief="flat",
                                    fg='gold', bg="black", width=20,)
        church_accounts.pack(side='left')

        add_item_to_inv = tk.Button(btn_list, text="Update Inventory", font=("Verdana", 11), relief="flat",fg='gold',
                                    bg="black", width=20,)
        add_item_to_inv.pack(side='left')

        inventory_frame_title = tk.Frame(self, bg='darkblue')
        inventory_frame_title.pack(anchor='nw')

        inventory_title = tk.Label(inventory_frame_title,text="INVENTORY",width=30, bg='darkblue',fg='white',
                                   font=("Verdana", 11))
        inventory_title.pack()

        inventory_frame_inv = tk.Frame(self, bg='darkblue')
        inventory_frame_inv.pack(anchor='nw',padx=30)

        inv_scr_bar = tk.Scrollbar(inventory_frame_inv)
        inv_scr_bar.pack(side='right', fill='y')
        inventory = ttk.Treeview(inventory_frame_inv,yscrollcommand=inv_scr_bar.set)
        inventory.pack(side='left')
        inv_scr_bar.config(command=inventory.yview)

        inventory_btn = tk.Frame(self, bg='darkblue')
        inventory_btn.pack(anchor='w')

        view_inv = tk.Button(inventory_btn, text="View item", font=("Verdana", 11), relief="groove",bg="gold", width=20)
        view_inv.pack(side='left',padx=30)

class Register(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.configure(bg="darkblue")

        font = ('Verdana',14,)

        home_button_frame = tk.Frame(self,bg="darkblue")
        home_button_frame.pack(fill='x')

        label = tk.Label(self, text="Register New User", bg="darkblue", fg="yellow", font=("Tahoma", 20,))
        label.pack()

        btn = tk.Button(home_button_frame, text="Back to Admin", font=("Verdana", 11), relief="groove", bg="gold",
                        width=20, command=lambda: controller.showframe(Administrator))
        btn.pack(side='left')

        def register():
            Database.Database.register_new_user(first_name.get(),last_name.get(),title_entry.get(),password_entry.get())
            first_name.delete(0, 'end')
            last_name.delete(0, 'end')
            title_entry.delete(0, 'end')
            password_entry.delete(0, 'end')

        form_frame = tk.Frame(self, bg='blue', relief='raised', bd=2)
        form_frame.pack(expand=True)

        first_name_label = tk.Label(form_frame, text="First Name: ", font=font, bg='blue', fg="yellow")
        first_name_label.grid(row=0, column=0, sticky='e')

        first_name = tk.Entry(form_frame, width=48, font=font)
        first_name.grid(row=0, column=1)

        last_name_label = tk.Label(form_frame, text="Last Name: ", font=font, bg='blue', fg="yellow")
        last_name_label.grid(row=2, column=0, sticky='e')

        last_name = tk.Entry(form_frame, width=48, font=font)
        last_name.grid(row=2, column=1)
        # ------------------------------------------------------------------------------------------------------------
        title_label = tk.Label(form_frame, text="Title: ", font=font, bg='blue', fg="yellow")
        title_label.grid(row=6, column=0, sticky='e')

        title_entry = tk.Entry(form_frame, width=38, font=font)
        title_entry.grid(row=6, column=1, sticky='w')

        password_label = tk.Label(form_frame, text="Password: ", font=font, bg='blue', fg="yellow")
        password_label.grid(row=7, column=0, sticky='e')

        password_entry = tk.Entry(form_frame, width=38, font=font)
        password_entry.grid(row=7, column=1, sticky='w')

        register_btn = tk.Button(form_frame, text="Register", relief="groove", bg="gold", command=register)
        register_btn.grid(row=8, column=1, sticky='w')


class Youth(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.configure(bg="darkblue")


        home_button_frame = tk.Frame(self,bg="darkblue")
        home_button_frame.pack(fill='x')

        label = tk.Label(self, text="ELCF YOUTH MINISTRY", bg="darkblue", fg="yellow", font=("Tahoma", 20,))
        label.pack()

        def n_member():
            font = ('Verdana', 12,)
            root = tk.Tk()
            root.title('ELCF Youth Ministry Registration')
            root.geometry('600x400')

            def printl():
                Database.CreateNewYouth(name.get(),surname.get(),dob.get(),favorites.get(1.,'end'))
                name.delete(0,'end')
                surname.delete(0, 'end')
                dob.delete(0,'end')
                favorites.delete(1., 'end')


            name_label = tk.Label(root,text='First name: ', font=font)
            name_label.grid(row=0,column=0,sticky='e')
            name = tk.Entry(root, font=font,width=25)
            name.grid(row=0,column=1,sticky='w')

            surname_label = tk.Label(root, text='Last name: ', font=font)
            surname_label.grid(row=1, column=0,sticky='e')
            surname = tk.Entry(root, font=font,width=20)
            surname.grid(row=1,column=1,sticky='w')

            dob_label = tk.Label(root, text='Date of birth: ', font=font)
            dob_label.grid(row=2, column=0,sticky='e')
            dob = tk.Entry(root, font=font)
            dob.grid(row=2,column=1,sticky='w')

            favorites_label = tk.Label(root, text='Favorites: ', font=font)
            favorites_label.grid(row=3, column=0,sticky='e')
            favorites = tk.Text(root, font=font,width=40,height=10)
            favorites.grid(row=4,column=1,sticky='w')

            submitButton = tk.Button(root,text='Create',command=printl,font=font)
            submitButton.grid(row=5,column=1,sticky='w')

            root.mainloop()

        home_btn = tk.Button(home_button_frame, text="Back to Admin", font=("Verdana", 11),
                        relief="flat", bg="darkblue",fg='turquoise',
                        width=20, command=lambda: controller.showframe(StartPage))
        home_btn.pack(side='left')

        new_btn = tk.Button(home_button_frame, text="New member", font=("Verdana", 11),
                        relief="flat", bg="darkblue", fg='turquoise',
                        width=20, command=n_member)
        new_btn.pack(side='left')
# =============================================================================================
        def record_member():
            Database.Register(youth_list.get(), var.get())

        today_record_frame = tk.Frame(self,bg='darkblue')
        today_record_frame.pack(side='top',anchor='n',expand=True,fill='x')

        youth_list = ttk.Combobox(today_record_frame,width=40,font=('Verdana',14))
        if os.path.exists("database_folder/youth register files"):
            youth_list['values'] = [i.split('.')[0] for i in os.listdir('database_folder/youth register files/.')]
        youth_list.pack(side = 'left')

        var = StringVar()
        var.set('Status')

        attend = ttk.OptionMenu(today_record_frame,var, 'Present', 'Absent', 'Present')
        attend.pack(side='left')

        record_button = ttk.Button(today_record_frame,text='Submit',command=record_member)
        record_button.pack(side='left')

# ================================================================================================

if __name__ == "__main__":
    app = Application()
    ani = animation.FuncAnimation(f, animate, interval=1000)
    app.mainloop()
