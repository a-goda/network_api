ARG PYTHON_VERSION=3.12

# First Stage
FROM python:${PYTHON_VERSION} AS installerimage

LABEL org.opencontainers.image.authors="Ahmed Gadallah" \
      org.opencontainers.image.version="v1.0" \
      org.opencontainers.image.title="Network API" \
      org.opencontainers.image.description="API service for sending ssh commands and get netconf from a network device."

RUN mkdir -p /app
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install --yes --no-install-recommends 

# Create a virtual environment
RUN python -m venv /venv
ENV PATH=/venv/bin:$PATH

#bind-mounted files are only added temporarily for a single RUN instruction
RUN --mount=type=bind,source=requirements.txt,target=/tmp/requirements.txt \
    pip install --requirement /tmp/requirements.txt

# Second stage
FROM python:${PYTHON_VERSION} AS final

RUN mkdir -p /app
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV PATH=/venv/bin:$PATH

COPY --from=InstallerImage /venv /venv
COPY ./src ./src

ENTRYPOINT ["fastapi", "run", "src/main.py", "--port", "8080"]