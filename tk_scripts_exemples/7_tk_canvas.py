# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 17:34:33 2016

@author: chmartin
"""

import tkinter as tk


fenetre = tk.Tk()

# canvas
canvas = tk.Canvas(fenetre, width=300, height=300, background='white')
ligne1 = canvas.create_line(150, 0, 150, 300)
ligne2 = canvas.create_line(0, 150, 300, 150)

cercle2 = canvas.create_oval(100,100,200,200, fill='yellow')
cercle = canvas.create_oval(40,40,260,260, fill='red')
cercle1 = canvas.create_oval(70,70,230,230, fill='orange')
#cercle2 = canvas.create_oval(100,100,200,200, fill='yellow')

txt = canvas.create_text(150, 150, text="Cible", font="Arial 16 italic", fill="blue")

photo = tk.PhotoImage(file="perso.png")
canvas.create_image(0, 0, anchor=tk.NW, image=photo)

canvas.create_rectangle(250, 10, 270, 30, fill='black')
pts = [(20,200),(80,200),(120,280),(0,260)]
canvas.create_polygon(pts, fill="magenta", outline="yellow", width=3)

print (canvas.find_all())
for objet in canvas.find_all() :
    print (objet, canvas.coords(objet), canvas.bbox(objet) )

canvas.pack()
fenetre.mainloop()


