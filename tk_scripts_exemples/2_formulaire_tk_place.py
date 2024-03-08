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
    

fenetre = tk.Tk()
fenetre.configure(height = 1000, width = 1000)
# labels
label = tk.Label(fenetre, text="Donnez-nous quelques renseignements ...\n", font=("Helvetica", 16))
label.place(x = 30, y = 30)

label = tk.Label(fenetre, text="Nom :")
label.place(x = 30, y = 110)

# entrée
value_nom = tk.StringVar() 
entree = tk.Entry(fenetre, textvariable=value_nom, width=30)
entree.place(x = 150, y = 110)

# case à cocher ...
value_check = tk.StringVar() 
bouton = tk.Checkbutton(fenetre, text="Nouveau ?", variable=value_check, onvalue='oui', offvalue='non')
bouton.deselect()
bouton.place(x = 800, y = 110)

# boutons 'radio'
label = tk.Label(fenetre, text="Etes-vous de bonne humeur ?")
label.place(x = 30, y = 180)
value_radio = tk.StringVar() 
bouton1 = tk.Radiobutton(fenetre, text="Oui", variable=value_radio, value='oui')
bouton2 = tk.Radiobutton(fenetre, text="Non", variable=value_radio, value='non')
bouton1.select()
bouton1.place(x = 500, y = 180)
bouton2.place(x = 500, y = 230)

# Scale
value_scale = tk.DoubleVar()
scale = tk.Scale(fenetre, variable=value_scale, orient='horizontal', from_=18, to=25,
      resolution=1, tickinterval=1, length=350,
      label='Quel est votre age ? ')
scale.place(x = 5, y = 280)

# liste
label = tk.Label(fenetre, text="Quel est votre langage préféré ?")
label.place(x = 10, y = 450)
liste = tk.Listbox(fenetre, height=3, selectmode='multiple')
liste.insert(1, "Python")
liste.insert(2, "PHP")
liste.insert(3, "...")
liste.place(x = 400, y = 450)

#Spinbox
label = tk.Label(fenetre, text="Combien de langages connaissez-vous ?")
label.place(x = 10, y = 580)
s = tk.Spinbox(fenetre, from_=0, to=10)
s.place(x = 600, y = 580)


## bouton de validation
bouton=tk.Button(fenetre, text="Valider", command=valider)
bouton.place(x = 300, y=800)
## bouton de sortie
bouton=tk.Button(fenetre, text="Fermer", command=fenetre.quit)
bouton.place(x = 700, y=800)

fenetre.title('Premier formulaire .... avec la méthode place !')

fenetre.mainloop()
