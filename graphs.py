import numpy as np
import random
from models import City


def generate_graph(cities, connections_drop=0, symmetric=True, seed=None):
    if seed:
        random.seed(seed)
    graph_no_weights = _create_graph_without_weights(cities, connections_drop, symmetric)
    weighted_graph = _add_weights_to_graph(graph_no_weights, cities, symmetric)
    return weighted_graph


def _create_graph_without_weights(cities, connections_drop=0.0, symmetric=True):
    size = len(cities)
    graph_no_weights = np.ones((size, size))
    np.fill_diagonal(graph_no_weights, 0)

    dropped_percent = _get_dropped_percent(graph_no_weights)
    while dropped_percent < connections_drop:
        _remove_connection(graph_no_weights, symmetric)
        dropped_percent = _get_dropped_percent(graph_no_weights)

    return graph_no_weights


def _get_dropped_percent(graph):
    return 1 - (graph.sum() / (graph.size - graph.shape[0]))


def _remove_connection(graph, symmetric):
    connection = _random_connection(graph)
    graph[connection] = False
    if symmetric:
        symmetric_connection = (connection[1], connection[0])
        graph[symmetric_connection] = False


def _random_connection(graph):
    cons_sum = graph.sum()
    con_to_drop = random.randint(0, cons_sum)
    cumsum = np.cumsum(graph)
    index = np.argmax(cumsum == con_to_drop)
    y = index // graph.shape[1]
    x = index % graph.shape[1]
    return y, x


def _add_weights_to_graph(graph_no_weights, cities, symmetric):
    graph = np.zeros(graph_no_weights.shape, dtype=np.double)
    graph.fill(np.NINF)
    for y in range(graph_no_weights.shape[0]):
        for x in range(graph_no_weights.shape[1]):
            if not graph_no_weights[y, x]:
                continue
            calc_weight = City.distance_symmetric if symmetric else City.distance_asymmetric
            graph[y, x] = calc_weight(cities[y], cities[x])
    return graph


def check_connected(graph):
    nodes_count = graph.shape[0]
    for start_node in range(nodes_count):
        is_connected = _check_connected_from_start(graph, start_node)
        if not is_connected:
            return False
    return True


def _check_connected_from_start(graph, start):
    nodes_count = graph.shape[0]
    visited_nodes = np.zeros((nodes_count,), dtype=np.bool_)
    nodes = [start]

    while nodes:
        node = nodes.pop(0)
        is_connected = graph[node, :] > np.NINF
        is_connected_and_unvisited = is_connected & ~visited_nodes
        nodes_to_visit = np.argwhere(is_connected_and_unvisited).flatten().tolist()
        nodes = nodes_to_visit + nodes
        visited_nodes[node] = True

    return visited_nodes.all()
