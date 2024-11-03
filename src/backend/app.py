from flask import Flask, jsonify, request
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# start itu untuk membuat initial state (random tapi diantara 1-125 inklusif)
@app.route('/start-algorithm', methods=['POST'])
def start_algorithm():
    nums = list(range(1, 126))
    random.shuffle(nums)
    return jsonify(nums)

# setelah melihat state yang di-generate, klik apakah setuju, kalau setuju klik okay
# kalau gak setuju klik start lagi supaya di-generate initial state yang baru
@app.route('/okay', methods=['POST'])
def okay():
    data = request.get_json()
    algorithm = data.get("algorithm")
    nums = array_algorithm_result(algorithm)
    return jsonify(nums)

def array_algorithm_result(algorithm):
    # Logika untuk membuat array awal berdasarkan pilihan algoritma
    if algorithm == 'SteepestAscent':
        return list(range(1, 126))
    elif algorithm == 'GeneticAlgorithm':
        return list(range(1, 126))
    elif algorithm == 'SimulatedAnnealing':
        return list(range(4, 129))

if __name__ == '__main__':
    app.run(debug=True)