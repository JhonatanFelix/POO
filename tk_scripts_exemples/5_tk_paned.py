# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 02:07:04 2016

@author: chmartin
"""

import tkinter as tk 

fenetre = tk.Tk()
fenetre['bg']='white'



p = tk.PanedWindow(fenetre, orient=tk.HORIZONTAL)
p.pack(side=tk.TOP, expand=tk.Y, fill=tk.BOTH, pady=2, padx=2)
p.add(tk.Label(p, text='Volet 1', background='blue', anchor=tk.CENTER))
p.add(tk.Label(p, text='Volet 2', background='white', anchor=tk.CENTER) )
p.add(tk.Label(p, text='Volet 3', background='red', anchor=tk.CENTER) )
p.pack()


fenetre.mainloop()


