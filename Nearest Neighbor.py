import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Location:
    def __init__(self, id, latitude, longitude, demand):
        self.id = id
        self.latitude = latitude
        self.longitude = longitude
        self.demand = demand
        self.visited = False

class Vehicle:
    def __init__(self, type, capacity, cost_per_km):
        self.type = type
        self.capacity = capacity
        self.cost_per_km = cost_per_km
        self.route = []
        self.total_distance = 0
        self.total_demand = 0

class Depot(Location):
    def __init__(self, latitude, longitude):
        super().__init__(id=0, latitude=latitude, longitude=longitude, demand=0)

class DeliveryProblem:
    def __init__(self, depot, customers, vehicles):
        self.depot = depot
        self.customers = customers
        self.vehicles = vehicles

    def euclidean_distance(self, loc1, loc2):
        return 100 * math.sqrt((loc2.longitude - loc1.longitude)**2 + (loc2.latitude - loc1.latitude)**2)

    def nearest_neighbor(self, vehicle, unvisited_customers):
        current_location = self.depot
        while vehicle.total_demand < vehicle.capacity and unvisited_customers:
            min_distance = float('inf')
            nearest_customer = None
            for customer in unvisited_customers:
                if vehicle.total_demand + customer.demand <= vehicle.capacity:
                    distance = self.euclidean_distance(current_location, customer)
                    if distance < min_distance:
                        min_distance = distance
                        nearest_customer = customer
            if nearest_customer is None:
                break  
            vehicle.route.append(nearest_customer)
            vehicle.total_distance += min_distance
            vehicle.total_demand += nearest_customer.demand
            nearest_customer.visited = True
            current_location = nearest_customer
            unvisited_customers.remove(nearest_customer)

         # Returning to depot after visiting customers
        if vehicle.route:
            vehicle.total_distance += self.euclidean_distance(current_location, self.depot)
    
    def optimize_routes(self):
        unvisited_customers = set(self.customers)  # Keep track of unvisited customers
        while unvisited_customers:
            for vehicle in self.vehicles:
                self.nearest_neighbor(vehicle, unvisited_customers)
                if not unvisited_customers:
                    break

    def print_routes(self):
        total_distance = sum(vehicle.total_distance for vehicle in self.vehicles)
        total_cost = sum(vehicle.total_distance * vehicle.cost_per_km for vehicle in self.vehicles)
        print(f"Total Distance = {total_distance:.2f} km")
        print(f"Total Cost = RM {total_cost:.2f}")

        for i, vehicle in enumerate(self.vehicles, 1):
            print(f"Vehicle {i} (Type {vehicle.type}):")
            print(f"Round Trip Distance: {vehicle.total_distance:.3f} km, Cost: RM {vehicle.total_distance * vehicle.cost_per_km:.2f}, Demand: {vehicle.total_demand}")
            print("Depot -> ", end="")
            for j, customer in enumerate(vehicle.route):
                if j > 0:  # If not the first customer, calculate distance from the previous customer
                    distance = self.euclidean_distance(vehicle.route[j - 1], customer)
                else:  # For the first customer, calculate distance from the depot
                    distance = self.euclidean_distance(self.depot, customer)
                print(f"C{customer.id} ({distance:.3f} km) -> ", end="")
            # After the last customer, print the distance back to the depot
            if vehicle.route:
                distance_back_to_depot = self.euclidean_distance(vehicle.route[-1], self.depot)
                print(f"Depot ({distance_back_to_depot:.3f} km)")

def plot_depot(depot):
    plt.plot(depot.longitude, depot.latitude, 'ks', markersize=10, label='Depot')
    plt.text(depot.longitude, depot.latitude, ' Depot', verticalalignment='bottom', horizontalalignment='right')

def plot_customers(customers):
    for customer in customers:
        plt.plot(customer.longitude, customer.latitude, 'bo', markersize=5)
        plt.text(customer.longitude, customer.latitude, f' C{customer.id}', verticalalignment='bottom', horizontalalignment='right')

def plot_vehicle_route(vehicle, depot, route_color, route_label):
    route_lngs, route_lats = [depot.longitude], [depot.latitude]  
    for customer in vehicle.route:
        route_lngs.append(customer.longitude)
        route_lats.append(customer.latitude)
    route_lngs.append(depot.longitude)  
    route_lats.append(depot.latitude)
    plt.plot(route_lngs, route_lats, route_color, label=route_label)

def plot_routes(vehicles, depot, customers, optimized=False):
    plot_depot(depot)
    plot_customers(customers)

    # Plot the routes for each vehicle
    for vehicle in vehicles:
        if optimized:
            plot_vehicle_route(vehicle, depot, '-o', f'Vehicle {vehicle.type} Optimized')
        else:
            plot_vehicle_route(vehicle, depot, 'r--o', f'Vehicle {vehicle.type} Initial')

    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Delivery Routes Before and After Optimization')
    plt.legend()
    plt.show()

def main():
   # Read customer data from an Excel file
    customer_data = pd.read_excel(r"C:\Users\User\Desktop\customerData.xlsx")

    # Define depot
    depot = Depot(latitude=4.4184, longitude=114.0932)

    # Create customers from the Excel data
    customers = []
    for index, row in customer_data.iterrows():
        customer_id = int(row['CustomerID'])
        customers.append(Location(id=customer_id, latitude=row['Latitude'], longitude=row['Longitude'], demand=row['Demand']))
    
    # Define the number of vehicles of each type
    num_type_a_vehicles = 2
    num_type_b_vehicles = 1

    # Create vehicles based on the specified numbers
    vehicles = []
    for _ in range(num_type_a_vehicles):
        vehicles.append(Vehicle(type="A", capacity=25, cost_per_km=1.2))
    for _ in range(num_type_b_vehicles):
        vehicles.append(Vehicle(type="B", capacity=30, cost_per_km=1.5))

    # Create delivery problem instance
    problem = DeliveryProblem(depot, customers, vehicles)

    # First call - before optimization
    plot_routes(vehicles, depot, customers)

    # Solve and print routes
    problem.optimize_routes()
    problem.print_routes()

    # Second call - after optimization
    plot_routes(vehicles, depot, customers, optimized=True)

if __name__ == "__main__":
    main()