# external
import math
from random import randint, uniform
import re

# custom
from config import def_genetic_conf as conf
from fitness import fintess_func


class genetic_algo:

    def __init__(self, filename, alphabet):
        self.generations = conf.config("generations")
        self.population_size = conf.config("population_size")
        self.k_tournament = conf.config("k_tournament")
        self.tournament_size = conf.config("tournament_size")
        self.winner_probability = conf.config("winner_probability")
        self.crossover_probability = conf.config("crossover_probability")
        self.crossover_points_count = conf.config("crossover_points_count")
        self.mutation_probability = conf.config("mutation_probability")
        self.elitism_percent = conf.config("elitism_percent")
        self.selection_method = conf.config("selection_method")
        self.termination = conf.config("termination")

        self.bigram_weight = conf.config("weights")[0]
        self.trigram_weight = conf.config("weights")[1]

        self.alphabet = alphabet
        self.alphabet_order = list([ord(letter) for letter in alphabet])

        self.verbose = conf.config("usage_params")["verbose"]

        self.elitism_count = int(
            self.elitism_percent
            * self.population_size)
        self.elitism_count = int(self.elitism_percent * self.population_size)
        self.crossover_count = self.population_size - self.elitism_count
        self.tournament_probabilities = [self.winner_probability]

        self.fitness = fintess_func(self.alphabet_order)

        for i in range(1, self.tournament_size):
            probability = self.tournament_probabilities[i - 1] * (1.0 - self.winner_probability)
            self.tournament_probabilities.append(probability)

        #     prepare trained text
        pattern = r'[0-9/\:\[\]\.\"\?\;\-\,]'
        with open(filename, 'r', encoding="utf-8") as t_f:
            self.trained = bytes(re.sub(pattern, '', t_f.read().upper()), "utf-8")

    def initialize(self):
        population = []

        for _ in range(self.population_size):
            key = ''

            while len(key) < 26:
                r = randint(0, len(self.alphabet) - 1)

                if self.alphabet[r] not in key:
                    key += self.alphabet[r]

            population.append(key)

        return population

    def evaluate(self, text: bytes, population: []):
        fitness = []

        for key in population:
            key_fitness = self.calculate_fitness(text, key)
            fitness.append(key_fitness)

        return fitness

    def calculate_fitness(self, text: bytes, key: []):
        bigram_fitness = self.fitness.aplay(text, self.trained, key, 2)
        trigram_fitness = self.fitness.aplay(text, self.trained, key, 3)
        fitness = (bigram_fitness * self.bigram_weight) + (trigram_fitness * self.trigram_weight)
        return fitness

    def select(self, population, fitness):
        selected_keys = []

        iteration = 0

        while iteration < self.k_tournament:
            tournament_population = {}
            iteration += 1

            for _ in range(self.tournament_size):
                r = randint(0, len(population) - 1)
                key = population[r]
                key_fitness = fitness[r]

                tournament_population[key] = key_fitness
                population.pop(r)

            sorted_tournament_population = \
                {k: v for k, v in sorted(tournament_population.items(), key=lambda item: item[1], reverse=True)}
            tournament_keys = list(sorted_tournament_population.keys())

            index = -1
            selected = False
            while not selected:
                index = randint(0, self.tournament_size - 1)
                probability = self.tournament_probabilities[index]

                r = uniform(0, self.winner_probability)
                selected = (r < probability)

            selected_keys.append(tournament_keys[index])

        print(selected_keys)

        return selected_keys[0], selected_keys[1]

    def rw_select(self, fitness):
        index = -1
        highest = max(fitness)

        selected = False
        while not selected:
            index = randint(0, self.population_size - 1)
            probability = fitness[index]

            r = uniform(0, highest)
            selected = (r < probability)

        return index
