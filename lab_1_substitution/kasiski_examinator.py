from collections import Counter, OrderedDict


def calc_kasiski_factor(grams_pos: (bytes, int)):
    repeated = found_repeated_grams(grams_pos)
    dist = [count_all_distances(r[1]) for r in repeated]
    # only possible key sizes
    sizes = set([item for on_val in dist for item in on_val])
    sizes_factors = [find_all_factors(size) for size in sizes]
    factors = list([factor for on_factor in sizes_factors for factor in on_factor])

    # create top of the uses sizes
    num_factor = OrderedDict(Counter(factors))

    # return the factor that has the max frequency
    return list(num_factor.keys())[0]


def found_repeated_grams(grams_pos: (bytes, int)) -> {}:
    # trigram: (counter, pos [])
    repeated = {}

    for inst, pos in grams_pos:
        if inst in repeated.keys():
            repeated[inst][1].append(pos)
            repeated[inst] = (repeated[inst][0] + 1, repeated[inst][1])
        else:
            repeated[inst] = (1, [pos])
    # only that repeats
    repeated = dict(filter(lambda v: v[1][0] > 1, repeated.items()))
    return repeated.values()


def count_all_distances(positions: []) -> []:
    distances = []
    for i in range(0, len(positions) - 1):
        for j in range(i + 1, len(positions)):
            dist = positions[j] - positions[i]
            if dist not in distances:
                distances.append(dist)
    return distances


def find_all_factors(val: int) -> [int]:
    factors = []
    # 2 -- too little for the key size
    for i in range(3, val + 1):
        if val % i == 0:
            factors.append(i)
            factors.append(val/i)
    return factors
