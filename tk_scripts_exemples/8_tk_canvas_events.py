# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 17:34:33 2016

@author: chmartin
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 02:07:04 2016

@author: chmartin
"""

import tkinter as tk 

def Clic(event):
    """ Gestion de l'événement Clic gauche """

    # position du pointeur de la souris
    X = event.x
    Y = event.y
    print("Press : Position du clic -> ",X,Y)


def Drag(event):
    """ Gestion de l'événement bouton gauche enfoncé """
    X = event.x
    Y = event.y
    print("Drag : Position du pointeur -> ",X,Y)



def Clavier(event):
    """ Gestion de l'événement Presser une touche """

    touche = event.keysym
    print ('Clavier : ', touche)



fenetre = tk.Tk()

# canvas
canvas = tk.Canvas(fenetre, width=300, height=300, background='white')
ligne1 = canvas.create_line(150, 0, 150, 300)
ligne2 = canvas.create_line(0, 150, 300, 150)


cercle = canvas.create_oval(40,40,260,260, fill='red')
print(cercle)
cercle1 = canvas.create_oval(70,70,230,230, fill='orange')
cercle2 = canvas.create_oval(100,100,200,200, fill='yellow')

txt = canvas.create_text(150, 150, text="Cible", font="Arial 16 italic", fill="blue")

photo = tk.PhotoImage(file="perso.png")
canvas.create_image(0, 0, anchor=tk.NW, image=photo)

canvas.create_rectangle(250, 10, 270, 30, fill='black')
pts = [(20,200),(80,200),(120,280),(0,260)]
canvas.create_polygon(pts, fill="magenta", outline="yellow", width=3)

print (canvas.find_all())
for objet in canvas.find_all() :
    print (objet, canvas.coords(objet), canvas.bbox(objet) )

canvas.focus_set() #permet d'indiquer que les évènements clavier seront reçu par la canvas
canvas.bind("<Key>", Clavier) # évènement touche enfoncée
canvas.bind('<Button-1>',Clic) # évévement clic gauche
canvas.bind('<B1-Motion>',Drag) # événement bouton gauche enfoncé

canvas.pack()
help(fenetre.focus_set)
fenetre.mainloop()


