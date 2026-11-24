from python:3.13.17-slim-trixie 
copy ./ /app
workdir /app
run pip install -r requirements.txt
cmd python3 Simulator.py