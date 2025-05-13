# Testing

## How to use

Run with python from terminal, specify which sensor to simulate using --device=
Sensor can now be added in home assistant on the local ip of the host

````
python3 serve.py --device safetech
python3 serve.py --device pontos
python3 serve.py --device safetech_v4
````

## Hardlinking into home assistant
Needs to be done on git pull/reset etc. Allows for editing files in the git repository and have it update within home assistant automatically.
