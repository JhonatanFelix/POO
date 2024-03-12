import pandas as pd
import numpy as np
import math
import random


# ================ Fonctions pour utiliser ==================================


def function_detecter_coyote(valeur):
    if valeur < 0:
        return 0
    elif valeur < 1:
        return valeur
    elif valeur < 20:
        return -valeur/20 + 20/19
    else:
        return 0


def function_detecter_blaireau(valeur):
    if valeur < 0:
        return 0
    elif valeur < 1:
        return 1
    else:
        return math.exp(-(valeur - 1)/2)


def function_detecter_predateur():
    return 0.5


# ================== Class plus géneral ======================================

class Animal:
    def __init__(self, position):
        self.position = np.array(position)
        self.direction = np.array([0, 0])
        self.captured_prey = None

    def move(self, vector):
        # La fonction va recevoir un vector de 2 dimensions [x,y]
        self.position += np.array(vector)


# ========================= Proie =====================================================

class Proie(Animal):
    def __init__(self, position):
        super().__init__(position)

        self.identified_predator = False
        # Tenho que fazer a condição para mudar isso dentro da simulação
        self.identified_haie = False

    def find_haie_plus_proche(self, haies):
        '''Essa função precisa receber o champ.obstacles como arbustos para funcionar
        pois ela vai pegar a lista de arbustos, medir a distância, selecionar o arbusto
        mais próximo.'''

        distances = [math.dist(obstaculo.position, self.position)
                     for obstaculo in haies]
        premier = distances.index(min(distances))

        return haies[premier]

    def marcher_haie(self, haie):
        '''Ideia melhor: primeiro dentro do jogo vamos verificar se existe tal arbusto,
        se sim vamos poder andar em direção a ele. Portanto, essa função vai receber o
        arbusto já sabendo que ele está nas condições que eu quero. E sendo assim a minha
        presa vai poder andar em direção a ele.'''

        if self.position[0] != haie.position[0]:
            self.move([1, 0])
        elif self.position[1] != haie.position[1]:
            self.move([0, 1])


    def detecter_predateur(self, list_predators):
        distances = [math.dist(self.position, predateur.position)
                     for predateur in list_predators]
        filtered_list = np.array(distances) < 8

        for i, valeur in enumerate(filtered_list):
            if valeur == 1:
                probabilite = function_detecter_predateur()
                if random.random() < probabilite:
                    filtered_list[i] = 0

        if len(filtered_list[filtered_list]) >= 1:
            self.identified_predator = True
        

    def senfuire(self, predateur):
        '''De novo, calcula a presença de um predador próximo, e se estiver dentro de uma
        distância mínima n então a presa foge, mas só se ela estiver fora do arbusto. A 
        presa vai calcular a distância máxima que ela pode ficar de um predador e correr
        exatamente para esse ponto.'''
        positions = []
        for i in range(-3, 4):
            positions.append(self.position + np.array([i, 0]))
        for i in range(-3, 4):
            positions.append(self.position + np.array([0, i]))

        # Calculando a mínima e para onde correr
        distances = [math.dist(possibilities, predateur.position)
                     for possibilities in positions]
        premier = distances.index(max(distances))

        # Aqui temos a locomoção da presa para onde ela fugiu
        self.position = positions[premier]


# =========================== Predateur =================================================

class Predateur(Animal):
    def __init__(self, position):
        super().__init__(position)
        self.is_satiated = False
        self.satiated_turns_remaining = 0
        self.assisting_other = False
        self.without_meat = 0

        self.identified_prey = False

    def detecter(self, proies):
        ''' Essa função deve receber a lista de presas, verificar se alguma foi identificada
        de acordo com uma função de (quase)probabilidade pré-determinada e com isso verificar
        a mais próxima e passar para a função de caça.'''
        pass

    def hunt(self, prey):
        '''Essa função vai receber uma presa para caçar, e ela vai precisar avaliar os possíveis
        caminhos para poder alcançar essa presa.'''
        possibilities = []
        for i in range(-5, 6):
            possibilities.append(self.position + np.array([i, 0]))
        for i in range(-5, 6):
            possibilities.append(self.position + np.array([0, i]))
        for i in range(-5, 6):
            possibilities.append(self.position + np.array([i, i]))

        distances = [math.dist(positions, prey.position)
                     for positions in possibilities]
        premier = distances.index(min(distances))
        self.position = positions[premier]


    def is_dead(self, prey, list_preys):
        '''Essa é para verificar se matou uma presa e muda o status do predador. Recebe a 
        presa específica, e vai receber também champ.proies para conseguir deletar uma 
        presa específcia depois que ela morrer.
        A condição de posições iguais tem que estar necessariamente antes de começar o
        código para poder fazer esass coisas.'''
        list_preys.remove(prey)
        self.is_satiated = True
        self.satiated_turns_remaining = 2
        self.without_meat = 0

    def death(self, list_predators, days_wihout_eating):
        ''' Essa funçaõ vai receber a lista de predadores para matar o animal depois
        de days_wihout_eating dias sem comer.'''
        if self.without_meat >= days_wihout_eating:
            list_predators.remove(self)

    def random_walk(self):
        pass


# ========================== Animaux predateurs ===========================================


class Blaireau(Predateur):
    def __init__(self, position):
        super().__init__(position)


class Blaireau(Predateur):
    def __init__(self, position):
        super().__init__(position)


# =========================== Les proies ===================================================

class PrairieChien(Proie):
    def __init__(self, position):
        super().__init__(position)


class Écureuil(Proie):
    def __init__(self, position):
        super().__init__(position)


# ============================= Les lieux =================================================

class Haie:
    def __init__(self, position):
        self.position = position


class Champ:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.proies = []
        self.predateurs = []
        self.obstacles = []
        self.turn = 0

    def add_proies(self, animal):
        self.proies.append(animal)

    def add_predateurs(self, animal):
        self.predateurs.append(animal)

    def add_obstacle(self, obstacle):
        self.obstacles.append(obstacle)

    def pass_turn(self):
        self.turn += 1


# ================================Implementation ====================================

# Créer un dictionnaire pour faire les probabilités
df = pd.read_csv("probabilites.csv")
probabilites = {}

for index, row in df.iterrows():
    # Separation des strings
    predateur, proie = row['Distance proie - prédateur (m)'].split('->')

    for col in df.columns[1:]:
        clé = (str(col) if col.isdigit() else col, predateur, proie)
        # Determination de valuer pour chaque clé
        probabilites[clé] = row[col]


if __name__ == '__main__':
    champ = Champ(10, 10)  # Initialize field with size N x M

    # A lógica do predador de turnos necessários para mudar os status tem que ser
    # mudada especificamente aqui.

    # A lógica de que o predador fica parado depois que comer tem que ser adicionada
    # aqui também.
    # Add predators and prey
    # Add hedges

    # Start simulation
    while not champ.is_simulation_over():
        champ.simulate_turn()
