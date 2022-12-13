import customtkinter as ctk

class MyOptionBox(ctk.CTkOptionMenu):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

class OptionBoxModels(MyOptionBox):
     def __init__(self,string,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(values=["MultinomialNB", "Randomforest"])
        self.set(string)