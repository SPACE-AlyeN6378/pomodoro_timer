import pygame
import tkinter as tk
from pomodoro import Pomodoro


if __name__ == "__main__":
    root = tk.Tk()
    app = Pomodoro(root, 5)
    root.after(100, app.start_pomodoro)
    
    root.mainloop()
