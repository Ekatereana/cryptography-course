# external
import math
import pandas
from random import randint, uniform

# custom
from lab_1_substitution.utils import calculate_n_grams, calc_fq, get_nth_letter


class GeneticAlgo:

    def __init__(self, filename, alphabet, conf, key_length):
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
        self.key_length = key_length

        self.alphabet = alphabet
        self.alphabet_order = list([ord(letter) for letter in alphabet])

        self.verbose = conf.config("usage_params")["verbose"]

        self.elitism_count = int(
            self.elitism_percent
            * self.population_size)
        self.elitism_count = int(self.elitism_percent * self.population_size)
        self.crossover_count = self.population_size - self.elitism_count
        self.tournament_probabilities = [self.winner_probability]

        for i in range(1, self.tournament_size):
            probability = self.tournament_probabilities[i - 1] * (1.0 - self.winner_probability)
            self.tournament_probabilities.append(probability)

        trigram_file = pandas.read_csv(filename)
        self.trigram_frequency = {}
        for i, row in trigram_file.iterrows():
            self.trigram_frequency[bytes(row['n-gram'], "utf-8")] = row['Frequency']

    # fitness functions helper

    # decrypt with combined key
    def decrypt_with_patch_key(self, text: bytes, keys: []):
        with_same_alphabet = [get_nth_letter(text, i, self.key_length) for i in range(0, self.key_length)]
        decrypted = []
        for t, key in zip(with_same_alphabet, keys):
            decrypted.append(self.decrypt_with_key(t, key))
        combined = self.combine_poly_decoded(decrypted, self.key_length, len(text))
        return combined

    # decrypt with one key
    def decrypt_with_key(self, text: bytes, key: bytes) -> bytes:
        decrypted = b''
        for byte in text:
            id = self.alphabet_order.index(byte)
            decrypted += bytes(key[id], 'ascii')
        return decrypted

    # merge decoded from several alphabets
    def combine_poly_decoded(self, decoded_texts: [], alpha_num: int, text_len: int) -> bytes:
        result = ''
        symb_id = 0
        pivot = 0
        while symb_id < text_len - 1:
            mode = symb_id % alpha_num
            result += chr(decoded_texts[mode][pivot])
            symb_id += 1
            if mode == 3:
                pivot += 1
        return bytes(result, "ascii")

    def fitness(self, text: bytes, chromosome: [], pivot: int):
        decrypted = self.decrypt_with_patch_key(text, chromosome)
        processed_grams = calculate_n_grams(decrypted, pivot)
        fq_decrypted = list([calc_fq(decrypted, n_gram) for n_gram in processed_grams])
        fq_source = list(
            [
                self.trigram_frequency.get(gram)
                if gram in self.trigram_frequency.keys()
                else 0
                for gram in processed_grams])

        smooth_if = lambda v: math.log2(v) if v != 0 else 0
        fitness = sum([smooth_if(fq[0]) * fq[1] for fq in zip(fq_source, fq_decrypted)])
        return fitness

    def initialize(self):
        population = []

        for _ in range(self.population_size):
            key = []

            while len(key) < self.key_length:
                chromosome = ''

                while len(chromosome) < 26:
                    r = randint(0, len(self.alphabet) - 1)

                    if self.alphabet[r] not in chromosome:
                        chromosome += self.alphabet[r]
                key.append(chromosome)

            population.append(key)

        return population

    def evaluate(self, text: bytes, population: []):
        fitness = []

        for key in population:
            key_fitness = self.calculate_fitness(text, key)
            fitness.append(key_fitness)

        return fitness

    def calculate_fitness(self, text: bytes, key: []):
        return self.fitness(text, key, 3)

    def rw_select(self, fitness):
        index = -1
        highest_probability = max(fitness)

        selected = False
        while not selected:
            index = randint(0, self.population_size - 1)
            probability = fitness[index]

            r = uniform(0, highest_probability)
            selected = (r < probability)

        return index

    def t_select(self, population, fitness):
        population_copy = population.copy()
        selected_keys = []

        iteration = 0

        while iteration < self.k_tournament:
            tournament_population = []
            iteration += 1

            for _ in range(self.tournament_size):
                if len(population_copy) == 0: population_copy = population.copy()

                r = randint(0, max(len(population_copy) - 1, 0))
                key = population[r]
                key_fitness = fitness[r]

                tournament_population.append((key, key_fitness))
                population_copy.pop(r)

            sorted_tournament_population = \
                sorted(tournament_population, key=lambda item: item[1], reverse=True)
            tournament_keys = list([item[0] for item in sorted_tournament_population])

            index = -1
            selected = False
            while not selected:
                index = randint(0, len(tournament_keys) - 1)
                probability = self.tournament_probabilities[index]

                r = uniform(0, self.winner_probability)
                selected = (r < probability)

            selected_keys.append(tournament_keys[index])

        return selected_keys[0], selected_keys[1]

    def cross(self, population, fitness):
        crossover = []

        while len(crossover) < self.crossover_count:

            if self.selection_method == 'RWS':
                parent_one_index = self.rw_select(fitness)
                parent_two_index = self.rw_select(fitness)

                parent_one = population[parent_one_index]
                parent_two = population[parent_two_index]
            else:
                parent_one, parent_two = self.t_select(population, fitness)

            # todo
            offspring_one = self.merge_complicated_keys(parent_one, parent_two)
            offspring_two = self.merge_complicated_keys(parent_two, parent_one)

            crossover += [offspring_one, offspring_two]

        crossover = self.mutate(crossover, self.crossover_count)

        return crossover

    def apply_elitism(self, population, fitness):
        population_fitness = []

        for i in range(self.population_size):
            key = population[i]
            value = fitness[i]

            population_fitness.append((key, value))

        population_fitness = sorted(population_fitness, key=lambda item: item[1])
        only_keys = list([key[0] for key in population_fitness])

        elitist = only_keys[-self.elitism_count:]

        return elitist

    def mutate(self, population, size):
        for i in range(size):
            r = uniform(0, 1)

            if r < self.mutation_probability:
                key = population[i]
                # todo
                mutated_key = self.mutate_combined_key(key)

                population[i] = mutated_key

        return population

    def merge_complicated_keys(self, one_set, two_set):
        merged = []
        for o, t in zip(one_set, two_set):
            merged.append(self.merge_keys(o, t))
        return merged

    def merge_keys(self, one, two):
        offspring = [None] * 26
        count = 0
        while count < self.crossover_points_count:
            r = randint(0, len(one) - 1)

            if offspring[r] == None:
                offspring[r] = one[r]
                count += 1

        for ch in two:
            if ch not in offspring:
                for i in range(len(offspring)):
                    if offspring[i] == None:
                        offspring[i] = ch
                        break

        return ''.join(offspring)

    def mutate_combined_key(self, keys: []) -> []:
        a = randint(0, len(keys) - 1)
        b = randint(0, len(keys) - 1)
        temp = keys[a]
        keys[a] = keys[b]
        keys[b] = temp
        return keys

    def mutate_key(self, key):
        a = randint(0, len(key) - 1)
        b = randint(0, len(key) - 1)

        key = list(key)
        temp = key[a]
        key[a] = key[b]
        key[b] = temp

        return ''.join(key)

    def solve(self, text: bytes):
        print("initialization")

        population = self.initialize()
        highest_fitness = 0
        stuck_counter = 0
        for inst in population:
            print(inst)
        for iter in range(self.generations + 1):
            print(f"--{iter} iteration --")
            fitness = self.evaluate(text, population)
            elitist_population = self.apply_elitism(population, fitness)
            crossover_population = self.cross(population, fitness)

            population = elitist_population + crossover_population

            # Terminate if highest_fitness not increasing
            if highest_fitness == max(fitness):
                stuck_counter += 1
            else:
                stuck_counter = 0

            if stuck_counter >= self.termination:
                break

            highest_fitness = max(fitness)
            average_fitness = sum(fitness) / self.population_size

            index = fitness.index(highest_fitness)
            key = population[index]
            decrypted_text = self.decrypt_with_patch_key(text, key)

            if self.verbose:
                print('[Generation ' + str(iter) + ']', )
                print('Average Fitness:', average_fitness)
                print('Max Fitness:', highest_fitness)
                print('Key:', key)
                print('Decrypted Text:')
                print(decrypted_text)

        return decrypted_text
