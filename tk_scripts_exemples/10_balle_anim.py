# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 14:14:12 2017

@author: chmartin
"""

import tkinter as tk
import math,random

LARGEUR = 480
HAUTEUR = 320
RAYON = 15 # rayon de la balle

# position initiale au milieu
X = LARGEUR/2
Y = HAUTEUR/2

# direction initiale aléatoire
vitesse = random.uniform(1.8,2)*5
angle = random.uniform(0,2*math.pi)
DX = vitesse*math.cos(angle)
DY = vitesse*math.sin(angle)

def deplacement():
    """ Déplacement de la balle """
    global X,Y,DX,DY,RAYON,LARGEUR,HAUTEUR
    
    # rebond à droite
    if X+RAYON+DX > LARGEUR:
        X = 2*(LARGEUR-RAYON)-X
        DX = -DX
    
    # rebond à gauche
    if X-RAYON+DX < 0:
        X = 2*RAYON-X
        DX = -DX
    
    # rebond en bas
    if Y+RAYON+DY > HAUTEUR:
        Y = 2*(HAUTEUR-RAYON)-Y
        DY = -DY
        
    # rebond en haut
    if Y-RAYON+DY < 0:
        Y = 2*RAYON-Y
        DY = -DY
    
    X = X+DX
    Y = Y+DY
    
    # affichage
    Canevas.coords(Balle,X-RAYON,Y-RAYON,X+RAYON,Y+RAYON)

    # mise à jour toutes les 50 ms
    Mafenetre.after(50,deplacement)

# Création de la fenêtre principale
Mafenetre = tk.Tk()
Mafenetre.title("Animation Balle")

# Création d'un widget Canvas
Canevas = tk.Canvas(Mafenetre,height=HAUTEUR,width=LARGEUR,bg='white')
Canevas.pack(padx=5,pady=5)

# Création d'un objet graphique
Balle = Canevas.create_oval(X-RAYON,Y-RAYON,X+RAYON,Y+RAYON,width=1,fill='green')

deplacement()
Mafenetre.mainloop()