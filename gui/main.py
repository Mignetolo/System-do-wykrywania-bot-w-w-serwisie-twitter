import customtkinter as ctk
from front import App

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    #  create a window first
    # define window dimensions width and height
    WINDOW_WIDTH = 1220
    WINDOW_HEIGHT = 850
    #Flipper_Back.EnterSudo("Onomatopeja")
    app = App.App(WINDOW_WIDTH,WINDOW_HEIGHT)
    # *get the screen size of your computer
    # *[width and height using the root object as foolows]
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    # Get the window position from the top dynamically
    # as well as position from left or right as follows
    position_top = int(screen_height / 2 - WINDOW_HEIGHT / 2)
    position_right = int(screen_width / 2 - WINDOW_WIDTH / 2)
    # this is the line that will center your window
    app.geometry(
                f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{position_right}+{position_top}')
    # lock window to not be resizable
    # initialise the window
    app.title('Account Audit')
    # change name of the app
    app.mainloop()
