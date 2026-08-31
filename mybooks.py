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
import sqlite3

def main():

    class Bookdb:
        def __init__(self):
            self.con = sqlite3.connect("mybooks.db")
            self.cursor = self.con.cursor()
            self.cursor.execute("CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY, title TEXT, author TEXT, isbn INTEGER)")
            self.con.commit()
            print("You have connected to the  database")
            print(self.con)

        def __del__(self):
            self.con.close()

        def view(self):
            self.cursor.execute("SELECT * FROM books")
            rows = self.cursor.fetchall()
            return rows

        def insert(self,title, author, isbn):
            sql=("INSERT INTO books(title,author,isbn)VALUES (?,?,?)")
            values =[title,author,isbn]
            self.cursor.execute(sql,values)
            self.con.commit()
            messagebox.showinfo(title="Book Database",message="New book added to database")

        def update(self, id, title, author, isbn):
            tsql = 'UPDATE books SET  title = ?, author = ?, isbn = ? WHERE id=?'
            self.cursor.execute(tsql, [title,author,isbn,id])
            self.con.commit()
            messagebox.showinfo(title="Book Database",message="Book Updated")

        def delete(self, id):
            delquery ='DELETE FROM books WHERE id = ?'
            self.cursor.execute(delquery, [id])
            self.con.commit()
            messagebox.showinfo(title="Book Database",message="Book Deleted")

    db = Bookdb()

    def get_selected_tuple():
        selection = list_bx.curselection() # returns tuple of indexes of selected items

        if not selection:
            return None

        index = selection[0] 
        return list_bx.get(index)
  
    def no_selection_warning():
        messagebox.showwarning(
            "No Selection",
            "Please select a book first."
        )
        
    def get_selected_row(event):
        selected_tuple = get_selected_tuple()

        if selected_tuple is None:
            return
        
        title_entry.delete(0, 'end') # clears whatever is in the entry boxes
        title_entry.insert('end', selected_tuple[1]) # puts whatever the selected title was into the entry box 

        author_entry.delete(0, 'end')
        author_entry.insert('end', selected_tuple[2])

        isbn_entry.delete(0, 'end')
        isbn_entry.insert('end', selected_tuple[3])

    def view_records():
        list_bx.delete(0, 'end') # clears list box
        for row in db.view(): # fetches all the records from the db
            list_bx.insert('end', row) # and displays them

    def add_book():
        db.insert(title_text.get(),author_text.get(),isbn_text.get())
        list_bx.delete(0, 'end')
        list_bx.insert('end', (title_text.get(), author_text.get(), isbn_text.get())) # type: ignore
        title_entry.delete(0, "end") # Clears input after inserting
        author_entry.delete(0, "end")
        isbn_entry.delete(0, "end")
        

    def delete_records():
        selected_tuple = get_selected_tuple()

        if selected_tuple is None:
            no_selection_warning()
            return
        
        db.delete(selected_tuple[0])
        

    def clear_screen():
        list_bx.delete(0,'end')
        title_entry.delete(0,'end')
        author_entry.delete(0,'end')
        isbn_entry.delete(0,'end')

    def update_records():
        selected_tuple = get_selected_tuple()

        if selected_tuple is None:
            no_selection_warning()
            return
        
        db.update(selected_tuple[0], title_text.get(), author_text.get(), isbn_text.get())
        title_entry.delete(0, "end") # Clears input after inserting
        author_entry.delete(0, "end")
        isbn_entry.delete(0, "end")
       

    def on_closing():
        dd = db
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()
            del dd


    root = Tk() # creates application window

    root.title("My Books Database Application")
    root.configure(background="light green")
    root.geometry("1920x1200") # app window size
    root.resizable(width=False, height=False) # prevent resizing

    title_label = ttk.Label(root, text="Title", background="light green", font=("TkDefaultFont", 16))
    title_label.grid(row=0, column=0, sticky=W)
    title_text = StringVar()
    title_entry = ttk.Entry(root, width=24, textvariable=title_text)
    title_entry.grid(row=0, column=1, sticky=W)

    # widgets for inserting new db entries
    author_label = ttk.Label(root, text="Author", background="light green", font=("TkDefaultFont", 16))
    author_label.grid(row=0, column=2, sticky=W)
    author_text = StringVar()
    author_entry = ttk.Entry(root, width=24, textvariable=author_text)
    author_entry.grid(row=0, column=3, sticky=W)

    isbn_label = ttk.Label(root, text="ISBN", background="light green", font=("TkDefaultFont", 16))
    isbn_label.grid(row=0, column=4, sticky=W)
    isbn_text = StringVar()
    isbn_entry = ttk.Entry(root, width=24, textvariable=isbn_text)
    isbn_entry.grid(row=0, column=5, sticky=W)

    add_btn = Button(root, text="Add Book", bg="blue", fg="white", font="helvetica 10 bold", command=add_book)
    add_btn.grid(row=0, column=6, sticky=W)

    # displays our db data
    list_bx = Listbox(root, height=16, width=40, font="helvetica 13", bg="light blue")
    list_bx.grid(row=3, column=1, columnspan=14, sticky=W + E, pady=40, padx=15)
    list_bx.bind('<<ListboxSelect>>', get_selected_row) # binds selected list box item

    scroll_bar = Scrollbar(root)
    scroll_bar.grid(row=1, column=8, rowspan=14, sticky=W)

    list_bx.configure(yscrollcommand=scroll_bar.set) # enables vertical scrolling
    scroll_bar.configure(command=list_bx.yview)



    # more widgets to interface with the db
    view_btn = Button(root, text="View all records", bg="black", fg="white", font="helvetica 10 bold", command=view_records)
    view_btn.grid(row=15, column=1)

    clear_btn = Button(root, text="Clear Screen", bg="maroon", fg="white", font="helvetica 10 bold", command=clear_screen)
    clear_btn.grid(row=15, column=2)

    exit_btn = Button(root, text="Exit Application", bg="blue", fg="white", font="helvetica 10 bold", command=root.destroy)
    exit_btn.grid(row=15, column=3)

    modify_btn = Button(root, text="Modify Record", bg="purple", fg="white", font="helvetica 10 bold", command=update_records)
    modify_btn.grid(row=15, column=4)

    delete_btn = Button(root, text="Delete Record", bg="red", fg="white", font="helvetica 10 bold", command=delete_records)
    delete_btn.grid(row=15, column=5)






    root.mainloop()




if __name__ == "__main__":
    main()
