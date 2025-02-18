import json
import os
from flask import Flask, jsonify

app = Flask(__name__)

# Global in-memory storage of device state
device_data = {}

def load_device_data():
    """Load the initial JSON data from safetech.json into 'device_data'."""
    global device_data
    file_path = os.path.join(os.path.dirname(__file__), "safetech.json")
    try:
        with open(file_path, "r") as f:
            device_data = json.load(f)
        print("Loaded safetech.json into memory.")
    except FileNotFoundError:
        device_data = {}
        print(f"Warning: {file_path} not found; using empty data.")
    except json.JSONDecodeError:
        device_data = {}
        print("Warning: Could not parse safetech.json; using empty data.")

@app.route("/trio/get/all", methods=["GET"])
def get_all_data():
    """
    Return the full 'device_data' dict, simulating a GET /trio/get/all endpoint.
    """
    return jsonify(device_data)

@app.route("/trio/get/<command>", methods=["GET"])
def get_command(command):
    """
    Handle requests like: GET /trio/get/<command>
    We'll look up 'command' in device_data and return a JSON object.
    For example, /trio/get/vlv -> { "getVLV": device_data["getVLV"] }
    """
    cmd_upper = command.upper()
    response_data = {}

    if cmd_upper == "VLV":
        # The doc says "getVLV" is an integer in device_data
        response_data["getVLV"] = device_data.get("getVLV", 10)
    elif cmd_upper == "PRF":
        response_data["getPRF"] = device_data.get("getPRF", 1)
    elif cmd_upper == "ALA":
        response_data["getALA"] = device_data.get("getALA", "ff")
    else:
        # Fallback: Just return { "command": device_data["someKey"] } if it exists
        key = "get" + cmd_upper
        if key in device_data:
            response_data[key] = device_data[key]
        else:
            response_data = {"error": f"Unknown command: {command}"}

    return jsonify(response_data)

@app.route("/trio/set/<command>", methods=["GET"])
@app.route("/trio/set/<command>/<value>", methods=["GET"])
def set_command(command, value=None):
    """
    Handle requests like:
      GET /trio/set/<command>           (without value)
      GET /trio/set/<command>/<value>   (with value)
    We'll parse <command> and <value>, then modify 'device_data' accordingly.
    """

    cmd_upper = command.upper()
    response_data = {}

    # Example: /trio/set/ab/true  -> closes the valve
    #          /trio/set/ab/false -> opens the valve
    if cmd_upper == "AB":
        if value is None:
            return jsonify({"error": "Missing value for AB command"}), 400

        # The doc says: AB bool => false => valve open, true => valve closed
        bool_val = (value.lower() == "true")
        device_data["setAB"] = bool_val
        if bool_val:
            # Valve closed
            device_data["getVLV"] = 10
        else:
            # Valve open
            device_data["getVLV"] = 20

        response_data["setAB"] = bool_val
        response_data["getVLV"] = device_data["getVLV"]

    # Example: /trio/set/prf/2 -> sets the active profile to 2
    elif cmd_upper == "PRF":
        if value is None:
            return jsonify({"error": "Missing value for PRF command"}), 400

        try:
            profile_num = int(value)
        except ValueError:
            return jsonify({"error": f"Invalid profile number: {value}"}), 400

        # The doc says "1-8" are valid
        if profile_num < 1 or profile_num > 8:
            return jsonify({"error": f"Profile out of range: {profile_num}"}), 400

        device_data["getPRF"] = profile_num
        response_data["setPRF"] = profile_num

    else:
        # Fallback for unknown commands
        # We store them generically to avoid errors.
        if value is None:
            device_data[f"set{cmd_upper}"] = "OK"
            response_data[f"set{cmd_upper}"] = "OK"
        else:
            device_data[f"set{cmd_upper}{value}"] = "OK"
            response_data[f"set{cmd_upper}{value}"] = "OK"

    return jsonify(response_data)

if __name__ == "__main__":
    load_device_data()
    app.run(host="0.0.0.0", port=5333)
