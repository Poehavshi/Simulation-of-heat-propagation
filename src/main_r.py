import tkinter as tk
from controllers.controller import Controller

if __name__ == "__main__":
    root = tk.Tk()
    app = Controller(root, param_name='r')
    root.mainloop()


