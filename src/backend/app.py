from objectiveFunctionSteepest import objectiveFunctionSteepest
from steepestAscent import steepestAscent
from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import math
import copy

app = Flask(__name__)
CORS(app)

nums = []
magic_number = 315  # Magic number for 5x5x5 Diagonal Magic Cube

# Generate initial random state for the 5x5x5 cube
@app.route('/start-algorithm', methods=['POST'])
def start_algorithm():
    global nums
    nums = list(range(1, 126))  # Numbers from 1 to 125
    random.shuffle(nums)
    return jsonify(nums)

@app.route('/okay', methods=['POST'])
def okay():
    data = request.get_json()
    algorithm = data.get("algorithm")
    nums = array_algorithm_result(algorithm)
    return jsonify(nums)

def array_algorithm_result(algorithm):
    global nums
    if algorithm == 'SimulatedAnnealing':
        return simulated_annealing(nums)
    elif algorithm == 'SteepestAscent':
        return steepestAscent(nums, objectiveFunctionSteepest(nums))
    return list(range(1, 126))

def objective_function(cube, x=None, y=None, z=None, old_val=None, new_val=None):
    """Compute score for deviation from the magic number for affected rows, columns, pillars, and diagonals."""
    total_difference = 0
    n = 5

    # If no specific cell provided, compute full objective function
    if x is None:
        # Sum rows, columns, pillars, and diagonals
        for z in range(n):
            for y in range(n):
                row_sum = sum(cube[z][y][x] for x in range(n))
                total_difference += abs(magic_number - row_sum)
        
        for y in range(n):
            for x in range(n):
                col_sum = sum(cube[z][y][x] for z in range(n))
                total_difference += abs(magic_number - col_sum)

        for x in range(n):
            for z in range(n):
                pillar_sum = sum(cube[z][y][x] for y in range(n))
                total_difference += abs(magic_number - pillar_sum)

        # Diagonals for each plane
        for z in range(n):
            main_diag_xy = sum(cube[z][i][i] for i in range(n))
            anti_diag_xy = sum(cube[z][i][n - 1 - i] for i in range(n))
            total_difference += abs(magic_number - main_diag_xy)
            total_difference += abs(magic_number - anti_diag_xy)

        for y in range(n):
            main_diag_xz = sum(cube[i][y][i] for i in range(n))
            anti_diag_xz = sum(cube[i][y][n - 1 - i] for i in range(n))
            total_difference += abs(magic_number - main_diag_xz)
            total_difference += abs(magic_number - anti_diag_xz)

        for x in range(n):
            main_diag_yz = sum(cube[i][i][x] for i in range(n))
            anti_diag_yz = sum(cube[n - 1 - i][i][x] for i in range(n))
            total_difference += abs(magic_number - main_diag_yz)
            total_difference += abs(magic_number - anti_diag_yz)

        # 3D diagonals
        diag1_sum = sum(cube[i][i][i] for i in range(n))
        diag2_sum = sum(cube[i][i][n - 1 - i] for i in range(n))
        diag3_sum = sum(cube[i][n - 1 - i][i] for i in range(n))
        diag4_sum = sum(cube[n - 1 - i][i][i] for i in range(n))

        total_difference += abs(magic_number - diag1_sum)
        total_difference += abs(magic_number - diag2_sum)
        total_difference += abs(magic_number - diag3_sum)
        total_difference += abs(magic_number - diag4_sum)

    return total_difference

# Tambahkan variabel global untuk menyimpan nilai objective function per iterasi
iteration_data = []

def simulated_annealing(nums):
    global iteration_data
    iteration_data = []  # Reset data iterasi

    T = 100.0      # Initial temperature
    T_min = 0.001  # Minimum temperature
    alpha = 0.9999  # Cooling rate
    n = 5          # Cube dimension

    current_state = [nums[i * 25:(i + 1) * 25] for i in range(5)]
    current_state = [[current_state[z][y * 5:(y + 1) * 5] for y in range(5)] for z in range(5)]
    current_cost = objective_function(current_state)

    # Simpan nilai objective function awal
    iteration_data.append(current_cost)

    while T > T_min:
        z1, y1, x1 = random.randint(0, n - 1), random.randint(0, n - 1), random.randint(0, n - 1)
        z2, y2, x2 = random.randint(0, n - 1), random.randint(0, n - 1), random.randint(0, n - 1)

        old_val_1, old_val_2 = current_state[z1][y1][x1], current_state[z2][y2][x2]
        current_state[z1][y1][x1], current_state[z2][y2][x2] = old_val_2, old_val_1

        new_cost = objective_function(current_state)

        if new_cost < current_cost or random.random() < math.exp((current_cost - new_cost) / T):
            current_cost = new_cost
        else:
            current_state[z1][y1][x1], current_state[z2][y2][x2] = old_val_1, old_val_2

        T *= alpha

        # Simpan nilai objective function setelah setiap iterasi
        iteration_data.append(current_cost)

    final_state = [num for layer in current_state for row in layer for num in row]
    return final_state

# Endpoint untuk mengirim data iterasi ke frontend
@app.route('/get-iteration-data', methods=['GET'])
def get_iteration_data():
    return jsonify(iteration_data)

if __name__ == '__main__':
    app.run(debug=True)
