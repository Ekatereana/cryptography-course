mono = {
    # algorithm specific parameters
    "generations": 500,
    "population_size": 500,
    "tournament_size": 10,
    "k_tournament": 2,
    "winner_probability": 0.75,
    "crossover_probability": 0.75,
    "crossover_points_count": 3,
    "mutation_probability": 0.05,
    "elitism_percent": 0.15,
    "selection_method": 'TS',
    "termination": 100,
    "mode": "mono",

    "usage_params": {"verbose": True},
}
poly = {
    "generations": 500,
    "population_size": 500,
    "tournament_size": 10,
    "k_tournament": 2,
    "winner_probability": 0.65,
    "crossover_probability": 0.65,
    "crossover_points_count": 4,
    "mutation_probability": 0.15,
    "elitism_percent": 0.15,
    "selection_method": 'TS',
    "termination": 100,
    "mode": "poly",
    "usage_params": {"verbose": True},
}


class GeneticConf:
    def __init__(self, is_poly: bool = False):
        self.__conf = poly if is_poly else mono

    __setters = ["generations", "population_size", "tournament_size",
                 "winner_probability", "crossover_probability", "crossover_points_count",
                 "mutation_probability", "elitism_percent", "selection_method", "termination",
                 "usage_params"]

    def config(self, name):
        return self.__conf[name]

    def set(self, name, value):
        if name in self.__setters:
            self.__conf[name] = value
        else:
            raise NameError("Config not exist or cannot be modified")
