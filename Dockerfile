# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster

ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# install the OS build deps
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    python3-dev \
    openssl \
    cargo \
    python3-pip \
 && rm -rf /var/lib/apt/lists/*

# Make sure below dns server is set in docker configuration.
# Without it, pip resolving will be failed during docker build.
# $ sudo cat /etc/docker/daemon.json
# {
#     "dns": ["8.8.8.8", "8.8.4.4"]
# }
# Update pip and install pip requirements
RUN python -m pip install --upgrade pip
ADD src/requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
ADD . /app

# Switching to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
RUN useradd appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "./src/teslamate_telegram_bot.py"]
