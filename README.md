# Capacitated-Vehicle-Routing-Problem-CVRP-
Optimizing vehicle routing for efficient delivery of goods to various customer locations while minimizing costs. This project implements algorithms to solve the Capacitated Vehicle Routing Problem (CVRP) using Python and frameworks like Google OR-Tools and the nearest neighbor heuristic, with the latter being used for comparison purposes. 

## Features
- Implementation of OR-Tools framework for solving CVRP
- Nearest neighbor heuristic algorithm for comparison
- Visualization of vehicle routes on a graph using Matplotlib

## Dataset
The dataset can be found in the `customerData` file as a CSV file. Here are the details:
- 10 customers

## Prerequisites
Before running the solver, ensure you have Python installed on your system. 
- Python (version version 3.8+ on Linux, macOS or Windows)
You will also need the following packages:
- Libraries: pandas, numpy, matplotlib, ortools
You can install them using pip:
-pip install ortools matplotlib

## Usage
### Preparing Your Data
Modify the `create_data_model` function in the script to reflect your specific problem instance. This includes: 
Define the number of vehicles of each type
    num_type_a_vehicles = 2
    num_type_b_vehicles = 1
Define capacities and costs
vehicles = []
    for _ in range(num_type_a_vehicles):
        vehicles.append(Vehicle(type="Type A", capacity=25, cost_per_km=1.2))
    for _ in range(num_type_b_vehicles):
        vehicles.append(Vehicle(type="Type B", capacity=30, cost_per_km=1.5))
defining the locations and demands of your customers
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

## Result Diagrams
![Vehicle Routing Before Optimization](images/before_optimization.png)
![Vehicle Routing After Optimization](images/after_optimization.png)
