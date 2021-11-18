# external
import math
from random import randint, uniform

# custom
from config import def_genetic_conf as conf
from fitness_helper import fintess_func


class genetic_algo:

    def __init__(self, alphabet):
        self.generations = conf.config("generations")
        self.population_size = conf.config("population_size")
        self.tournament_size = conf.config("tournament_size")
        self.winner_probability = conf.config("winner_probability")
        self.crossover_probability = conf.config("crossover_probability")
        self.crossover_points_count = conf.config("crossover_points_count")
        self.mutation_probability = conf.config("mutation_probability")
        self.elitism_percent = conf.config("elitism_percent")
        self.selection_method = conf.config("selection_method")
        self.termination = conf.config("terminatio")

        self.bigram_weight = conf.config("weights")[0]
        self.trigram_weight = conf.config("weights")[1]

        self.verbose = conf.config("usage_params")["verbose"]

        self.elitism_count = int(
            self.elitism_percent
            * self.population_size)
        self.elitism_count = int(self.elitism_percent * self.population_size)
        self.crossover_count = self.population_size - self.elitism_count
        self.tournament_probabilities = [self.winner_probability]
        self.alphabet_order = list([ord(letter) for letter in alphabet])

        for i in range(1, self.tournament_size):
            probability = self.tournament_probabilities[i - 1] * (1.0 - self.winner_probability)
            self.tournament_probabilities.append(probability)

    def initialize(self):
        population = []

        for _ in range(self.population_size):
            key = ''

            while len(key) < 26:
                r = randint(0, len(self.alphabet_order) - 1)

                if self.alphabet_order[r] not in key:
                    key += self.alphabet_order[r]

            population.append(key)

        return population
