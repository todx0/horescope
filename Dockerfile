FROM python:3.12-slim

WORKDIR /app

# Create venv inside the container
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Rest of your Dockerfile remains the same
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["/bin/bash", "-c", "source /opt/venv/bin/activate && python -m src.main"]