from tkinter import (
    Tk, 
    Button, 
    Label, 
    Scrollbar, 
    Listbox,
    StringVar,
    Entry,
    W,
    E,
    N,
    S,
    END
)
from tkinter import ttk
from tkinter import messagebox


def main():
    root = Tk()

    root.title("My Books Database Application")
    root.configure(background="light green")
    root.geometry("1700x1000")
    root.resizable(width=False, height=False)


    root.mainloop()




if __name__ == "__main__":
    main()
