# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 02:07:04 2016

@author: chmartin
"""

import tkinter as tk 

fenetre = tk.Tk()
fenetre['bg']='white'



label_frame = tk.LabelFrame(fenetre, text="titre", padx=20, pady=20)
label_frame.pack(fill="both", expand="yes")
 
tk.Label(label_frame, text="A l'intérieure de la frame").pack()


fenetre.mainloop()


