import json
from flask import Flask, jsonify

app = Flask(__name__)

# Existing endpoint for /trio/get/all
@app.route('/trio/get/all', methods=['GET'])
def get_data():
    # Load data from the safetech.json file
    try:
        with open('safetech.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error reading JSON"}), 500

    return jsonify(data)

# New endpoint for /set/ADM/(2)f
@app.route('trio/set/ADM/(2)f', methods=['GET'])
def set_adm():
    # Return the predefined response
    return jsonify({"setADM(2)f": "FACTORY"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5333)
