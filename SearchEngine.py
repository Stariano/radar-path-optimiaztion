# Required imports
import numpy as np
import networkx as nx
from Boundaries import Boundaries
from Map import EPSILON

# Number of nodes expanded in the heuristic search (stored in a global variable to be updated from the heuristic functions)
NODES_EXPANDED = 0

def h1(current_node, objective_node) -> np.float32:
    """ First heuristic: Manhattan distance scaled by EPSILON 
    This is admissible because:
    1. Manhattan distance is the minimum number of cells to traverse
    2. Each cell has at least EPSILON cost
    3. Therefore, Manhattan * EPSILON is always <= actual path cost
    """
    global NODES_EXPANDED
    current = eval(current_node)
    objective = eval(objective_node)
    h = (abs(current[0] - objective[0]) + abs(current[1] - objective[1])) * EPSILON
    NODES_EXPANDED += 1
    return h

def h2(current_node, objective_node) -> np.float32:
    """ Second heuristic: Euclidean distance scaled by EPSILON
    This is admissible because:
    1. Euclidean distance is always <= actual path length
    2. Each cell has at least EPSILON cost
    3. Therefore, Euclidean * EPSILON is always <= actual path cost
    """
    global NODES_EXPANDED
    current = eval(current_node)
    objective = eval(objective_node)
    h = np.sqrt((current[0] - objective[0])**2 + (current[1] - objective[1])**2) * EPSILON
    NODES_EXPANDED += 1
    return h

def build_graph(detection_map: np.array, tolerance: np.float32) -> nx.DiGraph:
    """ Builds an adjacency graph (not an adjacency matrix) from the detection map """
    # Create a new directed graph
    G = nx.DiGraph()
    
    height, width = detection_map.shape
    
    # Add nodes and edges
    for i in range(height):
        for j in range(width):
            # Current node coordinates as string
            current = f"[{i}, {j}]"
            
            # Skip if current cell exceeds tolerance
            if detection_map[i, j] > tolerance:
                continue
                
            # Add node
            G.add_node(current)
            
            # Check all possible movements (up, down, left, right)
            moves = [(-1,0), (1,0), (0,-1), (0,1)]  # up, down, left, right
            
            for di, dj in moves:
                ni, nj = i + di, j + dj
                
                # Check if neighbor is within bounds and below tolerance
                if (0 <= ni < height and 0 <= nj < width and 
                    detection_map[ni, nj] <= tolerance):
                    neighbor = f"[{ni}, {nj}]"
                    # Add edge with detection probability as weight
                    G.add_edge(current, neighbor, weight=detection_map[ni, nj])
    
    return G

def discretize_coords(high_level_plan: np.array, boundaries: Boundaries, map_width: np.int32, map_height: np.int32) -> np.array:
    """ Converts coordinates from (lat, lon) into (x, y) """
    # Calculate the step sizes
    lat_step = (boundaries.max_lat - boundaries.min_lat) / (map_height - 1)
    lon_step = (boundaries.max_lon - boundaries.min_lon) / (map_width - 1)
    
    # Convert coordinates
    discretized = []
    for coord in high_level_plan:
        # Calculate grid indices
        i = int(round((coord[0] - boundaries.min_lat) / lat_step))
        j = int(round((coord[1] - boundaries.min_lon) / lon_step))
        
        # Ensure indices are within bounds
        i = max(0, min(i, map_height - 1))
        j = max(0, min(j, map_width - 1))
        
        discretized.append(f"[{i}, {j}]")
    
    return np.array(discretized)

def path_finding(G: nx.DiGraph,
                 heuristic_function,
                 locations: np.array, 
                 initial_location_index: np.int32, 
                 boundaries: Boundaries,
                 map_width: np.int32,
                 map_height: np.int32) -> tuple:
    """ Implementation of the main searching / path finding algorithm """
    global NODES_EXPANDED
    NODES_EXPANDED = 0
    
    # Convert high-level coordinates to grid coordinates
    grid_locations = discretize_coords(locations, boundaries, map_width, map_height)
    
    # Initialize solution plan
    solution_plan = []
    current_location = grid_locations[initial_location_index]
    
    # Visit all locations in sequence
    for i in range(len(grid_locations)):
        next_idx = (i + initial_location_index) % len(grid_locations)
        target_location = grid_locations[next_idx]
        
        try:
            # Find path using A* algorithm
            path = nx.astar_path(G, 
                               current_location,
                               target_location,
                               heuristic=heuristic_function,
                               weight="weight")
            
            # Add path to solution
            solution_plan.append(path)
            current_location = target_location
            
        except nx.NetworkXNoPath:
            print(f"No path found to target {target_location}")
            return solution_plan, NODES_EXPANDED
    
    return solution_plan, NODES_EXPANDED

def compute_path_cost(G: nx.DiGraph, solution_plan: list) -> np.float32:
    """ Computes the total cost of the whole planning solution """
    total_cost = 0.0
    
    # For each path segment in the solution
    for path in solution_plan:
        # For each pair of consecutive nodes in the path
        for i in range(len(path) - 1):
            # Add the edge weight to total cost
            total_cost += G[path[i]][path[i+1]]["weight"]
    
    return total_cost
