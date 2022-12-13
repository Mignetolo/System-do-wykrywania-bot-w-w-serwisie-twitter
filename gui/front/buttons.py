import customtkinter as ctk
import tkinter as tk

class MyButton(ctk.CTkButton):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(width = 120)
        self.configure(height = 32)
        self.configure(corner_radius = 8)
        
class SearchButton(MyButton):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(text = " search")
        
class ImageButton(MyButton):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

class diagramButton(MyButton):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)