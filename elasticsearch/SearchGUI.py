from tkinter import *
from searcher import *

default_values = ('Honda', 'All')
fields = 'Query', 'City'

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

	row = Frame(root)
	lab = Label(row, width=15, text="Motor cycle type", anchor='w')
	variable1 = StringVar(root)
	row.pack(side=TOP, fill=X, padx=5, pady=5)
	lab.pack(side=TOP)
	variable1.set("All")
	w = OptionMenu(root, variable1, "Cross/enduro", "Custom", "Fyrhjuling/ATV", "Offroad", "Scooter", "Sport", "Touring", "Övrigt", "All")
	w.pack(side = TOP)
	entries.append(("Motor cycle type", variable1))

	row = Frame(root)
	lab = Label(row, width=15, text="Min model year", anchor='w')
	variable2 = StringVar(root)
	row.pack(side=TOP, fill=X, padx=5, pady=5)
	lab.pack(side=TOP)
	variable2.set("1981")
	w = OptionMenu(root, variable2, "1981", "1982", "1983", "1984", "1985", "1986", "1987", "1988", "1989","1990","1991","1992","1993","1994","1995","1996","1997","1998","1999","2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018")
	w.pack(side = TOP)
	entries.append(("Min model year", variable2))

	row = Frame(root)
	lab = Label(row, width=15, text="Min model year", anchor='w')
	variable3 = StringVar(root)
	row.pack(side=TOP, fill=X, padx=5, pady=5)
	lab.pack(side=TOP)
	variable3.set("2018")
	w = OptionMenu(root, variable3, "1981", "1982", "1983", "1984", "1985", "1986", "1987", "1988", "1989","1990","1991","1992","1993","1994","1995","1996","1997","1998","1999","2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018")
	w.pack(side = TOP)
	entries.append(("Max model year", variable3))

	return entries

def search(entries):
	"""
		Use searcher.py to create and display results
	"""
	if entries[2][1].get() == "All":
		res = searcher.price(query=entries[0][1].get(), location=entries[1][1].get(),  min_model_year=entries[3][1].get(), max_model_year=entries[4][1].get())
		returned_docs = searcher.similar(query=entries[0][1].get(), location=entries[1][1].get(),  min_model_year=entries[3][1].get(), max_model_year=entries[4][1].get())
		if entries[1][1].get() == "All":
			res = searcher.price(query=entries[0][1].get(),  min_model_year=entries[3][1].get(), max_model_year=entries[4][1].get())
			returned_docs = searcher.similar(query=entries[0][1].get(),  min_model_year=entries[3][1].get(), max_model_year=entries[4][1].get())
	elif entries[1][1].get() == "All":
		res = searcher.price(query=entries[0][1].get(), location=entries[2][1].get(),  min_model_year=entries[3][1].get(), max_model_year=entries[4][1].get())
		returned_docs = searcher.similar(query=entries[0][1].get(), location=entries[2][1].get(),  min_model_year=entries[3][1].get(), max_model_year=entries[4][1].get())
	else:
		res = searcher.price(query=entries[0][1].get(), location=entries[1][1].get(), vehicle_type=entries[2][1].get(),  min_model_year=entries[3][1].get(), max_model_year=entries[4][1].get())
		returned_docs = searcher.similar(query=entries[0][1].get(), location=entries[1][1].get(), vehicle_type=entries[2][1].get(),  min_model_year=entries[3][1].get(), max_model_year=entries[4][1].get())

	res_frame = Tk()
	res_frame.title('Result')

	if res == None:
		w = Label(res_frame, text='No match for this query')
		w.pack(padx=20, pady=20)
	else:
		for entry in entries:
			field = entry[0]
			text = entry[1].get()
			Label(res_frame, text='%s: "%s"' % (field, text)).pack(side=TOP)
		Label(res_frame, text='Number of hits: %s' % len(returned_docs)).pack(side=TOP,padx=20,pady=20)
		w = Label(res_frame, text="""
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
		w.pack(side=LEFT, padx=20, pady=20)

	b = Button(res_frame, text='Quit', command=res_frame.quit)
	b.pack(side=BOTTOM, padx=5, pady=5)

	res_frame.mainloop()

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



