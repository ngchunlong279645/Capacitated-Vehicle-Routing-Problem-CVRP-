# Capacitated Vehicle Routing Problem (CVRP)

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

### System Requirements

- Python (version version 3.8+ on Linux, macOS, or Windows)

### Required Packages

You will also need the following packages:

- pandas
- numpy
- matplotlib
- ortools

You can install them using pip:

```bash
pip install ortools matplotlib pandas numpy
```

## Usage

### Preparing Your Data

Modify the `create_data_model` function in the script to reflect your specific problem instance. This includes:

1. Define the number of vehicles of each type:

    ```python
    num_type_a_vehicles = 2
    num_type_b_vehicles = 1
    ```

2. Define capacities and costs:

    ```python
    vehicles = []
    for _ in range(num_type_a_vehicles):
        vehicles.append(Vehicle(type="Type A", capacity=25, cost_per_km=1.2))
    for _ in range(num_type_b_vehicles):
        vehicles.append(Vehicle(type="Type B", capacity=30, cost_per_km=1.5))
    ```

3. Define the locations and demands of your customers:

    ```python
    data["locations"] = [
        (4.4184, 114.0932), # Depot
        (4.3555, 113.9777), # Customers
        ...
    ]
    data["demands"] = [0, 5, 8, 3, 6, 5, 8, 3, 6, 5, 8] * len(vehicles)
    ```

### Interpreting the Output

The console output will provide detailed information about each vehicle's route, including:
- The sequence of customer locations visited
- The distance traveled to each location
- The total round trip distance and cost for each vehicle
- The total demand satisfied by each vehicle
 ``` Total Distance = 94.875 km
    Total Cost = RM 125.31
    Vehicle 1 (Type A):
    Round Trip Distance: 40.554 km, Cost: RM 48.66, Demand: 22
    Depot -> C7 (6.508 km) -> C10 (6.017 km) -> C9 (5.060 km) -> C8 (11.358 km) -> Depot (11.611 km)
    Vehicle 2 (Type A):
    Round Trip Distance: 16.120 km, Cost: RM 19.34, Demand: 8
    Depot -> C6 (8.060 km) -> Depot (8.060 km)
    Vehicle 3 (Type B):
    Round Trip Distance: 38.201 km, Cost: RM 57.30, Demand: 27
    Depot -> C2 (9.071 km) -> C5 (1.603 km) -> C1 (4.838 km) -> C4 (4.020 km) -> C3 (8.322 km) -> Depot (10.347 km)```

### Visualizing the Routes

The script also includes a function to plot the routes on a graph. After running the solver, a graph will be displayed showing the routes taken by each vehicle, with different colors representing different vehicle types.

### Customizing the Solver

You can customize the solver by modifying the constraints and parameters in the `main` function to better fit your needs. This includes changing the search parameters and the first solution strategy.


## Result Diagrams

Before Optimization             | After Optimization
:-------------------------:|:-------------------------:
![Vehicle Routing Before Optimization](images/before_optimization.png) | ![Vehicle Routing After Optimization](images/after_optimization.png)

