import sqlite3
try:
    import tkinter
except ImportError:     # python2
    import Tkinter as tkinter


class ScrollBox(tkinter.Listbox):

    def __init__(self, window, **kwargs):
        super().__init__(window, **kwargs)

        self.scrollbar = tkinter.Scrollbar(window, orient=tkinter.VERTICAL, command=self.yview)

    def grid(self, row, column, sticky='nsew', rowspan=1, columnspan=1, **kwargs):
        super().grid(row=row, column=column, sticky=sticky, rowspan=rowspan, columnspan=columnspan, **kwargs)
        self.scrollbar.grid(row=row, column=column, sticky='nse', rowspan=rowspan)
        self['yscrollcommand'] = self.scrollbar.set


class DataListbox(ScrollBox):

    def __init__(self, window, connection, table, field, sort_order=(), **kwargs):
        super().__init__(window, **kwargs)

        self.cursor = connection.cursor()
        self.table = table
        self.field = field

        self.link_field = None
        self.linked_box = None

        self.bind('<<ListboxSelect>>', self.on_select)

        self.sql_select = " SELECT " + self.field + ",_id" + " FROM " + self.table
        if sort_order:
            self.sql_order = " ORDER BY " + ",".join(sort_order)
        else:
            self.sql_order = " ORDER BY " + self.field

    def clear(self):
        self.delete(0, tkinter.END)

    def link(self, widget, link_field):
        self.linked_box = widget
        widget.link_field = link_field

    def requery(self, link_value=None):
        if link_value and self.link_field:
            sql = self.sql_select + " WHERE " + self.link_field + "=?" + self.sql_order
            print(sql)
            self.cursor.execute(sql, (link_value,))
        else:
            print(self.sql_select + self.sql_order)
            self.cursor.execute(self.sql_select + self.sql_order)

        self.clear()
        for value in self.cursor:
            self.insert(tkinter.END, value[0])

        if self.linked_box:
            self.linked_box.clear()

    def on_select(self, event):
        if self.linked_box:
            print(self is event.widget)
            index = self.curselection()[0]
            value = self.get(index),

            link_id = self.cursor.execute(self.sql_select + " WHERE " + self.field + "=?" + self.sql_order, value).fetchone()[1]
            self.linked_box.requery(link_id)


if __name__ == "__main__":
    conn = sqlite3.connect('music.db')

    mainwindow = tkinter.Tk()
    mainwindow.geometry("1024x720")
    mainwindow.title("JukeBox")

    mainwindow.rowconfigure(0, weight=1)
    mainwindow.rowconfigure(1, weight=5)
    mainwindow.rowconfigure(2, weight=5)
    mainwindow.rowconfigure(3, weight=1)

    mainwindow.columnconfigure(0, weight=2)
    mainwindow.columnconfigure(1, weight=2)
    mainwindow.columnconfigure(2, weight=2)
    mainwindow.columnconfigure(3, weight=1)

    # ======= listbox label ========
    tkinter.Label(mainwindow, text="Artists").grid(row=0, column=0)
    tkinter.Label(mainwindow, text="Albums").grid(row=0, column=1)
    tkinter.Label(mainwindow, text="Songs").grid(row=0, column=2)

    # ========= Artistlistbox =======
    artistlist = DataListbox(mainwindow, conn, "artists", "name")
    artistlist.grid(row=1, column=0, sticky='nsew', rowspan=2, padx=(30, 0))
    artistlist.config(relief='sunken', border=2)
    artistlist.requery()

    # ========= Albumlistbox =======
    albumLv = tkinter.Variable(mainwindow)
    albumLv.set(("choose an album:",))
    albumlist = DataListbox(mainwindow, conn, "albums", "name", sort_order=("name",))
    albumlist.grid(row=1, column=1, sticky='nsew', padx=(30, 0))
    albumlist.config(relief='sunken', border=2)
    artistlist.link(albumlist, "artist")

    # ========= songlistbox =======
    songLv = tkinter.Variable(mainwindow)
    songLv.set(("choose a song:",))
    songlist = DataListbox(mainwindow, conn, "songs", "title", ("title", "track"))
    songlist.grid(row=1, column=2, sticky='nsew', padx=(30, 0))
    songlist.config(relief='sunken', border=2)
    albumlist.link(songlist, "album")

    mainwindow.mainloop()
    conn.close()