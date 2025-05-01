# Stealth Aircraft Path Planning System

## Project Overview
This project implements a path planning system for a stealth aircraft navigating through radar-monitored airspace. The system uses A* search algorithm to find optimal paths that minimize radar detection probability while visiting specified points of interest (POIs).

## Setup Instructions

### Prerequisites
- Python 3.x
- pip3 (Python package installer)

### Installation
1. Clone or download the project repository
2. Install required dependencies:
```bash
pip3 install -r requirements.txt
```

## Running the System

### Single Scenario Execution
To run a single scenario:
```bash
python3 main.py <scenario_name> <tolerance>
```
Example:
```bash
python3 main.py scenario_0 0.5
```

Parameters:
- `scenario_name`: Name of the scenario from scenarios.json (e.g., scenario_0, scenario_1, etc.)
- `tolerance`: Maximum acceptable detection probability (0.0 to 1.0)

### Running All Experiments
To run all scenarios with different tolerance values and generate analysis:
```bash
python3 run_experiments.py
```
This will:
1. Test all scenarios with tolerances 0.3, 0.5, and 0.7
2. Generate performance plots in the `results` directory
3. Save detailed results to `results/experiment_results.csv`

## Project Structure

### Core Components
- `main.py`: Entry point and visualization
- `Map.py`: Grid generation and radar detection calculations
- `Radar.py`: Radar system modeling
- `SearchEngine.py`: A* search implementation with heuristics
- `Location.py`: Location coordinate handling
- `Boundaries.py`: Map boundary definitions

### Configuration and Testing
- `scenarios.json`: Test scenario configurations
- `run_experiments.py`: Automated testing script
- `requirements.txt`: Required Python packages

### Results and Documentation
- `results/`: Directory containing experiment results and plots
- `Technical_Report.tex`: LaTeX source for technical documentation
- `Technical_Report.pdf`: Compiled technical report

## Available Scenarios
1. `scenario_0`: Basic scenario (16x16 grid, 1 radar)
2. `scenario_1`: Multiple radars (16x16 grid, 3 radars)
3. `scenario_2` - `scenario_9`: Increasing complexity scenarios
4. `scenario_dense`: High radar density test
5. `scenario_sparse`: Low radar density test
6. `scenario_zigzag`: Complex path planning test

## Output Files
The system generates several outputs:
1. Real-time visualizations:
   - Radar locations plot
   - Detection probability fields
   - Solution path with waypoints
2. Analysis files (when running experiments):
   - `results/experiment_results.csv`: Raw performance data
   - `results/path_costs.png`: Path cost analysis
   - `results/nodes_expanded.png`: Search efficiency analysis

## Troubleshooting

### Common Issues
1. Missing dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

2. Permission errors:
   ```bash
   chmod +x run_experiments.py
   ```

3. Display issues:
   - Ensure matplotlib backend is configured correctly
   - Try running in a different terminal if plots don't display

### Error Messages
- "No module found": Run `pip3 install -r requirements.txt`
- "No such file": Check working directory
- "No path found": Try increasing tolerance value

## Performance Considerations
- Large grid sizes (>256x256) may take significant time
- High radar counts increase computation time
- Memory usage scales with grid size
