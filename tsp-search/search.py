import math
from heapq import heappush, heappop
from collections import deque
import numpy as np


def bfs(graph, start):
    return _generic_exhaustive_search(graph, start, deque.popleft)


def dfs(graph, start):
    return _generic_exhaustive_search(graph, start, deque.pop)


def _generic_exhaustive_search(graph, start, pop_fun):
    states = deque([(0, [start])])
    acceptable_states = []
    expanded_nodes = 0

    while states:
        current_cost, current_path = pop_fun(states)

        if _is_acceptable_path(graph, current_path):
            acceptable_states.append((current_cost, current_path))
        else:
            next_paths = _get_next_paths(current_path, graph)
            expanded_nodes += 1
            next_states = [(_get_next_cost(graph, next_path, current_cost), next_path) for next_path in next_paths]
            states.extend(next_states)

    acceptable_states.sort()
    optimal_state = acceptable_states[0] if acceptable_states else None

    if optimal_state is None:
        return None, None, expanded_nodes

    optimal_cost, optimal_path = optimal_state
    return optimal_path, optimal_cost, expanded_nodes


def _is_acceptable_path(graph, path):
    cities_count = graph.shape[0]
    path_length = len(path)
    return path_length == cities_count + 1


def _get_next_cost(graph, next_path, current_cost):
    return current_cost + _get_path_cost(graph, next_path[-2:])


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


def nearest_neighbor(graph, start):
    cities_count = graph.shape[0]
    state = (0, [start])
    expanded_nodes = 0

    for i in range(cities_count):
        next_paths = _get_next_paths(state[1], graph)
        next_states = [(_get_next_cost(graph, next_path, state[0]), next_path) for next_path in next_paths]
        expanded_nodes += 1

        if not next_states:
            return None, None, expanded_nodes

        best_next_state = sorted(next_states)[0]
        state = best_next_state

    cost, path = state
    return path, cost, expanded_nodes


def nearest_insertion(graph, start):
    cities_count = graph.shape[0]
    path = [start, start]

    for i in range(cities_count - 1):

        nearest_city = _find_city_nearest_to_path(graph, path)

        if not nearest_city:
            return None, None, None

        path = _get_path_with_inserted_city(graph, path, nearest_city)

        if path is None:
            return None, None, None

    cost = _get_path_cost(graph, path)
    return path, cost, None


def _find_city_nearest_to_path(graph, path):
    cities_count = graph.shape[0]
    not_visited_cities = [i for i in range(cities_count) if i not in path]
    cities_distances = []
    for target_city in not_visited_cities:
        minimum_distance = math.inf
        for start_city in path:
            distance = graph[start_city, target_city]
            if distance != -math.inf:
                minimum_distance = min(minimum_distance, distance)
        if minimum_distance != math.inf:
            city_distance = (minimum_distance, target_city)
            cities_distances.append(city_distance)
    if not cities_distances:
        return None
    nearest_city = sorted(cities_distances)[0][1]
    return nearest_city


def _get_path_with_inserted_city(graph, path, city):
    all_paths = [path[:pos] + [city] + path[pos:] for pos in range(1, len(path))]
    lengths_and_paths = [(_get_path_cost(graph, path), path) for path in all_paths]
    lengths_and_paths = [length_and_path for length_and_path in lengths_and_paths if length_and_path[0] != -math.inf]
    shortest_path = sorted(lengths_and_paths)[0][1] if lengths_and_paths else None
    return shortest_path


def _get_path_cost(graph, path):
    total_cost = 0
    for current_city, next_city in zip(path, path[1:]):
        cost = graph[current_city, next_city]
        total_cost += cost
    return total_cost


def a_star_min(graph, start):
    return _a_star(graph, start, _min_heuristic)


def a_star_avg(graph, start):
    return _a_star(graph, start, _avg_heuristic)


def _a_star(graph, start, heuristic):
    states = []
    expanded_nodes = 0

    initial_state = (0, 0, [start])     # cost, real cost, path
    heappush(states, initial_state)

    while states:
        cost, real_cost, path = heappop(states)

        if _is_acceptable_path(graph, path):
            return path, cost, expanded_nodes

        next_paths = _get_next_paths(path, graph)
        expanded_nodes += 1

        for next_path in next_paths:
            next_cost, next_real_cost = _get_next_a_star_cost(graph, next_path, real_cost, heuristic)
            next_state = (next_cost, next_real_cost, next_path)
            heappush(states, next_state)

    return None, None, expanded_nodes


def _get_next_a_star_cost(graph, next_path, current_cost, heuristic):
    c = current_cost + _get_path_cost(graph, next_path[-2:])
    h = heuristic(graph, next_path)
    return c + h, c


def _min_heuristic(graph, path):
    edges = _get_possible_edges_weights(graph, path)
    return np.min(edges) if edges.size else 0


def _avg_heuristic(graph, path):
    edges = _get_possible_edges_weights(graph, path)
    return np.mean(edges) if edges.size else 0


def _get_possible_edges_weights(graph, path):
    edges = np.delete(graph, path, 0)
    edges = np.delete(edges, path, 1)
    edges = edges[edges != np.NINF]
    return edges
