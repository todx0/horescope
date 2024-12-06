FROM python:3.12.8

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# If you want to use a virtual environment, uncomment the next lines
# RUN python -m venv venv
# ENV PATH="/app/venv/bin:$PATH"

# Copy the rest of the application code
COPY . /app/

# Set the command to run your bot
CMD ["python", "-m", "src.bot.bot"]
