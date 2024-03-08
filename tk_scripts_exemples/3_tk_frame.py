# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 02:07:04 2016

@author: chmartin
"""

import tkinter as tk 

fenetre = tk.Tk()
fenetre['bg']='white'

Frame1 = tk.Frame(fenetre, borderwidth=2, relief=tk.GROOVE)
Frame1.pack(side=tk.LEFT, padx=30, pady=30)
# Ajout de labels
tk.Label(Frame1, text="Frame 1").pack(padx=10, pady=10)

# frame 2
Frame2 = tk.Frame(fenetre, borderwidth=2, relief=tk.GROOVE)
Frame2.pack(side=tk.LEFT, padx=10, pady=10)

# frame 3 dans frame 2
Frame3 = tk.Frame(Frame2, bg="white", borderwidth=2, relief=tk.GROOVE)
Frame3.pack(side=tk.RIGHT, padx=5, pady=5)

Frame1 = tk.Frame(fenetre, borderwidth=2, relief=tk.GROOVE)
Frame1.pack(side=tk.LEFT, padx=30, pady=30)

# Ajout de labels
tk.Label(Frame1, text="Frame 1").pack(padx=10, pady=10)
tk.Label(Frame2, text="Frame 2").pack(padx=10, pady=10)
tk.Label(Frame3, text="Frame 3",bg="white").pack(padx=10, pady=10)

# frame 1
Frame4 = tk.Frame(fenetre, borderwidth=2, relief=tk.GROOVE)
Frame4.pack(side=tk.LEFT, padx=30, pady=30)
tk.Label(Frame4, text="Frame 4",bg="white").pack(padx=10, pady=10)

fenetre.mainloop()


