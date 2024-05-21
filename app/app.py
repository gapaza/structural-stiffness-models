from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the PyMesh and Flask Server!"

@app.route('/compute_geometry', methods=['POST'])
def compute_geometry():
    data = request.json
    CA = data['CA']
    NC = data['NC']
    radius = data['radius']





    result = {'volume': 0.11}  # Replace with actual computation
    return jsonify(result)

if __name__ == '__main__':
    print('Running flask')
    app.run(host='0.0.0.0', port=8483)