import customtkinter as ctk
from tkinter import *
from front import buttons
from front import textinputs
from back import user_model
from front import optionboxes
import os
from PIL import Image, ImageTk
from back import draw
from back import get_data
class MyFrame(ctk.CTkFrame):
    def __init__(self,width = 150,height = 600,fg_color ='#00a4ff',border_width = 5,border_color ='#006299',*args, **kwargs):
        super().__init__(width=width,height=height,fg_color=fg_color,border_color = border_color,border_width = border_width,*args, **kwargs)
        
class Left_frame(MyFrame):
    def __init__(self,canvas,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_propagate(False)
        self.canvas = canvas
        
    def add_button(self):
        for id,file in enumerate(os.listdir("gui/temp")):
            print(file)
            button = buttons.ImageButton(master = self,text = file[0:-4],command = lambda file = file : self.canvas.new_bg("gui/temp/"+str(file)))
            button.pack(padx=20,pady=20)
    
class Middle_Canvas(Canvas):
    def __init__(self,width = 850,height = 600,*args, **kwargs):
        super().__init__(bg="white",width=width,height=height,confine=False,*args, **kwargs)
        self.width = width
        self.height = height
    def new_bg(self,filename):
        self.delete("all")
        print(filename)
        img = Image.open(filename)
        print(img.width)
        print(img.height)
        if img.height > self.height or img.width > self.width:
            ratio_width = self.width / img.width
            ratio_height = self.height/img.height
            ratio = min([ratio_width,ratio_height])
            img = img.resize((int(img.width*ratio), int(img.height*ratio)), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(img)
        self.create_image(5,5,anchor=NW,image=self.img) 

    
class Right_frame(MyFrame):
    def __init__(self,canvas,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.canvas = canvas
    def add_buttons(self):
        list = ["followers","following"]
        for item in list:
            button = buttons.diagramButton(master = self,text = item,command = lambda who=item,user_model=os.environ['usermodel'],textmodel =os.environ['textmodel'],id = os.environ['ID'] :self.canvas.new_bg(draw.d_diagram(id,who,user_model,textmodel)))
            button.pack(padx=20,pady=20)
            
class Submit_frame(MyFrame):
    def __init__(self,master2,master3,*args, **kwargs):
        super().__init__(width=800,height=100,*args, **kwargs)
        self.grid_propagate(False)
        self.Left_frame = master2
        self.Right_frame = master3
        self.ID = ctk.StringVar()
        self.button = buttons.SearchButton(master = self,command=self.search)
        self.textinput = textinputs.MyEntry(master = self,textvar=self.ID)
        self.optionText = optionboxes.OptionBoxModels(master = self,string="text model classifier")
        self.optionUser = optionboxes.OptionBoxModels(master = self,string="user model classifier")
        self.textinput.pack(padx=10,pady=10)
        self.optionText.pack(padx=10,pady=10)
        self.optionUser.pack(padx=10,pady=10)
        self.button.pack(padx=10,pady=10)

    def search(self):
        os . environ['usermodel'] = str(self.optionUser.get())
        os.environ['textmodel'] = str(self.optionText.get())
        if str(self.ID.get()).isnumeric():
            os.environ['ID'] = str(self.ID.get())
        else:
            os.environ['ID'] = get_data.id_from_username(str(self.ID.get()))
        frames = [self.Left_frame,self.Right_frame]
        for frame in frames :
            for widget in frame.winfo_children():
                widget.destroy()
        user_model.user_prediction_explain(os.environ['ID'],os.environ['usermodel'],os.environ['textmodel'])
        self.Left_frame.add_button()
        self.Right_frame.add_buttons()