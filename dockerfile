# ARG PYTHON_VERSION=3.14.0a3-slim
ARG PYTHON_VERSION=3.12

FROM python:${PYTHON_VERSION} AS installerimage
LABEL author="Ahmed Gadallah" \
    version="v1.0"


RUN mkdir -p /app
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 
    
# Create a virtual environment
RUN python -m venv /venv
ENV PATH=/venv/bin:$PATH

# COPY requirements.txt .
# COPY requirements.txt /tmp/requirements.txt
# RUN pip3 install --no-cache-dir --upgrade -r /tmp/requirements.txt

#bind-mounted files are only added temporarily for a single RUN instruction
RUN --mount=type=bind,source=requirements.txt,target=/tmp/requirements.txt \
    pip install --requirement /tmp/requirements.txt


FROM python:${PYTHON_VERSION} AS final

RUN mkdir -p /app
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV PATH=/venv/bin:$PATH

RUN pwd && ls -l

COPY --from=InstallerImage /venv /venv
COPY ./src ./src

RUN pwd && ls -l
# COPY ./src /app



ENTRYPOINT ["fastapi", "run", "src/main.py", "--port", "8080"]