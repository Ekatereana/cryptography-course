class def_genetic_conf:
    __conf = {
        # algorithm specific parameters
        "generations": 100,
        "population_size": 100,
        "tournament_size": 10,
        "k_tournament": 2,
        "winner_probability": 0.75,
        "crossover_probability": 0.65,
        "crossover_points_count": 5,
        "mutation_probability": 0.2,
        "elitism_percent": 0.15,
        "selection_method": 'TS',
        "termination": 100,

        # bigram, trigram
        "weights": [0, 1.0],
        "usage_params": {"verbose": False},

    }
    __setters = ["generations", "population_size", "tournament_size",
                 "winner_probability", "crossover_probability", "crossover_points_count",
                 "mutation_probability", "elitism_percent", "selection_method", "termination", "weights",
                 "usage_params"]

    @staticmethod
    def config(name):
        return def_genetic_conf.__conf[name]

    @staticmethod
    def set(name, value):
        if name in def_genetic_conf.__setters:
            def_genetic_conf.__conf[name] = value
        else:
            raise NameError("Config not exist or cannot be modified")
