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

## Result Diagrams

Before Optimization             | After Optimization
:-------------------------:|:-------------------------:
![Vehicle Routing Before Optimization](images/before_optimization.png) | ![Vehicle Routing After Optimization](images/after_optimization.png)

