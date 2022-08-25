import random

from snake import *
import math

LEARN_RATE = 0.6
PRZEWIDYWALNOSC = 0.1


def rand_max(zbior: list):
    ind_max = []
    for i in range(len(zbior)):
        if zbior[i] == max(zbior):
            ind_max.append(i)
    return random.choice(ind_max)


def vector_len(Point1, Point2):
    max_len = math.sqrt(math.pow(900, 2) + math.pow(600, 2))
    return math.sqrt(math.pow(Point2[0] - Point1[0], 2) + math.pow(Point2[1] - Point1[1], 2)) / max_len


class Agent:

    def __init__(self):
        # dlugosc do jedzenia i 4 dlugosci do scian
        self.weights =  [0, 0, 0, 0, 0]
        self.actions = [0, 0, 0, 0]
        self.values = [0, 0, 0, 0, 0]
        self.x = 0
        self.y = 0

    def func(self, x_y_jedz, x_y_player):
        lst = []
        lst.append(vector_len(x_y_jedz, x_y_player))  # dist to eat
        lst.append(vector_len(x_y_player, [self.x, 0]))  # up wall
        lst.append(vector_len(x_y_player, [self.x, HEIGHT]))  # down wall
        lst.append(vector_len(x_y_player, [0, self.y]))  # left wall
        lst.append(vector_len(x_y_player, [WIDTH, self.y]))  # right wall
        return lst



    def predict(self, x_y_jedz,ilosc_gier):
        if random.randint(0,10+ilosc_gier//30) == 2:return random.randint(0,3)
        func_lst = []
        for i in range(len(self.actions)):
            value = 0
            if i == 0: func_lst = self.func(x_y_jedz, [self.x - width, self.y])
            if i == 1: func_lst = self.func(x_y_jedz, [self.x, self.y - height])
            if i == 2: func_lst = self.func(x_y_jedz, [self.x + width, self.y])
            if i == 3: func_lst = self.func(x_y_jedz, [self.x, self.y + height])
            for j in range(len(self.weights)):
                value += self.weights[j] * func_lst[j]

            self.actions[i] = value
        self.values = func_lst
        return rand_max(self.actions)

    def learn(self, did_lose, did_collide, prev_predict, x_y_jedz,ilosc_gier):
        nagroda = 0 + did_lose + did_collide
        new_predict = self.predict(x_y_jedz,ilosc_gier)
        blad = (nagroda + PRZEWIDYWALNOSC * self.actions[new_predict]) - self.actions[prev_predict]
        for i in range(len(self.weights)):
            self.weights[i] += LEARN_RATE * blad * self.values[i]
