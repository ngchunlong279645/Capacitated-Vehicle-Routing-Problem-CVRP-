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

### OR-Tools
#### Prepare The Data

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

#### Interpreting the Output

The console output will provide detailed information about each vehicle's route, including:
- The sequence of customer locations visited
- The distance traveled to each location
- The total round trip distance and cost for each vehicle
- The total demand satisfied by each vehicle
 ```
    Total Distance = 94.875 km
    Total Cost = RM 125.31
    Vehicle 1 (Type A):
    Round Trip Distance: 40.554 km, Cost: RM 48.66, Demand: 22
    Depot -> C7 (6.508 km) -> C10 (6.017 km) -> C9 (5.060 km) -> C8 (11.358 km) -> Depot (11.611 km)
    Vehicle 2 (Type A):
    Round Trip Distance: 16.120 km, Cost: RM 19.34, Demand: 8
    Depot -> C6 (8.060 km) -> Depot (8.060 km)
    Vehicle 3 (Type B):
    Round Trip Distance: 38.201 km, Cost: RM 57.30, Demand: 27
    Depot -> C2 (9.071 km) -> C5 (1.603 km) -> C1 (4.838 km) -> C4 (4.020 km) -> C3 (8.322 km) -> Depot (10.347 km)
 ```

#### Customizing the Solver

You can customize the solver by modifying the constraints and parameters in the `main` function to better fit your needs. This includes changing the search parameters and the first solution strategy.
 ```python
    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )
    search_parameters.time_limit.FromSeconds(1)
 ```
### Nearest Neighbor Heuristic

The Nearest Neighbor heuristic is a simple and intuitive method used to approximate solutions for the CVRP. It works by starting at the depot, selecting the nearest unvisited customer, and repeating this process until the vehicle's capacity is reached or there are no more customers to visit.

#### Preparing The Data
1. Define customer data file location
Ensure you have customer data in an Excel file and set to correct path
 ```python
Read customer data from an Excel file
    customer_data = pd.read_excel(r"C:\Users\User\Desktop\customerData.xlsx")
 ```
2. Set Depot Location

Define the location of the depot where vehicles start and end their routes. You need to specify the latitude and longitude coordinates for the depot.
```python
# Define depot
    depot = Depot(latitude=4.4184, longitude=114.0932)
```

3. Define Vehicle Types and Capacities

Determine the number of vehicles and their types required for the delivery problem. You can define multiple vehicle types with different capacities. 
```python
# Define the number of vehicles of each type
    num_type_a_vehicles = 2
    num_type_b_vehicles = 1
```

4. Run the Solver

Execute the main script to solve the delivery problem.

#### Interpreting the Output

The console output will provide detailed information about each vehicle's route:
 ```
Total Distance = 106.88 km
Total Cost = RM 137.65
Vehicle 1 (Type A):
Round Trip Distance: 53.582 km, Cost: RM 64.30, Demand: 25.0
Depot -> C7 (6.508 km) -> C10 (6.018 km) -> C9 (5.060 km) -> C8 (11.358 km) -> C3 (14.290 km) -> Depot (10.347 km)
Vehicle 2 (Type A):
Round Trip Distance: 21.981 km, Cost: RM 26.38, Demand: 21.0
Depot -> C6 (8.061 km) -> C2 (1.834 km) -> C5 (1.604 km) -> Depot (10.483 km)
Vehicle 3 (Type B):
Round Trip Distance: 31.315 km, Cost: RM 46.97, Demand: 11.0
Depot -> C1 (13.152 km) -> C4 (4.021 km) -> Depot (14.142 km)
 ```

## Result Comparison between OR-tools and Nearest Neighbor

OR-tools            | Neareast Neighbour
:-------------------------:|:-------------------------:
![image](https://github.com/ngchunlong279645/Capacitated-Vehicle-Routing-Problem-CVRP-/assets/73117650/d6cea7f0-fbd2-460c-b5e6-02ca176bbd81) | ![image](https://github.com/ngchunlong279645/Capacitated-Vehicle-Routing-Problem-CVRP-/assets/73117650/b5fa34ae-36bc-426a-b8bd-19daef251669)

