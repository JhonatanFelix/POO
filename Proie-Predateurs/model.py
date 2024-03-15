import pandas as pd
import numpy as np
import math
import random
import tkinter as tk

# ================ Fonctions pour utiliser ==================================


def save_data_simulation(champ, name_file="simulacao_resultados.xlsx"):

    data_simulation = {
        "width": champ.width,
        "height": champ.height,
        "haie": len(champ.obstacles),

        "n_coyote_start": champ.coyote_i,
        "n_blaireau_start": champ.blaireau_i,
        "n_prairiechien_start": champ.prairiechien_i,
        "n_ecureuil_start": champ.ecureuil_i,
        "n_coyote_final": len(champ.coyote),
        "n_blaireau_final": len(champ.blaireau),
        "n_prairiechien_final": len(champ.prairiechien),
        "n_ecureuil_final": len(champ.ecureuil),

        "maximum_turns_coyote": champ.maximum_turns_coyote,
        "maximum_turns_blaireau": champ.maximum_turns_blaireau,
        "turns_total": champ.turn
    }

    new_df = pd.DataFrame([data_simulation])

    try:

        with pd.ExcelWriter(name_file, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
            # Lê o arquivo existente para não sobrescrever outros dados além do necessário
            existing_data = pd.read_excel(name_file)

            complete_data = pd.concat(
                [existing_data, new_df], ignore_index=True)
            complete_data.to_excel(writer, index=False, sheet_name='Sheet1')

    except FileNotFoundError:
        new_df.to_excel(name_file, index=False)


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

        self.identified_haie = False
        self.is_in_haie = False

        self.s_predateurs = []
        self.haie_plus_proche = None

        self.got_captured = False

    def detecter_haie(self, haies):
        if self.is_in_haie == False and self.identified_haie == False:
            distances = np.array([math.dist(obstaculo.position, self.position)
                                  for obstaculo in haies])
            proches = distances < 4
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
            if len(haies) > 0:
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
                    self.move([-1, 0])
                else:
                    self.move([1, 0])
            elif self.position[1] != haie.position[1]:
                if self.position[1] > haie.position[1]:
                    self.move([0, -1])
                else:
                    self.move([0, 1])
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
        else:
            self.identified_predator = False

    def senfuire(self, predateur, champ):
        '''Tenho que mudar essa função, pois vão existir lugares no mapa onde la proie não
        vai poder fugir, então, eu tenho que sempre considerar esses pontos.'''

        '''De novo, calcula a presença de um predador próximo, e se estiver dentro de uma
        distância mínima n então a presa foge, mas só se ela estiver fora do arbusto. A 
        presa vai calcular a distância máxima que ela pode ficar de um predador e correr
        exatamente para esse ponto.'''
        if True:
            if self.identified_predator == True:
                if self.is_in_haie == False or (predateur.position[0] == self.position[0] and predateur.position[1] == self.position[1]):
                    positions = []
                    for i in range(-3, 4):
                        positions.append(self.position + np.array([i, 0]))
                        positions.append(self.position + np.array([0, i]))

                    positions = np.array(positions)
                    positions = positions[positions[:, 0] < champ.width]
                    positions = positions[positions[:, 1] < champ.height]
                    positions = positions[positions[:, 0] > 0]
                    positions = positions[positions[:, 1] > 0]

                    # Calculando a mínima e para onde correr
                    distances = [math.dist(possibilities, predateur.position)
                                 for possibilities in positions]
                    if len(distances) != 0:
                        premier = distances.index(max(distances))
                        self.position = positions[premier]
                        self.is_in_haie = False
                    else:
                        pass
        else:
            pass

    def random_walk(self, champ, n_pas):
        if self.identified_haie == False and self.identified_predator == False:
            positions = []
            for i in range(-n_pas, n_pas+1):
                positions.append(self.position + np.array([i, 0]))
                positions.append(self.position + np.array([0, i]))

            positions = np.array(positions)
            positions = positions[positions[:, 0] < champ.width]
            positions = positions[positions[:, 1] < champ.height]
            positions = positions[positions[:, 0] > 0]
            positions = positions[positions[:, 1] > 0]

            if len(positions) > 0:
                aleatoire = np.random.randint(0, len(positions)-1)
                self.position = positions[aleatoire]
            else:
                pass
        else:
            pass

    def update_state(self, champ):
        self.detecter_predateur(champ.predateurs)
        self.detecter_haie(champ.obstacles)

        if self.got_captured == False:
            if self.identified_predator == True:
                if self.is_in_haie == True:
                    if self.position in np.array([predateur.position for predateur in champ.predateurs]):
                        self.senfuire(self.s_predateurs[0], champ)
                    else:
                        pass
                else:
                    self.senfuire(self.s_predateurs[0], champ)
            else:
                if self.identified_haie == True:
                    self.find_haie_plus_proche(champ.obstacles)
                    self.marcher_haie(self.haie_plus_proche)
                else:
                    self.random_walk(champ, 3)
                    self.detecter_haie(champ.obstacles)
                    self.find_haie_plus_proche(champ.obstacles)
        else:
            self.got_captured = False

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

        self.killed_ensemble = False

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
                    possibilities.append(self.position + np.array([0, i]))
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
                if len(distances) != 0:
                    premier = distances.index(min(distances))
                    self.position = possibilities[premier]
                else:
                    pass
            else:
                pass
        else:
            pass

    def is_dead(self, champ):
        '''Essa é para verificar se matou uma presa e muda o status do predador. Recebe a 
        presa específica, e vai receber também champ.proies para conseguir deletar uma 
        presa específcia depois que ela morrer.
        A condição de posições iguais tem que estar necessariamente antes de começar o
        código para poder fazer esass coisas.'''
        if self.s_proie != None:
            if self.position[0] == self.s_proie.position[0] and self.position[1] == self.s_proie.position[1]:
                if self.s_proie in champ.proies:
                    champ.proies.remove(self.s_proie)
                self.is_satiated = True
                self.without_meat = 0
                self.identified_prey = False
                self.s_proie = None

        else:
            pass

    def is_dead_ensemble(self, champ):  # o champ aqui é pra usar a lista de presas

        if self.s_proie != None:
            positions = []
            for i in range(-15, 16):
                positions.append(self.position + np.array([i, 0]))
                positions.append(self.position + np.array([0, i]))
                positions.append(self.position + np.array([i, i]))

            positions = np.array(positions)
            positions = positions[positions[:, 0] < champ.width]
            positions = positions[positions[:, 1] < champ.height]
            positions = positions[positions[:, 0] > 0]
            positions = positions[positions[:, 1] > 0]

            if self.s_proie.position in positions:

                d_coyote_proie = round(
                    math.dist(self.position, self.s_proie.position))
                if d_coyote_proie >= 15:
                    d_coyote_proie = '15+'
                elif d_coyote_proie >= 9:
                    d_coyote_proie = '9+'
                elif d_coyote_proie >= 1:
                    d_coyote_proie = str(
                        round(math.dist(self.position, self.s_proie.position)))
                else:
                    d_coyote_proie = '1'

                if proie in champ.ecureuil:
                    p_coyote_ecureuil = probabilites[(
                        d_coyote_proie, 'coyote+blaireau', 'écureuil')]

                    if random.random() < p_coyote_ecureuil:
                        champ.ecureuil.remove(proie)
                        if proie in champ.proies:
                            champ.proies.remove(proie)

                        self.killed_ensemble = True
                    else:
                        proie.got_captured = True
                        positions1 = np.array([self.position + np.array([1, 0]),
                                               self.position +
                                               np.array([0, 1]),
                                               self.position -
                                               np.array([1, 0]),
                                               self.position - np.array([0, 1])])
                        positions1 = positions1[positions1[:, 0] > 0]
                        positions1 = positions1[positions1[:, 1] > 0]
                        positions1 = positions1[positions1[:, 0] < champ.width]
                        positions1 = positions1[positions1[:, 1]
                                                < champ.height]

                        aleatoire = random.randint(0, len(positions1)-1)

                        self.killed_ensemble = False
                        if len(positions1) > 0:
                            proie.position = positions1[aleatoire]
                        else:
                            proie.got_captured = False

                elif proie in champ.prairiechien:

                    p_coyote_prairiechien = probabilites[(
                        d_coyote_proie, 'coyote+blaireau', 'chien de prairie')]

                    if random.random() < p_coyote_prairiechien:

                        champ.ecureuil.remove(proie)
                        if proie in champ.proies:
                            champ.proies.remove(proie)

                        self.killed_ensemble = True
                        # self.is_satiated = True         # tenho que tirar saporra pq se não dá problema quando ele pega junto
                        # self.without_meat = 0
                        # self.identified_prey = False
                        # self.s_proie = None
                    else:
                        proie.got_captured = True
                        positions1 = np.array([self.position + np.array([1, 0]),
                                               self.position +
                                               np.array([0, 1]),
                                               self.position -
                                               np.array([1, 0]),
                                               self.position - np.array([0, 1])])
                        positions1 = positions1[positions1[:, 0] > 0]
                        positions1 = positions1[positions1[:, 1] > 0]
                        positions1 = positions1[positions1[:, 0] < champ.width]
                        positions1 = positions1[positions1[:, 1]
                                                < champ.height]

                        aleatoire = random.randint(0, len(positions1)-1)

                        self.killed_ensemble = False
                        if len(positions1) > 0:
                            proie.position = positions1[aleatoire]
                        else:
                            proie.got_captured = False
                else:
                    pass
            else:
                self.hunt(self.s_proie, champ)
        else:
            pass

    def death(self, champ):
        ''' Essa funçaõ vai receber a lista de predadores para matar o animal depois
        de days_wihout_eating dias sem comer.'''
        if self in champ.predateurs:
            champ.predateurs.remove(self)

    def random_walk(self, champ, n_pas):
        if self.identified_prey == False:
            positions = []
            for i in range(-n_pas, n_pas+1):
                positions.append(self.position + np.array([i, 0]))
                positions.append(self.position + np.array([0, i]))
                positions.append(self.position + np.array([i, i]))

            positions = np.array(positions)
            positions = positions[positions[:, 0] < champ.width]
            positions = positions[positions[:, 1] < champ.height]
            positions = positions[positions[:, 0] > 0]
            positions = positions[positions[:, 1] > 0]

            if len(positions) > 0:
                aleatoire = np.random.randint(0, len(positions)-1)
                self.position = positions[aleatoire]
            else:
                pass
        else:
            pass

    def update_state(self, champ):
        self.without_meat += 1
        if self.without_meat >= 25:
            self.death(champ)

        elif self.without_meat > 5:
            if self.identified_prey == False:
                self.detecter(champ.proies)
                self.random_walk(champ, 5)
            else:
                self.hunt(self.s_proie, champ)
            self.is_dead(champ)

        elif self.without_meat > 2:
            if self.identified_prey == False:
                self.detecter(champ.proies)
                self.random_walk(champ, 5)
            else:
                self.hunt(self.s_proie, champ)  # Caça a presa identificada
            # Verifica se conseguiu matar a presa
        else:
            pass

# ========================== Animaux predateurs ===========================================


class Coyote(Predateur):
    def __init__(self, position):
        super().__init__(position)

        self.blaireau_proche = False
        self.s_blaireau = None

    def closest_blaireau(self, champ):
        if self.s_blaireau == None and self.blaireau_proche == False:
            distances = np.array([math.dist(blaireau.position, self.position)
                                  for blaireau in champ.blaireau])
            proches = distances < 2
            array_blaireau = np.array(champ.blaireau)
            array_blaireau = array_blaireau[proches]

            if len(array_blaireau) > 0:
                self.blaireau_proche = True
                self.s_blaireau = array_blaireau[0]
            else:
                self.blaireau_proche = False
                self.s_blaireau = None
        else:
            pass

    def death(self, champ):
        ''' Essa funçaõ vai receber a lista de predadores para matar o animal depois
        de days_wihout_eating dias sem comer.'''
        if self in champ.predateurs:
            champ.predateurs.remove(self)
            champ.coyote.remove(self)

    def is_dead(self, champ):  # o champ aqui é pra usar a lista de presas
        '''Essa é para verificar se matou uma presa e muda o status do predador. Recebe a 
        presa específica, e vai receber também champ.proies para conseguir deletar uma 
        presa específcia depois que ela morrer.
        A condição de posições iguais tem que estar necessariamente antes de começar o
        código para poder fazer esass coisas.'''

        if self.s_proie != None:

            positions = []

            for i in range(-15, 16):
                positions.append(self.position + np.array([i, 0]))
                positions.append(self.position + np.array([0, i]))
                positions.append(self.position + np.array([i, i]))

            positions = np.array(positions)
            positions = positions[positions[:, 0] < champ.width]
            positions = positions[positions[:, 1] < champ.height]
            positions = positions[positions[:, 0] > 0]
            positions = positions[positions[:, 1] > 0]

            if self.s_proie.position in positions:

                d_coyote_proie = round(
                    math.dist(self.position, self.s_proie.position))
                if d_coyote_proie >= 15:
                    d_coyote_proie = '15+'
                elif d_coyote_proie >= 9:
                    d_coyote_proie = '9+'
                elif d_coyote_proie >= 1:
                    d_coyote_proie = str(
                        round(math.dist(self.position, self.s_proie.position)))
                else:
                    d_coyote_proie = '0'

                if self.s_proie in champ.ecureuil:
                    if d_coyote_proie == '0':
                        p_coyote_ecureuil = 1
                    else:
                        p_coyote_ecureuil = probabilites[(
                            d_coyote_proie, 'coyote', 'écureuil')]

                    if random.random() < p_coyote_ecureuil:

                        champ.ecureuil.remove(self.s_proie)
                        if self.s_proie in champ.proies:
                            champ.proies.remove(self.s_proie)

                        self.is_satiated = True
                        self.without_meat = 0
                        self.identified_prey = False
                        self.s_proie = None
                    else:
                        self.s_proie.got_captured = True
                        positions1 = np.array([self.position + np.array([1, 0]),
                                               self.position +
                                               np.array([0, 1]),
                                               self.position -
                                               np.array([1, 0]),
                                               self.position - np.array([0, 1])])
                        positions1 = positions1[positions1[:, 0] > 0]
                        positions1 = positions1[positions1[:, 1] > 0]
                        positions1 = positions1[positions1[:, 0] < champ.width]
                        positions1 = positions1[positions1[:, 1]
                                                < champ.height]

                        aleatoire = random.randint(0, len(positions1)-1)
                        if len(positions1) > 0:
                            self.s_proie.position = positions1[aleatoire]
                        else:
                            self.s_proie.got_captured = False

                elif self.s_proie in champ.prairiechien:
                    if d_coyote_proie == '0':
                        p_coyote_prairiechien = 1
                    else:
                        p_coyote_prairiechien = probabilites[(
                            d_coyote_proie, 'coyote', 'chien de prairie')]

                    if random.random() < p_coyote_prairiechien:
                        champ.prairiechien.remove(self.s_proie)
                        if self.s_proie in champ.proies:
                            champ.proies.remove(self.s_proie)

                        self.is_satiated = True
                        self.without_meat = 0
                        self.identified_prey = False
                        self.s_proie = None
                    else:
                        self.s_proie.got_captured = True
                        positions1 = np.array([self.position + np.array([1, 0]),
                                               self.position +
                                               np.array([0, 1]),
                                               self.position -
                                               np.array([1, 0]),
                                               self.position - np.array([0, 1])])
                        positions1 = positions1[positions1[:, 0] > 0]
                        positions1 = positions1[positions1[:, 1] > 0]
                        positions1 = positions1[positions1[:, 0] < champ.width]
                        positions1 = positions1[positions1[:, 1]
                                                < champ.height]

                        aleatoire = random.randint(0, len(positions1)-1)
                        if len(positions1) > 0:
                            self.s_proie.position = positions1[aleatoire]
                        else:
                            self.s_proie.got_captured = False
                else:
                    pass
            else:
                self.hunt(self.s_proie, champ)
        else:
            pass

    def update_state(self, champ):
        self.without_meat += 1
        self.closest_blaireau(champ)

        if self.s_blaireau != None and self.blaireau_proche == True:
            if self.without_meat >= 25:
                self.death(champ)

            elif self.without_meat > 5:
                if self.identified_prey == False:
                    self.detecter(champ.proies)
                    self.random_walk(champ, 5)
                else:
                    self.hunt(self.s_proie, champ)
                    self.is_dead_ensemble(champ)
                    self.s_blaireau.identified_prey = True
                    self.s_blaireau.s_proie = self.s_proie

                    if self.killed_ensemble == True:
                        if random.random() < 0.1:
                            self.is_satiated = True
                            self.without_meat = 0
                            self.identified_prey = False
                            self.s_proie = None

                            self.s_blaireau.s_proie = None
                            self.s_blaireau.coyote_proche = False
                            self.s_blaireau.killed_ensemble = False

                            self.blaireau_proche = False
                            self.s_blaireau = None
                            self.killed_ensemble = False
                        else:
                            self.s_blaireau.is_satiated = True
                            self.s_blaireau.without_meat = 0
                            self.s_blaireau.identified_prey = False
                            self.s_blaireau.s_proie = None

                            self.s_blaireau.s_proie = None
                            self.s_blaireau.coyote_proche = False
                            self.s_blaireau.killed_ensemble = False

                            self.blaireau_proche = False
                            self.s_blaireau = None
                            self.killed_ensemble = False
                    else:
                        pass
            elif self.without_meat > 2:
                if self.identified_prey == False:
                    self.detecter(champ.proies)
                    self.random_walk(champ, 5)
                else:
                    self.hunt(self.s_proie, champ)
                    self.is_dead_ensemble(champ)
                    self.s_blaireau.identified_prey = True
                    self.s_blaireau.s_proie = self.s_proie

                    if self.killed_ensemble == True:
                        self.s_blaireau.is_satiated = True
                        self.s_blaireau.without_meat = 0
                        self.s_blaireau.identified_prey = False
                        self.s_blaireau.s_proie = None

                        self.s_blaireau.s_proie = None
                        self.s_blaireau.coyote_proche = False
                        self.s_blaireau.killed_ensemble = False

                        self.blaireau_proche = False
                        self.s_blaireau = None
                        self.killed_ensemble = False
                    else:
                        pass
            else:
                self.blaireau_proche = False
                self.s_blaireau = None
                pass
        else:
            if self.without_meat >= 25:
                self.death(champ)

            elif self.without_meat > 5:
                if self.identified_prey == False:
                    self.detecter(champ.proies)
                    self.random_walk(champ, 5)
                else:
                    self.hunt(self.s_proie, champ)
                self.is_dead(champ)

            elif self.without_meat > 2:
                if self.identified_prey == False:
                    self.detecter(champ.proies)
                    self.random_walk(champ, 5)
                else:
                    self.hunt(self.s_proie, champ)  # Caça a presa identificada
            else:
                pass


class Blaireau(Predateur):
    def __init__(self, position):
        super().__init__(position)

        self.s_coyote = None
        self.coyote_proche = False

    def is_dead(self, champ):  # o champ aqui é pra usar a lista de presas
        '''Essa é para verificar se matou uma presa e muda o status do predador. Recebe a 
        presa específica, e vai receber também champ.proies para conseguir deletar uma 
        presa específcia depois que ela morrer.
        A condição de posições iguais tem que estar necessariamente antes de começar o
        código para poder fazer esass coisas.'''

        if self.s_proie != None:
            positions = []
            for i in range(-15, 16):
                positions.append(self.position + np.array([i, 0]))
                positions.append(self.position + np.array([0, i]))
                positions.append(self.position + np.array([i, i]))

            positions = np.array(positions)
            positions = positions[positions[:, 0] < champ.width]
            positions = positions[positions[:, 1] < champ.height]
            positions = positions[positions[:, 0] > 0]
            positions = positions[positions[:, 1] > 0]

            if self.s_proie.position in positions:

                d_coyote_proie = round(
                    math.dist(self.position, self.s_proie.position))
                if d_coyote_proie >= 15:
                    d_coyote_proie = '15+'
                elif d_coyote_proie >= 9:
                    d_coyote_proie = '9+'
                elif d_coyote_proie >= 1:
                    d_coyote_proie = str(
                        round(math.dist(self.position, self.s_proie.position)))
                else:
                    d_coyote_proie = '1'

                if self.s_proie in champ.ecureuil:
                    p_coyote_ecureuil = probabilites[(
                        d_coyote_proie, 'blaireau', 'écureuil')]

                    if random.random() < p_coyote_ecureuil:
                        champ.ecureuil.remove(self.s_proie)
                        if self.s_proie in champ.proies:
                            champ.proies.remove(self.s_proie)

                        self.is_satiated = True
                        self.without_meat = 0
                        self.identified_prey = False
                        self.s_proie = None
                    else:
                        self.s_proie.got_captured = True
                        positions1 = np.array([self.position + np.array([1, 0]),
                                               self.position +
                                               np.array([0, 1]),
                                               self.position -
                                               np.array([1, 0]),
                                               self.position - np.array([0, 1])])
                        positions1 = positions1[positions1[:, 0] > 0]
                        positions1 = positions1[positions1[:, 1] > 0]
                        positions1 = positions1[positions1[:, 0] < champ.width]
                        positions1 = positions1[positions1[:, 1]
                                                < champ.height]

                        aleatoire = random.randint(0, len(positions1)-1)
                        if len(positions1) > 0:
                            self.s_proie.position = positions1[aleatoire]
                        else:
                            self.s_proie.got_captured = False

                elif self.s_proie in champ.prairiechien:

                    p_coyote_prairiechien = probabilites[(
                        d_coyote_proie, 'blaireau', 'chien de prairie')]

                    if random.random() < p_coyote_prairiechien:
                        champ.prairiechien.remove(self.s_proie)
                        if self.s_proie in champ.proies:
                            champ.proies.remove(self.s_proie)

                        self.is_satiated = True
                        self.without_meat = 0
                        self.identified_prey = False
                        self.s_proie = None
                    else:
                        self.s_proie.got_captured = True
                        positions1 = np.array([self.position + np.array([1, 0]),
                                               self.position +
                                               np.array([0, 1]),
                                               self.position -
                                               np.array([1, 0]),
                                               self.position - np.array([0, 1])])
                        positions1 = positions1[positions1[:, 0] > 0]
                        positions1 = positions1[positions1[:, 1] > 0]
                        positions1 = positions1[positions1[:, 0] < champ.width]
                        positions1 = positions1[positions1[:, 1]
                                                < champ.height]

                        aleatoire = random.randint(0, len(positions1)-1)
                        if len(positions1) > 0:
                            self.s_proie.position = positions1[aleatoire]
                        else:
                            self.s_proie.got_captured = False
                else:
                    pass
            else:
                self.hunt(self.s_proie, champ)
        else:
            pass

    def closest_coyote(self, champ):
        if self.s_coyote == None and self.coyote_proche == False:
            distances = np.array([math.dist(coyote.position, self.position)
                                  for coyote in champ.coyote])
            proches = distances < 2
            array_coyote = np.array(champ.coyote)
            array_coyote = array_coyote[proches]

            if len(array_coyote) > 0:
                self.coyote_proche = True
                self.s_coyote = array_coyote[0]
            else:
                self.coyote_proche = False
                self.s_coyote = None
        else:
            pass

    def death(self, champ):
        ''' Essa funçaõ vai receber a lista de predadores para matar o animal depois
        de days_wihout_eating dias sem comer.'''
        if self in champ.predateurs:
            champ.predateurs.remove(self)
            champ.blaireau.remove(self)

    def update_state(self, champ):
        self.without_meat += 1
        self.closest_coyote(champ)

        if self.s_coyote != None and self.coyote_proche == True:
            if self.without_meat >= 21:
                self.death(champ)

            elif self.without_meat > 5:
                if self.identified_prey == False:
                    self.detecter(champ.proies)
                    self.random_walk(champ, 5)
                else:
                    self.hunt(self.s_proie, champ)
                    self.is_dead_ensemble(champ)
                    # self.s_coyote.identified_prey = False
                    # self.s_coyote.s_proie = self.s_proie

                    if self.killed_ensemble == True:
                        if random.random() < 0.1:
                            self.is_satiated = True
                            self.without_meat = 0
                            self.identified_prey = False
                            self.s_proie = None

                            self.s_coyote.s_proie = None
                            self.s_coyote.blaireau_proche = False
                            self.s_coyote.killed_ensemble = False

                            self.coyote_proche = False
                            self.s_coyote = None
                            self.killed_ensemble = False
                        else:
                            self.s_coyote.is_satiated = True
                            self.s_coyote.without_meat = 0
                            self.s_coyote.identified_prey = False
                            self.s_coyote.s_proie = None

                            self.s_coyote.s_proie = None
                            self.s_coyote.blaireau_proche = False
                            self.s_coyote.killed_ensemble = False

                            self.coyote_proche = False
                            self.s_coyote = None
                            self.killed_ensemble = False
                    else:
                        pass
            elif self.without_meat > 2:
                if self.identified_prey == False:
                    self.detecter(champ.proies)
                    self.random_walk(champ, 5)
                else:
                    self.hunt(self.s_proie, champ)
                    self.is_dead_ensemble(champ)
                    self.s_coyote.identified_prey = True
                    self.s_coyote.s_proie = self.s_proie

                    if self.killed_ensemble == True:
                        self.s_coyote.is_satiated = True
                        self.s_coyote.without_meat = 0
                        self.s_coyote.identified_prey = False
                        self.s_coyote.s_proie = None

                        self.s_coyote.s_proie = None
                        self.s_coyote.blaireau_proche = False
                        self.s_coyote.killed_ensemble = False

                        self.coyote_proche = False
                        self.s_coyote = None
                        self.killed_ensemble = False
                    else:
                        pass
            else:
                self.coyote_proche = False
                self.s_coyote = None
                pass
        else:
            if self.without_meat >= 21:
                self.death(champ)

            elif self.without_meat > 5:
                if self.identified_prey == False:
                    self.detecter(champ.proies)
                    self.random_walk(champ, 5)
                else:
                    self.hunt(self.s_proie, champ)
                self.is_dead(champ)

            elif self.without_meat > 2:
                if self.identified_prey == False:
                    self.detecter(champ.proies)
                    self.random_walk(champ, 5)
                else:
                    self.hunt(self.s_proie, champ)  # Caça a presa identificada
            else:
                pass

# =========================== Les proies ===================================================


class PrairieChien(Proie):
    def __init__(self, position):
        super().__init__(position)


class Ecureuil(Proie):
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
        self.turn = 1

        self.coyote = []
        self.blaireau = []
        self.prairiechien = []
        self.ecureuil = []

        self.coyote_i = 0
        self.blaireau_i = 0
        self.prairiechien_i = 0
        self.ecureuil_i = 0

        self.maximum_turns_coyote = 0
        self.maximum_turns_blaireau = 0

    def add_proies(self, animal):
        self.proies.append(animal)

    def add_predateurs(self, animal):
        self.predateurs.append(animal)

    def add_coyote(self, animal):
        self.coyote.append(animal)

    def add_blaireau(self, animal):
        self.blaireau.append(animal)

    def add_ecureuil(self, animal):
        self.ecureuil.append(animal)

    def add_prairiechien(self, animal):
        self.prairiechien.append(animal)

    def add_obstacle(self, obstacle):
        self.obstacles.append(obstacle)

    def pass_turn(self):
        self.turn += 1

    def process_turn(self):
        for predateur in self.predateurs:
            predateur.update_state(self)
        for proies in self.proies:
            proies.update_state(self)

        if self.turn == 2:
            self.coyote_i = len(self.coyote)
            self.blaireau_i = len(self.blaireau)
            self.prairiechien_i = len(self.prairiechien)
            self.ecureuil_i = len(self.ecureuil)

        if len(self.coyote) != 0:
            self.maximum_turns_coyote += 1

        if len(self.blaireau) != 0:
            self.maximum_turns_blaireau += 1

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

        self.label_predateurs = tk.Label(
            self, text=f"Nombre predateurs: {len(self.champ.predateurs)}")
        self.label_predateurs.pack()

        self.label_proies = tk.Label(
            self, text=f"Nombre proies: {len(self.champ.proies)}")
        self.label_proies.pack()

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

        for coyote in self.champ.coyote:
            self.draw_object(coyote.position, 'red')

        for blaireau in self.champ.blaireau:
            self.draw_object(blaireau.position, "#FF8C00")

        for prairiechien in self.champ.prairiechien:
            self.draw_object(prairiechien.position, 'blue')

        for ecureuil in self.champ.ecureuil:
            self.draw_object(ecureuil.position, '#ADD8E6')

        for haie in self.champ.obstacles:
            self.draw_object(haie.position, 'green')

    def draw_object(self, position, color):
        x, y = position
        self.canvas.create_rectangle(x * self.cell_size, y * self.cell_size,
                                     (x + 1) * self.cell_size, (y + 1) * self.cell_size, fill=color)

    def update(self):

        if len(self.champ.predateurs) == 0 or len(self.champ.proies) == 0:
            print("Simulação terminada: ou os predadores ou as presas foram eliminados.")
            save_data_simulation(self.champ)
            return

        self.champ.process_turn()  # Processa um turno do jogo
        self.place_objects()  # Atualiza a visualização com os novos estados

        self.label_turn.config(text=f"Turno:{self.champ.turn}")
        self.label_predateurs.config(
            text=f"Nombre predateurs: {len(self.champ.predateurs)}")
        self.label_proies.config(
            text=f"Nombre proies: {len(self.champ.proies)}")

        # Aguarda 1000ms (1 segundo) e chama update novamente
        self.after(100, self.update)


# ======================= Add Predateurs et Proies ================================

def create_and_add_coyote(champ, number_of_predateurs):
    for _ in range(number_of_predateurs):
        x = random.randint(0, champ.width - 1)
        y = random.randint(0, champ.height - 1)

        new_predator = Coyote(position=[x, y])

        champ.add_predateurs(new_predator)
        champ.add_coyote(new_predator)


def create_and_add_blaireau(champ, number_of_predateurs):
    for _ in range(number_of_predateurs):
        x = random.randint(0, champ.width - 1)
        y = random.randint(0, champ.height - 1)

        new_predator = Blaireau(position=[x, y])

        champ.add_blaireau(new_predator)
        champ.add_predateurs(new_predator)


def create_and_add_prairiechien(champ, number_of_proies):
    for _ in range(number_of_proies):
        x = random.randint(0, champ.width - 1)
        y = random.randint(0, champ.height - 1)

        new_proie = PrairieChien(position=[x, y])

        champ.add_prairiechien(new_proie)
        champ.add_proies(new_proie)


def create_and_add_ecureuil(champ, number_of_proies):
    for _ in range(number_of_proies):
        x = random.randint(0, champ.width - 1)
        y = random.randint(0, champ.height - 1)

        new_proie = Ecureuil(position=[x, y])

        champ.add_ecureuil(new_proie)
        champ.add_proies(new_proie)


def create_and_add_haies(champ, number_of_haies):
    for _ in range(number_of_haies):
        x = random.randint(0, champ.width - 1)
        y = random.randint(0, champ.height - 1)

        new_haie = Proie(position=[x, y])

        champ.add_obstacle(new_haie)


champ = Champ(50, 50)
create_and_add_coyote(champ, 10)
create_and_add_blaireau(champ, 2)
create_and_add_ecureuil(champ, 100)
create_and_add_prairiechien(champ, 100)
create_and_add_haies(champ, 20)


# Iniciar a simulação com uma interface gráfica
game_board = GameBoard(champ)
game_board.mainloop()
