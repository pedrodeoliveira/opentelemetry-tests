FROM python:3.7-slim

# copy and install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy source file
COPY . .

CMD ["python", "otcollector-metrics.py"]
