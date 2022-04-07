import numpy as np
import random
from functools import total_ordering


def ant_search(graph, start, n_ants=50, q=100, rho=0.99, alpha=1, beta=5):
    cities_count = graph.shape[0]

    ants = _init_ants(cities_count, n_ants)
    phs = _init_pheromones(graph)

    for i in range(cities_count):
        _turn(ants, phs, graph, q, rho, alpha, beta)

    best_ant = _find_best_ant(ants, start)
    return best_ant.path, best_ant.cost, None


@total_ordering
class _Ant:

    def __init__(self, city):
        self.path = [city]
        self.cost = 0

    def __repr__(self):
        return f'Ant(cost={self.cost}; path={self.path})'

    def __lt__(self, other):
        return self.cost < other.cost

    @property
    def city(self):
        return self.path[-1]

    @property
    def start(self):
        return self.path[0]

    def go(self, next_city, graph):
        self.cost += graph[self.city, next_city]
        self.path.append(next_city)


def _init_ants(cities_count, n_ants):
    return [_Ant(city) for city in range(cities_count) for _ in range(n_ants)]


def _init_pheromones(graph):
    phs = graph.copy()
    phs[phs > np.NINF] = 0
    return phs


def _turn(ants, phs, graph, q, rho, alpha, beta):
    _update_ants(ants, phs, graph, alpha, beta)
    _update_pheromones(ants, phs, q, rho)


def _update_ants(ants, phs, graph, alpha, beta):
    ants_to_kill = []
    for ant in ants:
        live = _update_ant(ant, graph, phs, alpha, beta)
        if not live:
            ants_to_kill.append(ant)

    for ant in ants_to_kill:
        ants.remove(ant)


def _update_ant(ant, graph, phs, alpha, beta):
    next_paths, probabilities = _get_next_paths_and_probabilities(ant.path, graph, phs, alpha, beta)
    if len(next_paths) == 0:
        return False
    selected_path = random.choices(next_paths, weights=probabilities, k=1)[0]
    ant.go(selected_path[-1], graph)
    return True


def _get_next_paths_and_probabilities(path, graph, phs, alpha, beta):
    next_paths = _get_next_paths(path, graph)
    numerators = [_get_probability_numerator(path, graph, phs, alpha, beta) for path in next_paths]
    denominator = sum(numerators) if numerators else 0
    probabilities = [num / denominator for num in numerators] if denominator != 0 else []
    return next_paths, probabilities


def _get_probability_numerator(path, graph, phs, alpha, beta):
    if len(path) == 2:
        return 1
    current_city, next_city = path[-2:]
    visibility = 1 / graph[current_city, next_city]
    numerator = phs[current_city, next_city]**alpha * visibility**beta
    return numerator


def _update_pheromones(ants, phs, q, rho):
    np.multiply(phs, rho, out=phs)
    for ant in ants:
        prev_city, next_city = ant.path[-2:]
        delta_phs = q / ant.cost
        phs[prev_city, next_city] += delta_phs


def _find_best_ant(ants, start):
    start_ants = [ant for ant in ants if ant.start == start]
    best_ants = sorted(start_ants)
    return best_ants[0]


def _get_next_paths(current_path, graph):
    cities_count = graph.shape[1]
    current_path_length = len(current_path)

    if current_path_length == cities_count:
        return _get_next_paths_final_step(current_path, graph)
    else:
        return _get_next_paths_standard_step(current_path, graph)


def _get_next_paths_standard_step(current_path, graph):
    next_paths = []
    cities_count = graph.shape[1]
    current_city = current_path[-1]

    for next_city in range(cities_count):
        weight = graph[current_city][next_city]
        if next_city in current_path or weight == np.NINF:
            continue
        next_path = current_path + [next_city]
        next_paths.append(next_path)
    return next_paths


def _get_next_paths_final_step(current_path, graph):
    first_city = current_path[0]
    current_city = current_path[-1]

    cost = graph[current_city][first_city]

    if cost == np.NINF:
        return []

    new_path = current_path + [first_city]
    return [new_path]