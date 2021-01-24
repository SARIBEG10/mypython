import sqlite3
try:
    import tkinter
except ImportError:  # python2
    import Tkinter as tkinter


class ScrollBox(tkinter.Listbox):

    def __init__(self, window, **kwargs):
        super().__init__(window, **kwargs)
        self.scrollbar = tkinter.Scrollbar(window, orient=tkinter.VERTICAL, command=self.yview)

    def grid(self, row, column, sticky='nsw', rowspan=1, columnspan=1, **kwargs):
        super().grid(row=row, column=column, sticky=sticky, rowspan=rowspan, columnspan=columnspan, **kwargs)
        self.scrollbar.grid(row=row, column=column, sticky='nse', rowspan=rowspan)
        self['yscrollcommand'] = self.scrollbar.set


class DataListbox(ScrollBox):

    def __init__(self, window, connection, table, field, sort_order=(), **kwargs):
        super().__init__(window, **kwargs)

        self.cursor = connection.cursor()
        self.table = table
        self.field = field

        self.linked_box = None
        self.link_field = None

        self.bind('<<ListboxSelect>>', self.on_select)

        self.sql_select = " SELECT " + self.field + ",_id" + " FROM " + self.table
        if sort_order:
            self.sql_sort = " ORDER BY " + ','.join(sort_order)
        else:
            self.sql_sort = " ORDER BY " + self.field

    def clear(self):
        self.delete(0, tkinter.END)

    def link(self, widget, link_field):
        self.linked_box = widget
        widget.link_field = link_field

    def requery(self, link_value=None):
        if link_value and self.link_field:
            sql = self.sql_select + " WHERE " + self.link_field + "=?" + self.sql_sort
            self.cursor.execute(sql, (link_value,))
        else:
            print(self.sql_select + self.sql_sort)
            self.cursor.execute(self.sql_select + self.sql_sort)

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

            link_value = self.cursor.execute(self.sql_select + " WHERE " + self.field + "=?" + self.sql_sort, value).fetchone()[1]
            self.linked_box.requery(link_value)


if __name__ == "__main__":

    conn = sqlite3.connect("music.db")

    mainwindow = tkinter.Tk()
    mainwindow.title('Music DB Browser')
    mainwindow.geometry("1024x720")

    mainwindow.columnconfigure(0, weight=2)
    mainwindow.columnconfigure(1, weight=2)
    mainwindow.columnconfigure(2, weight=2)
    mainwindow.columnconfigure(3, weight=1)     # spacer column on right

    mainwindow.rowconfigure(0, weight=1)
    mainwindow.rowconfigure(1, weight=5)
    mainwindow.rowconfigure(2, weight=5)
    mainwindow.rowconfigure(3, weight=1)

    # ======= Labels =======
    tkinter.Label(mainwindow, text='Artists').grid(row=0, column=0)
    tkinter.Label(mainwindow, text='Albums').grid(row=0, column=1)
    tkinter.Label(mainwindow, text='Songs').grid(row=0, column=2)

    # ======= Artists List ========
    artistList = DataListbox(mainwindow, conn, "artists", "name")
    artistList.grid(row=1, column=0, sticky='nsew', rowspan=2, padx=(30, 0))
    artistList.config(border=2, relief='sunken')
    artistList.requery()
    # ======= Albums List ========
    albumLv = tkinter.Variable(mainwindow)
    albumLv.set(("Choose an Artist ",))
    albumlist = DataListbox(mainwindow, conn, "albums", "name", sort_order=("name",))
    albumlist.grid(row=1, column=1, sticky='nsew', padx=(30, 0))
    albumlist.config(border=2, relief='sunken')
    artistList.link(albumlist, "artist")
    # ======= Songs List ========
    songLv = tkinter.Variable(mainwindow)
    songLv.set(("Choose an Album ",))
    songlist = DataListbox(mainwindow, conn, "songs", "title", ("track", "title"))
    songlist.grid(row=1, column=2, sticky='nsew', padx=(30, 0))
    songlist.config(border=2, relief='sunken')
    albumlist.link(songlist, "album")
    # ======= Closing db And Mainloop ========
    mainwindow.mainloop()
    conn.close()