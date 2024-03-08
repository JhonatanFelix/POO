# -*- coding: utf-8 -*-
"""
@author: chmartin
"""



import tkinter as tk

# fonction appellée lorsque l'utilisateur presse une touche
def clavier(event):
    
    x1, y1, x2, y2 = canvas.bbox(personnage)
    
    touche = event.keysym

    if touche == "Up" and y1 > 0 : 
        canvas.move(personnage, 0, -pas)
    elif touche == "Down" and y2 < hauteur_plateau :
        canvas.move(personnage, 0, pas)
    elif touche == "Right" and x2 < largeur_plateau:
        canvas.move(personnage, pas, 0)
    elif touche == "Left" and x1 > 0:
        canvas.move(personnage, -pas, 0)

      
            

###############################################################################
#         Programme principal                                                 #
###############################################################################
      

fenetre = tk.Tk()
nb_lignes = 10
nb_colonnes = 10
pas = 50
largeur_plateau = nb_lignes*pas
hauteur_plateau = nb_colonnes*pas

# création du canvas
canvas = tk.Canvas(fenetre, width=largeur_plateau, height=hauteur_plateau, bg="ivory")

photo = tk.PhotoImage(width=pas, height=pas, file="perso.png")

personnage = canvas.create_image(0, 0, anchor=tk.NW, image=photo)

# ajout du bind sur les touches du clavier
canvas.focus_set()
canvas.bind("<Key>", clavier)

# Ajout du canvas dans le fenetre
canvas.pack()
fenetre.mainloop()
