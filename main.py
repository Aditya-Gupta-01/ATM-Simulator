import os
import tkinter as tk
from dotenv import load_dotenv
from GUI import GUI

from Bank import db_connection


if __name__ == "__main__":

    load_dotenv()

    root = tk.Tk()
    connection = db_connection(
        user=os.getenv("USER"),
        database=os.getenv("DATABASE"),
        password=os.getenv("PASSWORD"),
        host=os.getenv("HOST"),
        port=os.getenv("PORT"),
    )
    
    gui = GUI(root,connection)

    root.mainloop()
    connection.close()