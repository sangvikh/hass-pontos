# Testing

Simulates the endpoints used in the integration, making it possible to test device implementation without having a device available.

## How to use

Run with python from terminal, specify which sensor to simulate using '--device='. You can also specify the port and host IP address using the `--port` and `--host` arguments. Default is 0.0.0.0 port 5333
````
python3 serve.py --device safetech
python3 serve.py --device pontos
python3 serve.py --device safetech_v4
````

## Hardlinking into home assistant
Needs to be done on git pull/reset etc. Allows for editing files in the git repository and have it update within home assistant automatically.

````
bash link_hass_pontos.sh
````