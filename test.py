from models import City
from graphs import generate_graph, check_connected
from ant_search import ant_search
import time


def display_cities(cities):
    print('* CITIES')
    for nr, city in enumerate(cities):
        print(f'{nr}: {city}')
    print()


def display_test_result(connected, result=None, duration=None):
    path, cost, expanded_nodes = result
    print(f'- Connected: {connected}')
    print(f'- Solved: {path is not None}')
    if path is not None:
        print(f'- Path: {path}')
    if cost is not None:
        print(f'- Cost: {round(cost, 5)}')
    if expanded_nodes is not None:
        print(f'- Expanded nodes: {expanded_nodes}')
    if duration is not None:
        print(f'- Time: {round(duration, 5)}s')
    print()


def test(cities, start_city, connections_drop, symmetric, seed=None):
    start_time = time.time()

    # Represent the created map as a weighted, directed graph
    graph = generate_graph(cities, connections_drop=connections_drop, symmetric=symmetric, seed=seed)

    # Make sure whether generated graph is connected
    # This is necessary condition, but not sufficient
    # It may be still impossible to visit every city only once
    connected = check_connected(graph)
    if not connected:
        display_test_result(connected=False)
        return

    # Search graph
    result = ant_search(graph, start_city)

    end_time = time.time()
    display_test_result(connected=True, result=result, duration=end_time-start_time)


if __name__ == '__main__':
    seed = 222467
    cities_count = 9
    start_city = 0

    # Create a set of cities
    cities = City.generate(count=cities_count, x_range=(-100, 100), y_range=(-100, 100), z_range=(0, 50), seed=seed)
    display_cities(cities)

    for connections_drop in [0.0, 0.2]:
        for symmetric in [True, False]:
            print(f"{'-'*15} connections_drop: {connections_drop}; symmetric: {symmetric} {'-'*15}\n")
            test(cities, start_city, connections_drop, symmetric, seed=seed)
