

import heapq
import math

CITIES = {
    "Delhi": (28.6139, 77.2090),
    "Jaipur": (26.9124, 75.7873),
    "Ahmedabad": (23.0225, 72.5714),
    "Mumbai": (19.0760, 72.8777),
    "Pune": (18.5204, 73.8567),
    "Surat": (21.1702, 72.8311),
    "Indore": (22.7196, 75.8577),
    "Bhopal": (23.2599, 77.4126),
    "Agra": (27.1767, 78.0081),
    "Udaipur": (24.5854, 73.7125),
}

ROAD_CONNECTIONS = [
    ("Delhi", "Jaipur"),
    ("Delhi", "Agra"),
    ("Jaipur", "Udaipur"),
    ("Jaipur", "Indore"),
    ("Agra", "Bhopal"),
    ("Bhopal", "Indore"),
    ("Indore", "Ahmedabad"),
    ("Ahmedabad", "Surat"),
    ("Surat", "Mumbai"),
    ("Mumbai", "Pune"),
    ("Udaipur", "Ahmedabad"),
]

EARTH_RADIUS_KM = 6371.0


def haversine(lat1, lon1, lat2, lon2):
  

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Differences in coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))

    # Distance in kilometers
    return EARTH_RADIUS_KM * c


def build_graph():
    """
    Step 3: Build a weighted adjacency-list graph.

    For every road connection, calculate Haversine distance between
    the two cities and store it as the edge weight in both directions
    (undirected graph).
    """
    graph = {city: [] for city in CITIES}

    for city_a, city_b in ROAD_CONNECTIONS:
        lat_a, lon_a = CITIES[city_a]
        lat_b, lon_b = CITIES[city_b]

        # Calculate edge weight using Haversine distance
        distance = haversine(lat_a, lon_a, lat_b, lon_b)

        # Add bidirectional edges (undirected road)
        graph[city_a].append((city_b, distance))
        graph[city_b].append((city_a, distance))

    return graph


def dijkstra(graph, start, destination):
    """
    Step 4: Find the shortest path using Dijkstra's algorithm.

    Uses a min-heap priority queue (heapq) to always expand
    the node with the smallest known distance first.

    Returns:
        path: list of city names from start to destination
        total_distance: sum of edge weights along the path (km)
    """
    # Distance from start to each city; infinity means unreachable
    distances = {city: float("inf") for city in graph}
    distances[start] = 0.0

    # Track the previous city on the shortest path to each city
    previous = {city: None for city in graph}

    # Priority queue: (distance, city_name)
    heap = [(0.0, start)]
    visited = set()

    while heap:
        current_dist, current = heapq.heappop(heap)

        # Skip if we've already finalized this node's shortest distance
        if current in visited:
            continue
        visited.add(current)

        # Stop early once we reach the destination
        if current == destination:
            break

        # Relax all neighbors of the current city
        for neighbor, edge_weight in graph[current]:
            if neighbor in visited:
                continue

            new_dist = current_dist + edge_weight

            # If we found a shorter path to the neighbor, update it
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous[neighbor] = current
                heapq.heappush(heap, (new_dist, neighbor))

    # Reconstruct path from destination back to start
    if distances[destination] == float("inf"):
        return [], float("inf")

    path = []
    node = destination
    while node is not None:
        path.append(node)
        node = previous[node]
    path.reverse()

    return path, distances[destination]


def shortest_route(source, destination):
    """
    Step 5: Build the graph, run Dijkstra, and return route and distance.

    Returns:
        route: list of city names on the shortest path
        distance: total distance in kilometers
    """
    graph = build_graph()
    route, distance = dijkstra(graph, source, destination)
    return route, distance


def display_route(route, distance):
    """Format and print the shortest route and total distance."""
    print("\nShortest Route\n")

    for i, city in enumerate(route):
        print(city)
        if i < len(route) - 1:
            print("↓")

    print(f"\nTotal Distance:\n{distance:.2f} km")


def run_menu():
    """
    Step 6: Interactive menu for selecting source and destination cities.
    """
    city_list = list(CITIES.keys())

    print("Available Cities:")
    for city in city_list:
        print(city)

    print()
    source = input("Enter Source: ").strip()
    destination = input("Enter Destination: ").strip()

    # Validate city names
    if source not in CITIES:
        print(f"Error: '{source}' is not a valid city.")
        return
    if destination not in CITIES:
        print(f"Error: '{destination}' is not a valid city.")
        return
    if source == destination:
        print("Error: Source and destination must be different cities.")
        return

    route, distance = shortest_route(source, destination)

    if not route:
        print(f"\nNo route found between {source} and {destination}.")
        return

    display_route(route, distance)


if __name__ == "__main__":
    run_menu()
