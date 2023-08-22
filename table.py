import tkinter as tk

class Table:
    custom_font = ("Courier New", 30, "bold")
    border_width = 1
    border_style = "ridge"

    def draw_field(self):
        fields = ["Cycle", "Work", "Break"]
        for i, field in enumerate(fields):
            tk.Label(self.frame, text=field).grid(row=0, column=i, pady=1)

    def create(self, row_size, column_size):
        for y in range(1, column_size+1):

            row = []
            for x in range(row_size):
                cell = tk.Label(self.frame, text="", bg="white", 
                                font=self.custom_font, fg="black", 
                                borderwidth=self.border_width, relief=self.border_style)
                cell.grid(row=y, column=x, padx=0, pady=0, sticky="nsew")
                row.append(cell)

            self.cells.append(row)


    def __init__(self, root, columns):
        self.frame = tk.Frame(root)
        self.draw_field()
        self.cells = []
        self.create(3, columns)
        self.frame.pack(padx=2, pady=2)

    def change_text(self, value, x, y):
        self.cells[y][x].config(text=value)

    def change_color(self, x, y, fg_color='black', bg_color='white'):
        self.cells[y][x].config(fg=fg_color, bg=bg_color)

def main():
    root = tk.Tk()
    root.title("Table")
    table = Table(root, 5)
    table.change_text("Hi!", 0, 0)
    table.change_color(x=0, y=0, fg_color="#75cfff")
    table.change_text("Hi!", 1, 0)
    table.change_text("Hi!", 1, 1)
    table.change_text("Hi!", 2, 2)
    root.mainloop()

if __name__ == "__main__":
    main()
