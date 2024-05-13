from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import math
import matplotlib.pyplot as plt
from itertools import cycle

class Vehicle:
    def __init__(self, type, capacity, cost_per_km):
        self.type = type
        self.capacity = capacity
        self.cost_per_km = cost_per_km

def create_data_model():
    """Stores the data for the problem."""
    # Define the number of vehicles of each type
    num_type_a_vehicles = 2
    num_type_b_vehicles = 1

    # Create vehicles based on the specified numbers
    vehicles = []
    for _ in range(num_type_a_vehicles):
        vehicles.append(Vehicle(type="Type A", capacity=25, cost_per_km=1.2))
    for _ in range(num_type_b_vehicles):
        vehicles.append(Vehicle(type="Type B", capacity=30, cost_per_km=1.5))
    data = {}
    data["locations"] = [
        (4.4184, 114.0932), # Depot
        (4.3555, 113.9777), # Customers
        (4.3976, 114.0049),
        (4.3163, 114.0764),
        (4.3184, 113.9932),
        (4.4024, 113.9896),
        (4.4142, 114.0127),
        (4.4804, 114.0734),
        (4.3818, 114.2034),
        (4.4935, 114.1828),
        (4.4932, 114.1322),
    ]
    data["demands"] = [0, 5, 8, 3, 6, 5, 8, 3, 6, 5, 8] * len(vehicles)
    data["vehicle_capacities"] = [vehicle.capacity for vehicle in vehicles]
    data["num_vehicles"] = len(vehicles)
    data["vehicle_types"] = [vehicle.type for vehicle in vehicles]
    data["vehicle_costs"] = [vehicle.cost_per_km for vehicle in vehicles]
    data["depot"] = 0
    data["distance_matrix"] = compute_euclidean_distance_matrix(data["locations"])
    return data

def compute_euclidean_distance_matrix(locations):
    """Creates callback to return distance between points."""
    distance_matrix = [[0 for _ in locations] for _ in locations]
    for from_counter, from_node in enumerate(locations):
        for to_counter, to_node in enumerate(locations):
            if from_counter == to_counter:
                distance_matrix[from_counter][to_counter] = 0
            else:
                # Calculate Euclidean distance and scale it up
                distance = math.hypot(
                    (from_node[0] - to_node[0]), 
                    (from_node[1] - to_node[1])
                )
                scaled_distance = distance * 100000
                distance_matrix[from_counter][to_counter] = int(scaled_distance)
    return distance_matrix

def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    total_distance = 0
    total_cost = 0
    vehicle_routes = {}
    # Calculate the total distance and total cost
    for vehicle_id in range(data["num_vehicles"]):
        vehicle_type = data["vehicle_types"][vehicle_id]
        cost_per_km = data["vehicle_costs"][vehicle_id]
        index = routing.Start(vehicle_id)
        route_distance = 0
        route_demand = 0
        route = []
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_demand += data["demands"][node_index]
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
            route.append(node_index)
        route_cost = (route_distance / 1000) * cost_per_km
        total_distance += route_distance
        total_cost += route_cost
        vehicle_routes[vehicle_id] = {"type": vehicle_type, "distance": route_distance, "cost": route_cost, "demand": route_demand - data["demands"][data["depot"]], "route": route}

    # Print the total distance and total cost
    print(f"Total Distance = {total_distance/1000:.3f} km")
    print(f"Total Cost = RM {total_cost:.2f}")

    # Print the details for each vehicle
    for vehicle_id, route_info in vehicle_routes.items():
        print(f"Vehicle {vehicle_id + 1} ({route_info['type']}):")
        print(f"Round Trip Distance: {route_info['distance']/1000:.3f} km, Cost: RM {route_info['cost']:.2f}, Demand: {route_info['demand']}")
        print("Depot -> ", end="")
        for node_index in route_info["route"]:
            if node_index != 0:
                distance = data["distance_matrix"][route_info["route"][route_info["route"].index(node_index) - 1]][node_index] / 1000
                print(f"C{node_index} ({distance:.3f} km) -> ", end="")
        distance_back_to_depot = data["distance_matrix"][route_info["route"][-1]][0] / 1000
        print(f"Depot ({distance_back_to_depot:.3f} km)")

def plot_routes(data, manager, routing, solution):
    """Plots the routes on a graph."""
    color_cycle = cycle(plt.rcParams['axes.prop_cycle'].by_key()['color'])
    depot_location = data["locations"][data["depot"]]
    plt.scatter(depot_location[1], depot_location[0], c='black', marker='s', label='Depot')

    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        route_x = [] 
        route_y = [] 
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            location = data["locations"][node_index]
            route_x.append(location[1])  
            route_y.append(location[0])  
            plt.text(location[1], location[0], f'C{node_index}')
            index = solution.Value(routing.NextVar(index))
        route_x.append(depot_location[1])
        route_y.append(depot_location[0])
        vehicle_color = next(color_cycle)
        plt.plot(route_x, route_y, '-o', color=vehicle_color, label=f'Vehicle {data["vehicle_types"][vehicle_id]}')

    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Vehicle Routing Problem')
    plt.legend()
    plt.show()

def main():
    """Solve the CVRP problem."""
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
    )

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Capacity constraint.
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data["demands"][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data["vehicle_capacities"],  # vehicle maximum capacities
        True,  # start cumul to zero
        "Capacity",
    )

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )
    search_parameters.time_limit.FromSeconds(1)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution)
        plot_routes(data, manager, routing, solution)

if __name__ == "__main__":
    main()
