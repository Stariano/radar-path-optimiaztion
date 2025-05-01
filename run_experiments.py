#!/usr/bin/env python3
import subprocess
import json
import time
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def run_scenario(scenario_name, tolerance, results):
    """Run a single scenario and capture its results"""
    start_time = time.time()
    
    # Run the scenario
    process = subprocess.Popen(
        ['python3', 'main.py', scenario_name, str(tolerance)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    stdout, stderr = process.communicate()
    
    # Extract results from output
    execution_time = time.time() - start_time
    
    # Parse output for metrics
    path_cost = None
    nodes_expanded = None
    for line in stdout.split('\n'):
        if "Total path cost:" in line:
            path_cost = float(line.split(":")[1].strip())
        elif "Number of expanded nodes:" in line:
            nodes_expanded = int(line.split(":")[1].strip())
    
    # Store results
    results.append({
        'scenario': scenario_name,
        'tolerance': tolerance,
        'path_cost': path_cost,
        'nodes_expanded': nodes_expanded,
        'execution_time': execution_time,
        'success': path_cost is not None
    })

def main():
    # Create results directory
    Path('results').mkdir(exist_ok=True)
    
    # Load scenarios
    with open('scenarios.json', 'r') as f:
        scenarios = json.load(f)
    
    # Test parameters
    tolerances = [0.3, 0.5, 0.7]
    results = []
    
    # Run experiments
    for scenario in scenarios:
        scenario_name = list(scenario.keys())[0]
        print(f"\nTesting scenario: {scenario_name}")
        
        for tolerance in tolerances:
            print(f"  With tolerance: {tolerance}")
            run_scenario(scenario_name, tolerance, results)
    
    # Convert results to DataFrame
    df = pd.DataFrame(results)
    
    # Save raw results
    df.to_csv('results/experiment_results.csv', index=False)
    
    # Generate plots
    
    # 1. Path costs vs Tolerance for each scenario
    plt.figure(figsize=(12, 6))
    for scenario_name in df['scenario'].unique():
        scenario_data = df[df['scenario'] == scenario_name]
        plt.plot(scenario_data['tolerance'], scenario_data['path_cost'], 
                marker='o', label=scenario_name)
    plt.xlabel('Tolerance')
    plt.ylabel('Path Cost')
    plt.title('Path Costs vs Tolerance by Scenario')
    plt.legend()
    plt.grid(True)
    plt.savefig('results/path_costs.png')
    plt.close()
    
    # 2. Nodes expanded vs Grid size
    plt.figure(figsize=(12, 6))
    scenario_sizes = [(int(list(s.values())[0]['W']), list(s.keys())[0]) 
                     for s in scenarios]
    scenario_sizes.sort()
    sizes = [size for size, _ in scenario_sizes]
    
    for tolerance in tolerances:
        nodes = []
        for _, scenario_name in scenario_sizes:
            scenario_data = df[(df['scenario'] == scenario_name) & 
                             (df['tolerance'] == tolerance)]
            nodes.append(scenario_data['nodes_expanded'].iloc[0] 
                       if not scenario_data.empty else 0)
        plt.plot(sizes, nodes, marker='o', label=f'Tolerance={tolerance}')
    
    plt.xlabel('Grid Size')
    plt.ylabel('Nodes Expanded')
    plt.title('Search Space Exploration vs Grid Size')
    plt.legend()
    plt.grid(True)
    plt.savefig('results/nodes_expanded.png')
    plt.close()
    
    # Print summary statistics
    print("\nSummary Statistics:")
    print("\nAverage path cost by tolerance:")
    print(df.groupby('tolerance')['path_cost'].mean())
    print("\nAverage nodes expanded by tolerance:")
    print(df.groupby('tolerance')['nodes_expanded'].mean())
    print("\nSuccess rate by scenario:")
    print(df.groupby('scenario')['success'].mean())

if __name__ == '__main__':
    main() 