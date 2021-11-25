class def_genetic_conf:
    __conf = {
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

        "usage_params": {"verbose": True},

    }
    __setters = ["generations", "population_size", "tournament_size",
                 "winner_probability", "crossover_probability", "crossover_points_count",
                 "mutation_probability", "elitism_percent", "selection_method", "termination",
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
