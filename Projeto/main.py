import tkinter as tk
import customtkinter as ctk
from tkinter import *
from login import tela_login

if __name__ == "__main__":
    window = ctk.CTk()
    tela_login(window)
    window.mainloop()
