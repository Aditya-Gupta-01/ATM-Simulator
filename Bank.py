import psycopg2
from psycopg2 import sql, extras
from bcrypt import checkpw, hashpw, gensalt
from tkinter import messagebox


class Bank:
    def withdraw(self, card_number, password, amount) -> float:
        if self.authenticate(password=password, card_number=card_number):
            balance = self.get_balance(card_number=card_number)

            if balance >= amount:
                self.set_balance_withdraw(card_number=card_number,balance=amount)
                return {"Success": f"amount withdraw - {amount}"}
            else:
                return {"Info": "Low Balance"}
        else:
            return {"Error": "authentication failed"}

    def deposite(self, acc_number, amount) -> float:
        try:
            query = """select count(*) from users where account_number = %s"""
            self.cursor.execute(query, (acc_number,))

            if self.cursor.fetchone():
                self.set_balance_deposite(acc_number, amount)
                return {"Success": "Amount deposited"}
            else:
                return {"Error": "account dose not exists"}
        except Exception as e:
            return {"Error": "Error in deposit" + str(e)}

    def check_balance(self, card_number,password):
        if self.authenticate(password=password,card_number=card_number):
            return {"Info": self.get_balance(card_number=card_number)}
        else:
            return {"Error": "Authentication failed"}

    def get_balance(self, card_number=None, acc_number=None) -> float:
        try:
            if card_number:
                query = """select curr_balance from users
                            where card_number = %s"""
                self.cursor.execute(query, (card_number,))
            elif acc_number:
                query = """select curr_balance from users
                            where account_number = %s"""
                self.cursor.execute(query, (acc_number,))
            else:
                return {"Error": "No account or card number provided"}

            return float(self.cursor.fetchone()[0])

        except Exception as e:
            return {"Error": f"Error in fetching balance: {e}"}

    def set_balance_deposite(self, acc_number, balance):
        try:
            query = """update users
                        set curr_balance = curr_balance+%s
                        where account_number = %s"""
            self.cursor.execute(query, (balance, acc_number))
            self.add_transaction_details(amount = balance,acc_number = acc_number)
        except Exception as e:
            return {"Error": f"Error in updating deposited balance: {e}"}

    def set_balance_withdraw(self, card_number, balance):
        try:
            query = """update users
                        set curr_balance = curr_balance-%s
                        where card_number = %s"""
            self.cursor.execute(query, (balance, card_number))
            self.add_transaction_details(amount=balance,card_number=card_number)
        except Exception as e:
            return {"Error": f"Error in updating withdrawl balance: {e}"}

    def add_transaction_details(self,amount,acc_number=None,card_number=None):
        try:
            if not acc_number:
                query = '''select account_number from users where 
                            card_number = %s'''
                self.cursor.execute(query,(card_number,))
                acc_number = self.cursor.fetchone()[0]
                
            print(acc_number)
            curr_balance = self.get_balance(acc_number = acc_number)
            
            query = '''insert into transactions(account_number,type_of_transaction,amount_of_transaction,curr_amount)
                        values(%s,'ATM',%s,%s)'''
            self.cursor.execute(query,(acc_number,amount,curr_balance))
        except Exception as e:
            print("Error in updating transaction "+str(e))

    def get_password(self, card_number) -> str:
        try:
            query = """SELECT password FROM passwords WHERE card_number = %s"""
            self.cursor.execute(query, (card_number,))
            result = self.cursor.fetchone()
            return result[0]
        except Exception as e:
            print(str(e))

    def set_password(self, acc_number, password):
        try:
            # Retrieve the card number for the given account number
            query = """select card_number from passwords where account_number = %s"""
            self.cursor.execute(query, (acc_number,))

            try:
                if self.cursor.fetchone()[0]:
                    return {"Info": "Use change password option"}
            except:
                pass

            query = """SELECT card_number FROM users WHERE account_number = %s"""
            self.cursor.execute(query, (acc_number,))
            result = self.cursor.fetchone()

            if result:
                card_number = result[0]

                password = password.encode("utf-8")
                hashed_password = hashpw(password, gensalt())
                hashed_password = hashed_password.decode("utf-8")

                query = """INSERT INTO passwords(password, account_number, card_number) VALUES(%s, %s, %s)"""
                self.cursor.execute(query, (hashed_password, acc_number, card_number))

                return {"Success": "Password is created"}
            else:
                return {"Error": "Account number not found"}

        except Exception as e:
            return {"Error": f"Error in setting password: {e}"}

    def change_password(self, card_number, password, new_password):
        try:
            if self.authenticate(password, card_number):
                query = """update passwords
                            set password = %s
                            where card_number = %s"""
                
                new_password = new_password.encode("utf-8")
                hashed_password = hashpw(new_password, gensalt())
                hashed_password = hashed_password.decode("utf-8")

                self.cursor.execute(query, (hashed_password,card_number))
                return {"Success": "Password is updated"}
            
        except Exception as e:
            return {"Error": f"Error in updating password: {e}"}

    def authenticate(self, password, card_number):
        try:
            # Retrieve the hashed password for the given card number
            result = self.get_password(card_number)
            if result:
                hashed_password = result.encode("utf-8")
                password = password.encode("utf-8")

                # Check if the provided password matches the stored hashed password
                if checkpw(password, hashed_password):
                    return True

            return False

        except Exception as e:
            return False


class db_connection(Bank):

    def __init__(self, user, database, password, host, port):
        """establish db connection"""
        try:
            self.con = psycopg2.connect(
                user=user, dbname=database, password=password, host=host, port=port
            )

            self.cursor = self.con.cursor()
            self.con.autocommit = True

        except Exception as e:
            print(f"Error in DB connection " + str(e))

    def close(self):
        self.cursor.close()
        self.con.close()
