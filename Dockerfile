FROM python:3.10-slim
WORKDIR usr/src/app

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt

# Run the application:
# COPY ./src .
# CMD ["python", "src/main.py"]

# Command line
# docker build -t gic .
# To run main: docker run --rm -ti -v /home/jewelaw/gic-assignment:/app gic python /app/src/main.py
# To run tests: docker run --rm -ti -v /home/jewelaw/gic-assignment:/app gic pytest /app/tests
