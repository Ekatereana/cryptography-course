from config import def_genetic_conf as conf
import math
from random import randint, uniform


class genetic_algo:

    def __init__(self):
        self.elitism_count = int(
            conf.config("elitism_percent")
            * conf.config("population_size"))
        self.elitism_count = int(conf.config("elitism_percent") * conf.config("population_size"))
        self.crossover_count = conf.config("population_size") - self.elitism_count
        self.tournament_probabilities = [conf.config("winner_probability")]

        for i in range(1, conf.config("tournament_size")):
            probability = self.tournament_probabilities[i - 1] * (1.0 - conf.config("winner_probability"))
            self.tournament_probabilities.append(probability)
