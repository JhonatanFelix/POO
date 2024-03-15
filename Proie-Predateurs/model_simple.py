import pandas as pd
import numpy as np
import math
import random
import tkinter as tk

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


def function_detecter_proie():  # mudar saporra para ficar com =1 no intervalo muito perto
    return 0.5


# ================== Class plus géneral ======================================

class Animal:
    def __init__(self, position):
        self.position = np.array(position)
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
        self.is_in_haie = False

        self.s_predateurs = []
        self.haie_plus_proche = None

    def detecter_haie(self, haies):
        if self.is_in_haie == False and self.identified_haie == False:
            distances = np.array([math.dist(obstaculo.position, self.position)
                                  for obstaculo in haies])
            proches = distances[distances < 6]
            array_haies = np.array(haies)
            array_haies = array_haies[proches]

            if len(array_haies) > 0:
                self.identified_haie = True
            else:
                self.identified_haie = False

    def find_haie_plus_proche(self, haies):
        '''Essa função precisa receber o champ.obstacles como arbustos para funcionar
        pois ela vai pegar a lista de arbustos, medir a distância, selecionar o arbusto
        mais próximo.'''
        if self.is_in_haie == False and self.identified_predator == False:
            if haies != []:
                distances = [math.dist(obstaculo.position, self.position)
                             for obstaculo in haies]
                premier = distances.index(min(distances))

                self.haie_plus_proche = haies[premier]
            else:
                self.haie_plus_proche = None
        else:
            pass

    def marcher_haie(self, haie=None):
        '''Ideia melhor: primeiro dentro do jogo vamos verificar se existe tal arbusto,
        se sim vamos poder andar em direção a ele. Portanto, essa função vai receber o
        arbusto já sabendo que ele está nas condições que eu quero. E sendo assim a minha
        presa vai poder andar em direção a ele.'''
        if haie != None:
            if self.position[0] != haie.position[0]:
                if self.position[0] > haie.position[0]:
                    self.move([1, 0])
                else:
                    self.move([-1, 0])
            elif self.position[1] != haie.position[1]:
                if self.position[1] > haie.position[1]:
                    self.move([0, 1])
                else:
                    self.move([0, -1])
            else:
                self.is_in_haie = True
        else:
            pass

    def detecter_predateur(self, list_predators):
        array_predators = np.array(list_predators)
        distances = [math.dist(self.position, predateur.position)
                     for predateur in list_predators]
        filtered_list = np.array(distances) < 8

        for i, valeur in enumerate(filtered_list):
            if valeur == 1:
                probabilite = function_detecter_proie()
                if random.random() < probabilite:
                    filtered_list[i] = 0

        if len(filtered_list[filtered_list]) >= 1:
            self.identified_predator = True
            self.s_predateurs = array_predators[filtered_list]

    def senfuire(self, predateur, champ):
        '''Tenho que mudar essa função, pois vão existir lugares no mapa onde la proie não
        vai poder fugir, então, eu tenho que sempre considerar esses pontos.'''

        '''De novo, calcula a presença de um predador próximo, e se estiver dentro de uma
        distância mínima n então a presa foge, mas só se ela estiver fora do arbusto. A 
        presa vai calcular a distância máxima que ela pode ficar de um predador e correr
        exatamente para esse ponto.'''
        if True:
            if self.identified_predator == True:
                if self.is_in_haie == False or predateur.position == self.position:
                    positions = []
                    for i in range(-3, 4):
                        positions.append(self.position + np.array([i, 0]))
                    for i in range(-3, 4):
                        positions.append(self.position + np.array([0, i]))

                    positions = np.array(positions)
                    positions = positions[positions[:, 0] < champ.width]
                    positions = positions[positions[:, 1] < champ.height]
                    positions = positions[positions[:, 0] > 0]
                    positions = positions[positions[:, 1] > 0]

                    # Calculando a mínima e para onde correr
                    distances = [math.dist(possibilities, predateur.position)
                                 for possibilities in positions]
                    premier = distances.index(max(distances))

                    # Aqui temos a locomoção da presa para onde ela fugiu
                    self.position = positions[premier]
                    self.is_in_haie = False
        else:
            pass

    def update_state(self, champ):
        self.detecter_predateur(champ.predateurs)
        if self.identified_predator == True:
            if self.is_in_haie == True:
                if np.array([predateur.position for predateur in champ.predateurs]).any() == self.position:
                    self.senfuire(self.s_predateurs[0], champ)
                else:
                    pass
            else:
                self.senfuire(self.s_predateurs[0], champ)
        else:
            if self.identified_haie == True:
                self.marcher_haie(self.haie_plus_proche)
            else:
                self.find_haie_plus_proche(champ.obstacles)


# =========================== Predateur =================================================

class Predateur(Animal):
    def __init__(self, position):
        super().__init__(position)
        self.is_satiated = False
        self.assisting_other = False
        self.without_meat = 0
        self.s_proie = None

        self.identified_prey = False
        self.died = False

    def detecter(self, list_proies):
        ''' Essa função deve receber a lista de presas, verificar se alguma foi identificada
        de acordo com uma função de (quase)probabilidade pré-determinada e com isso verificar
        a mais próxima e passar para a função de caça.'''
        array_proies = np.array(list_proies)
        distances = [math.dist(self.position, proie.position)
                     for proie in list_proies]
        filtered_list = np.array(distances) < 15

        for i, valeur in enumerate(filtered_list):
            if valeur == 1:
                probabilite = function_detecter_coyote(distances[i])
                if random.random() < probabilite:
                    filtered_list[i] = 0

        if len(filtered_list[filtered_list]) >= 1:
            self.identified_prey = True
            self.s_proie = array_proies[filtered_list][0]

    def hunt(self, prey, champ):
        '''Essa função vai receber uma presa para caçar, e ela vai precisar avaliar os possíveis
        caminhos para poder alcançar essa presa.'''
        if prey != None:
            if self.identified_prey == True:
                possibilities = []

                for i in range(-5, 6):
                    possibilities.append(self.position + np.array([i, 0]))
                for i in range(-5, 6):
                    possibilities.append(self.position + np.array([0, i]))
                for i in range(-5, 6):
                    possibilities.append(self.position + np.array([i, i]))

                possibilities = np.array(possibilities)
                possibilities = possibilities[possibilities[:, 0]
                                              < champ.width]
                possibilities = possibilities[possibilities[:, 1]
                                              < champ.height]
                possibilities = possibilities[possibilities[:, 0]
                                              > 0]
                possibilities = possibilities[possibilities[:, 1]
                                              > 0]

                distances = [math.dist(positions, prey.position)
                             for positions in possibilities]
                premier = distances.index(min(distances))
                self.position = possibilities[premier]
            else:
                pass
        else:
            pass

    def is_dead(self, list_preys):
        '''Essa é para verificar se matou uma presa e muda o status do predador. Recebe a 
        presa específica, e vai receber também champ.proies para conseguir deletar uma 
        presa específcia depois que ela morrer.
        A condição de posições iguais tem que estar necessariamente antes de começar o
        código para poder fazer esass coisas.'''
        if self.s_proie != None:
            if self.position[0] == self.s_proie.position[0] and self.position[1] == self.s_proie.position[1]:
                if self.s_proie in list_preys:
                    list_preys.remove(self.s_proie)
                self.is_satiated = True
                self.without_meat = 0
                self.identified_prey = False
                self.s_proie = None

        else:
            pass

    def death(self, champ):
        ''' Essa funçaõ vai receber a lista de predadores para matar o animal depois
        de days_wihout_eating dias sem comer.'''
        if self in champ.predateurs:
            champ.predateurs.remove(self)

    def random_walk(self):
        pass

    def update_state(self, champ):
        self.without_meat += 1
        if self.without_meat >= 25:
            self.death(champ)
        elif self.without_meat > 2:
            if self.identified_prey == False:
                self.detecter(champ.proies)

            self.hunt(self.s_proie, champ)  # Caça a presa identificada
            # Verifica se conseguiu matar a presa
            self.is_dead(champ.proies)
        else:
            pass  # O predador fica parado se não estiver com fome

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
    def __init__(self, width=50, height=50):
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

    def process_turn(self):
        for predateur in self.predateurs:
            predateur.update_state(self)
        for proies in self.proies:
            proies.update_state(self)

        self.turn += 1

# ================================Implementation ====================================


# Créer un dictionnaire pour faire les probabilités
df = pd.read_csv("Proie-Predateurs/probabilites.csv")
probabilites = {}

for index, row in df.iterrows():
    # Separation des strings
    predateur, proie = row['Distance proie - prédateur (m)'].split('->')

    for col in df.columns[1:]:
        clé = (str(col) if col.isdigit() else col, predateur, proie)
        # Determination de valuer pour chaque clé
        probabilites[clé] = row[col]


# ============================ Game ==========================================
class GameBoard(tk.Tk):
    def __init__(self, champ, cell_size=10):
        super().__init__()
        self.title("Prédateur-Proie Simulation")

        self.champ = champ
        self.rows = champ.height
        self.cols = champ.width
        self.cell_size = cell_size

        self.label_turn = tk.Label(self, text=f"Turno: {self.champ.turn}")
        self.label_turn.pack()

        self.canvas = tk.Canvas(
            self, height=self.rows * self.cell_size, width=self.cols * self.cell_size)
        self.canvas.pack()

        self.draw_grid()
        self.update()  # Chama o método de atualização para iniciar a simulação

    def draw_grid(self):
        for i in range(self.rows):
            self.canvas.create_line(
                0, i * self.cell_size, self.cols * self.cell_size, i * self.cell_size)
        for i in range(self.cols):
            self.canvas.create_line(
                i * self.cell_size, 0, i * self.cell_size, self.rows * self.cell_size)

    def place_objects(self):
        self.canvas.delete("all")  # Limpa o canvas antes de redesenhar
        self.draw_grid()  # Redesenhar a grade pode ser opcional, dependendo do desejado
        for predator in self.champ.predateurs:
            self.draw_object(predator.position, 'red')

        for prey in self.champ.proies:
            self.draw_object(prey.position, 'blue')

        for haie in self.champ.obstacles:
            self.draw_object(haie.position, 'green')

    def draw_object(self, position, color):
        x, y = position
        self.canvas.create_rectangle(x * self.cell_size, y * self.cell_size,
                                     (x + 1) * self.cell_size, (y + 1) * self.cell_size, fill=color)

    def update(self):
        # print(self.champ.predateurs[0].without_meat)
        self.champ.process_turn()  # Processa um turno do jogo
        self.place_objects()  # Atualiza a visualização com os novos estados
        self.label_turn.config(text=f"Turno:{self.champ.turn}")
        # Aguarda 1000ms (1 segundo) e chama update novamente
        self.after(100, self.update)


# ======================= Add Predateurs et Proies ================================

def create_and_add_predateurs(champ, number_of_predateurs):
    for _ in range(number_of_predateurs):
        x = random.randint(0, champ.width - 1)
        y = random.randint(0, champ.height - 1)

        new_predator = Predateur(position=[x, y])

        champ.add_predateurs(new_predator)


def create_and_add_proies(champ, number_of_proies):
    for _ in range(number_of_proies):
        x = random.randint(0, champ.width - 1)
        y = random.randint(0, champ.height - 1)

        new_proie = Proie(position=[x, y])

        champ.add_proies(new_proie)


champ = Champ(50, 50)
create_and_add_predateurs(champ, 10)
create_and_add_proies(champ, 50)


# Iniciar a simulação com uma interface gráfica
game_board = GameBoard(champ)
game_board.mainloop()