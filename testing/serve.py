import argparse
import json
import os
from flask import Flask, jsonify, request

DEVICE_CONFIGS = {
    "safetech": {
        "prefix": "/trio",
        "filename": "safetech.json",
        "defaults": {"getVLV": 10, "getPRF": 1, "getALA": "ff"},
    },
    "pontos": {
        "prefix": "/pontos-base",
        "filename": "pontos.json",
        "defaults": {
            "getVLV": 20,  # 10=closed, 20=open in your example
            "getPRF": 1,
            "getALA": "ff",
            "getCND": "300",  # For "water conductivity/hardness"
        },
    },
    "safetech_v4": {
        "prefix": "/safe-tec",
        "filename": "safetech_v4.json",
        "defaults": {"getVLV": 10, "getPRF": 2, "getALA": "ff"},
    },
    "safetech_v4_copy": {
        "prefix": "/safe-tec",
        "filename": "safetech_v4_copy.json",
        "defaults": {"getVLV": 10, "getPRF": 2, "getALA": "ff"},
    },
    "neosoft": {
        "prefix": "/neosoft",
        "filename": "neosoft.json",
        "defaults": {"getVLV": 10, "getPRF": 1, "getALA": "ff"},
    },
}

ALL_DEVICE_DATA = {}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run the test server for a specific device type."
    )
    parser.add_argument(
        "--device",
        choices=DEVICE_CONFIGS.keys(),
        required=True,
        help="Which device to serve: 'safetech', 'pontos', 'safetech_v4', 'safetech_v4_copy', or 'neosoft'.",
    )
    parser.add_argument(
        "--port", type=int, default=5333, help="Port to run the Flask app on."
    )
    parser.add_argument(
        "--host", type=str, default="0.0.0.0", help="Host to run the Flask app on."
    )
    return parser.parse_args()


def load_device_data(device_key):
    """
    Load the JSON file for the selected device into memory.
    """
    config = DEVICE_CONFIGS[device_key]
    filename = config["filename"]
    path = os.path.join(os.path.dirname(__file__), filename)

    try:
        with open(path, "r") as f:
            ALL_DEVICE_DATA[device_key] = json.load(f)
        print(f"Loaded {filename} for '{device_key}'.")
    except (FileNotFoundError, json.JSONDecodeError):
        ALL_DEVICE_DATA[device_key] = {}
        print(
            f"Warning: Could not load {filename} for '{device_key}', using empty data."
        )


def register_device_endpoints(app, device_key):
    """
    Dynamically create the “/get” and “/set” routes for the chosen device type.
    Ensures the same valve/profile logic is implemented for each device.
    """
    prefix = DEVICE_CONFIGS[device_key]["prefix"]
    defaults = DEVICE_CONFIGS[device_key]["defaults"]

    @app.route(prefix + "/get/all", methods=["GET"])
    def get_all():
        return jsonify(ALL_DEVICE_DATA[device_key])

    @app.route(prefix + "/get/<command>", methods=["GET"])
    def get_command(command):
        data = ALL_DEVICE_DATA[device_key]
        cmd_upper = command.upper()
        response_data = {}

        # --- Example for valve status:
        if cmd_upper == "VLV":
            response_data["getVLV"] = data.get("getVLV", defaults["getVLV"])

        # --- Example for the profile:
        elif cmd_upper == "PRF":
            response_data["getPRF"] = data.get("getPRF", defaults["getPRF"])

        # --- Example for the alarm:
        elif cmd_upper == "ALA":
            response_data["getALA"] = data.get("getALA", defaults["getALA"])

        # --- Example for the Pontos “CND” (water conductivity/hardness):
        elif cmd_upper == "CND":
            # Some devices might not have CND at all. For Pontos, it’s used. If you want it for others, add it similarly.
            response_data["getCND"] = data.get("getCND", defaults.get("getCND", "300"))

        else:
            # Fallback
            key = "get" + cmd_upper
            if key in data:
                response_data[key] = data[key]
            else:
                response_data = {"error": f"Unknown command: {command}"}

        return jsonify(response_data)

    @app.route(prefix + "/set/<command>", methods=["GET"])
    @app.route(prefix + "/set/<command>/<value>", methods=["GET"])
    def set_command(command, value=None):
        data = ALL_DEVICE_DATA[device_key]
        cmd_upper = command.upper()
        response_data = {}

        # The AB command is used for opening/closing the valve.
        if cmd_upper == "AB":
            if value is None:
                return jsonify({"error": "Missing value for AB command"}), 400

            # Check which device we’re dealing with:
            if device_key == "pontos" or device_key == "safetech_v4":
                # For Pontos, "1" => open, "2" => close
                if value == "1":
                    data["getVLV"] = 20  # 20 => valve open
                    data["setAB"] = "open"
                    response_data["getVLV"] = data["getVLV"]
                    response_data["setAB"] = "open"
                elif value == "2":
                    data["getVLV"] = 10  # 10 => valve closed
                    data["setAB"] = "close"
                    response_data["getVLV"] = data["getVLV"]
                    response_data["setAB"] = "close"
                else:
                    return (
                        jsonify({"error": f"Invalid AB value for Pontos: {value}"}),
                        400,
                    )
            else:
                # For Trio / SafeTec, "true" => closed (10), "false" => open (20)
                bool_val = value.lower() == "true"
                data["setAB"] = bool_val
                # If “true” => valve closed => getVLV=10; “false” => valve open => getVLV=20
                data["getVLV"] = 10 if bool_val else 20
                response_data["setAB"] = bool_val
                response_data["getVLV"] = data["getVLV"]

        # Profile switching logic:
        elif cmd_upper == "PRF":
            if value is None:
                return jsonify({"error": "Missing value for PRF command"}), 400
            try:
                profile_num = int(value)
            except ValueError:
                return jsonify({"error": f"Invalid profile number: {value}"}), 400

            data["getPRF"] = profile_num
            response_data["setPRF"] = profile_num

        # --- Example of the special “CND” set command (optional):
        #     If you wanted to allow setting getCND, do something like:
        elif cmd_upper == "CND":
            if not value:
                return jsonify({"error": "Missing value for CND"}), 400
            data["getCND"] = value
            response_data["setCND"] = value

        else:
            # Fallback
            if value is None:
                data[f"set{cmd_upper}"] = "OK"
                response_data[f"set{cmd_upper}"] = "OK"
            else:
                data[f"set{cmd_upper}{value}"] = "OK"
                response_data[f"set{cmd_upper}{value}"] = "OK"

        return jsonify(response_data)


def create_app(device_key):
    """
    Create a Flask app that only serves endpoints for the specified device.
    """
    app = Flask(__name__)
    register_device_endpoints(app, device_key)
    return app


if __name__ == "__main__":
    args = parse_args()
    device_key = args.device

    # Load the JSON data for that device
    load_device_data(device_key)

    # Create and run the Flask app with that device’s routes
    app = create_app(device_key)
    print(f"Starting Flask app for device: {device_key} on port: {args.port}")
    app.run(host=args.host, port=args.port, debug=True)
