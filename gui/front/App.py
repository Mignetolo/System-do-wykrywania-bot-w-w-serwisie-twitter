import customtkinter as ctk
import tkinter as tk
from front import frames

class App(ctk.CTk, tk.Tk):
    def __init__(self,width,height):
        super().__init__()
        self.MiddleFrame = frames.Middle_Canvas(master=self,)
        self.LeftFrame = frames.Left_frame(master=self,canvas = self.MiddleFrame)
        self.RightFrame = frames.Right_frame(master=self,canvas = self.MiddleFrame)
        self.SubmitFrame = frames.Submit_frame(master=self,master2 =self.LeftFrame,master3=self.RightFrame)
        self.RightFrame.grid(column=2,row=1,pady=10,padx=10)
        self.LeftFrame.grid(column=0,row=1,pady=10,padx=10)
        self.MiddleFrame.grid(column=1,row=1,pady=10,padx=10)
        self.SubmitFrame.grid(column = 1,row =0,pady=10,padx=10)