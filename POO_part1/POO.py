from datetime import datetime
from unidecode import unidecode


def dialogue(nom, age):
    vingt_ans = 2019+(20-age)
    if age < 20:
        print(f"{nom} vous avez {age} ans et vous en aurez 20 ans en {vingt_ans}.")
    elif age == 20:
        print(f"{nom} vous avez {age} ans.")
    else:
        print(f"{nom} vous avez {age} ans et vous en avais 20 ans en {vingt_ans}")


def dialogue1(nom, date_naissance):
    ajd = datetime.today()
    idade = ajd.year - date_naissance.year - \
        ((ajd.month, ajd.day) < (date_naissance.month, date_naissance.day))
    vingt_ans = date_naissance.year + 20

    if idade < 20:
        print(f"{nom}, vous avez {idade} ans et vous aurez 20 ans em {vingt_ans}.")
    elif idade == 20:
        print(f"{nom}, vous avez {idade} ans.")
    else:
        print(f"{nom}, vous avez {idade} ans et vous avez eu 20 ans em {vingt_ans}.")


def ligne_croix(carac):
    print(f"{'+'*len(carac)}")


ligne_croix("cabra")


def triangle_croix(entier):
    for i in range(entier):
        if i % 2 == 0:
            print(f"{' '*(i//2) + '+'*(entier - i)} ")


def nb_multiples(valeur_max, nombre_interet):
    print(valeur_max // nombre_interet)


def voyelles(carac):
    voye = ['a', 'e', 'i', 'o', 'u']
    carac = unidecode(carac.replace(" ", "").lower())
    j = 0
    for i in carac:
        if i in voye:
            j += 1
    print(f"Le chaîne de caractères a {j} voyelles.")


def saison(date):
    pass
