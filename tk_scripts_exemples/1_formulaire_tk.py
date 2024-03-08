# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 14:33:47 2016

@author: chmartin
"""

import tkinter as tk
 
    
def valider():
    if value_nom.get() :
        print (value_nom.get())
        print (value_check.get())
        print (value_radio.get())
        print (value_scale.get())
        for index in liste.curselection() :
            print (liste.get(index))
        print (s.get())
    else :
        print ('Vous devez au moins saisir votre nom')
    

#-------------------------------------------
fenetre = tk.Tk()

# labels
label = tk.Label(fenetre, text="Donnez-nous quelques renseignements ...\n", font=("Helvetica", 16))
label.pack()
label = tk.Label(fenetre, text="Nom :")
label.pack()

# entrée
value_nom = tk.StringVar() 
entree = tk.Entry(fenetre, textvariable=value_nom, width=30)
entree.pack()

# case à cocher ...
value_check = tk.StringVar() 
bouton = tk.Checkbutton(fenetre, text="Nouveau ?", variable=value_check, onvalue='oui', offvalue='non')
bouton.deselect()
bouton.pack()

# boutons 'radio'
label = tk.Label(fenetre, text="Etes-vous de bonne humeur ?")
label.pack()
value_radio = tk.StringVar() 
bouton1 = tk.Radiobutton(fenetre, text="Oui", variable=value_radio, value='oui')
bouton2 = tk.Radiobutton(fenetre, text="Non", variable=value_radio, value='non')
bouton1.select()
bouton1.pack()
bouton2.pack()

# Scale
value_scale = tk.DoubleVar()
scale = tk.Scale(fenetre, variable=value_scale, orient='horizontal', from_=18, to=25,
      resolution=1, tickinterval=1, length=350,
      label='Quel est votre age ? ')
scale.pack()

# liste
label = tk.Label(fenetre, text="Quel est votre langage préféré ?")
label.pack()
liste = tk.Listbox(fenetre, height=3, selectmode='multiple')
liste.insert(1, "Python")
liste.insert(2, "PHP")
liste.insert(3, "...")
liste.pack()

#Spinbox
label = tk.Label(fenetre, text="Combien de langages connaissez-vous ?")
label.pack()
s = tk.Spinbox(fenetre, from_=0, to=10)
s.pack()


## bouton de validation
bouton=tk.Button(fenetre, text="Valider", command=valider)
bouton.pack()
## bouton de sortie
bouton=tk.Button(fenetre, text="Fermer", command=fenetre.quit)
bouton.pack()

fenetre.title('Premier formulaire ....')

fenetre.mainloop()
