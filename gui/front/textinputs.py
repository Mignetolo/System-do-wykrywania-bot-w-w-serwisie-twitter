import customtkinter as ctk
import tkinter as tk

class MyEntry(ctk.CTkEntry):
      def __init__(self,textvar,*args, **kwargs):
            super().__init__(*args, **kwargs)
            self.configure(height = 30)
            self.configure(textvariable = textvar)