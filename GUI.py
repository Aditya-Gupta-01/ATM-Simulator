import tkinter as tk
from tkinter import messagebox


class GUI():

    def __init__(self,root,db_manager) -> None:
        self.root = root
        self.db_manager = db_manager  

        self.root.title("ATM simulator")      
        self.root.geometry("400x400")

        self.main_menu()

    def main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy() 
        
        self.main_menu_lable = tk.Label(self.root,text="Main Menu")
        self.main_menu_lable.pack(pady=20)

        self.deposite_button = tk.Button(self.root,text="Deposite",command=self.deposite)
        self.deposite_button.pack(pady=10)

        self.withdraw_button = tk.Button(self.root,text="Withdraw",command=self.withdraw)
        self.withdraw_button.pack(pady=10)

        self.check_balance = tk.Button(self.root,text="Check Balance",command=self.balance)
        self.check_balance.pack(pady=10)

        self.set_password_button = tk.Button(self.root,text="Create Password",command=self.create_password)
        self.set_password_button.pack(pady=10)

        self.change_password_button = tk.Button(self.root,text="Change Password",command=self.change_password)
        self.change_password_button.pack(pady=10)


    def withdraw(self):
        for widget in self.root.winfo_children():
            widget.destroy() 
        
        self.card_number_lable = tk.Label(self.root,text="Card Number")
        self.card_number_lable.grid(row=0,column=0,padx=10,pady=10)
        self.card_number_entry = tk.Entry(self.root)
        self.card_number_entry.grid(row=0,column=1,padx=10,pady=10)

        self.password_lable = tk.Label(self.root,text="Password")
        self.password_lable.grid(row=1,column=0,padx=10,pady=10)
        self.password_entry = tk.Entry(self.root)
        self.password_entry.grid(row=1,column=1,padx=10,pady=10)

        self.amount_lable = tk.Label(self.root,text="Amount")
        self.amount_lable.grid(row=2,column=0,padx=10,pady=10)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=2,column=1,padx=10,pady=10)

        self.withdraw_button = tk.Button(self.root,text="Withdraw",command=self.handle_withdraw)
        self.withdraw_button.grid(row=4,column=1,columnspan=2,padx=10,pady=10)
    
    def handle_withdraw(self):
        amount = float(self.amount_entry.get())
        card_number = self.card_number_entry.get()
        password = self.password_entry.get()

        if amount > -1 and card_number and password:
            info_dict = self.db_manager.withdraw(password=password,card_number=card_number,amount=amount)
            self.message(info_dict)
        else:
            messagebox.showerror("Error","Credentials are not provided",parent=self.root)
        

    def deposite(self):
        for widget in self.root.winfo_children():
            widget.destroy() 
        
        self.acount_number_lable = tk.Label(self.root,text="Acount Number")
        self.acount_number_lable.grid(row=0,column=0,padx=10,pady=10)
        self.acount_number_entry = tk.Entry(self.root)
        self.acount_number_entry.grid(row=0,column=1,padx=10,pady=10)

        self.amount_lable = tk.Label(self.root,text="Amount")
        self.amount_lable.grid(row=1,column=0,padx=10,pady=10)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=1,column=1,padx=10,pady=10)

        self.deposite_button = tk.Button(self.root,text="Deposite",command=self.handle_deposite)
        self.deposite_button.grid(row=4,column=1,columnspan=2,padx=10,pady=10)
    
    def handle_deposite(self):
        amount = float(self.amount_entry.get())
        acount_number = self.acount_number_entry.get()

        if amount > 0 and acount_number:
            info_dict = self.db_manager.deposite(acc_number=acount_number,amount=amount)
            self.message(info_dict)
        else:
            messagebox.showerror("Error","Credentials are not provided",parent=self.root)

    def balance(self):
        for widget in self.root.winfo_children():
            widget.destroy() 
        
        self.card_number_lable = tk.Label(self.root,text="Card Number")
        self.card_number_lable.grid(row=0,column=0,padx=10,pady=10)
        self.card_number_entry = tk.Entry(self.root)
        self.card_number_entry.grid(row=0,column=1,padx=10,pady=10)

        self.password_lable = tk.Label(self.root,text="Password")
        self.password_lable.grid(row=1,column=0,padx=10,pady=10)
        self.password_entry = tk.Entry(self.root)
        self.password_entry.grid(row=1,column=1,padx=10,pady=10)

        self.check_balance_button = tk.Button(self.root,text="Check balance",command=self.handle_check_balance)
        self.check_balance_button.grid(row=3,column=1,columnspan=2,padx=10,pady=10)
    
    def handle_check_balance(self):
        card_number = self.card_number_entry.get()
        password = self.password_entry.get()
        info_dict = self.db_manager.check_balance(card_number = card_number,password=password)
        self.message(info_dict)

    def create_password(self):
        for widget in self.root.winfo_children():
            widget.destroy() 
        
        self.acount_number_lable = tk.Label(self.root,text="Acount Number")
        self.acount_number_lable.grid(row=0,column=0,padx=10,pady=10)
        self.acount_number_entry = tk.Entry(self.root)
        self.acount_number_entry.grid(row=0,column=1,padx=10,pady=10)

        self.password_lable = tk.Label(self.root,text="Password")
        self.password_lable.grid(row=1,column=0,padx=10,pady=10)
        self.password_entry = tk.Entry(self.root)
        self.password_entry.grid(row=1,column=1,padx=10,pady=10)

        self.create_password_button = tk.Button(self.root,text="Create",command=self.handle_create_password)
        self.create_password_button.grid(row=3,column=1,columnspan=2,padx=10,pady=10)
    
    def handle_create_password(self):
        password = self.password_entry.get()
        account_number = self.acount_number_entry.get()

        info_dict = self.db_manager.set_password(password=password,acc_number = account_number)
        self.message(info_dict)

    def change_password(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.card_number_lable = tk.Label(self.root,text="Card Number")
        self.card_number_lable.grid(row=0,column=0,padx=10,pady=10)
        self.card_number_entry = tk.Entry(self.root)
        self.card_number_entry.grid(row=0,column=1,padx=10,pady=10)

        self.password_lable = tk.Label(self.root,text="Password")
        self.password_lable.grid(row=1,column=0,padx=10,pady=10)
        self.password_entry = tk.Entry(self.root)
        self.password_entry.grid(row=1,column=1,padx=10,pady=10)

        self.New_password_lable = tk.Label(self.root,text="New_Password")
        self.New_password_lable.grid(row=2,column=0,padx=10,pady=10)
        self.New_password_entry = tk.Entry(self.root)
        self.New_password_entry.grid(row=2,column=1,padx=10,pady=10)

        self.create_password_button = tk.Button(self.root,text="Change",command=self.handle_change_password)
        self.create_password_button.grid(row=4,column=1,columnspan=2,padx=10,pady=10)

    def handle_change_password(self):
        new_password = self.New_password_entry.get()        
        password = self.password_entry.get()
        card_number = self.card_number_entry.get()
        info_dict = self.db_manager.change_password(new_password=new_password,card_number=card_number,password=password)
        self.message(info_dict)


    def message(self,info_dict):
        for key,value in info_dict.items():
            if(key == "Error"):
                messagebox.showerror("Error",value,parent=self.root)
            elif(key == 'Success'):
                messagebox.showinfo("Success",value,parent=self.root)
            else:
                messagebox.showwarning("Info",value,parent=self.root)