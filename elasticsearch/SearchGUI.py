from tkinter import *
from searcher import *

default_values = ('honda', 'vänersborg', 'sport', '2009', '2018')
fields = ['Query', 'City', 'Vehicle type', 'Min model year', 'Max model year']

types = [
            "Cross/enduro", 
            "Custom", 
            "Fyrhjuling/ATV", 
            "Offroad", 
            "Scooter", 
            "Sport", 
            "Touring",
            "Övrigt",
        ]

def makeform(root, fields):
    """
    Create search window
    """

    entries = []
    for i, field in enumerate(fields):
        row = Frame(root)
        lab = Label(row, width=15, text=field, anchor='w')
        ent = Entry(row)
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        ent.insert(10,default_values[i])
        entries.append((field, ent))

    return entries

def search(entries):
    """
    	Use searcher.py to create and display results
    """
    res = searcher.price(query=entries[0][1].get(), location=entries[1][1].get(), vehicle_type=entries[2][1].get(),  min_model_year=entries[3][1].get(), max_model_year=entries[4][1].get())
    root = Tk()
    root.title('Result')
    w = Label(root, text="""
    Average price: {}
    Median price: {}
    Max price: {}
    Min price: {}
    """.format(\
        res["average_price"],
        res["median_price"],
        res["max_price"],
        res["min_price"],
        ))
    w.pack()
    root.mainloop()
    return res


if __name__ == '__main__':
    root = Tk()
    root.title('Searcher')
    searcher = Searcher()

    ents = makeform(root, fields)
    root.bind('<Return>', (lambda event, e=ents: search(e)))   

    # Quit button
    b1 = Button(root, text='Quit', command=root.quit)
    b1.pack(side=LEFT, padx=5, pady=5)
    # Search button
    b2 = Button(root, text='Search', command=(lambda e=ents: search(e)))
    b2.pack(side=RIGHT, padx=5, pady=5)

    root.mainloop()



