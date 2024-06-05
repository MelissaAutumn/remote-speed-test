from python:3.11-alpine

workdir /code/

copy main.py .
copy requirements.txt .

run pip install -r requirements.txt

cmd fastapi run main.py