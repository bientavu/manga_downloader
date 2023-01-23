FROM ubuntu:focal-20221130

SHELL ["/bin/bash", "-c"]

# Install python 3.8 & Xvfb
RUN set -x && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends software-properties-common && \
    add-apt-repository -y ppa:deadsnakes && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3.8-venv python3-pip && \
    apt-get install -y xvfb

# Install google chrome
RUN apt-get -y install wget && \
    apt install -y gpg-agent && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get update && \
    apt-get install -y google-chrome-stable

# Install chromedriver
RUN apt-get install -yqq unzip && \
    apt-get install -y curl && \
    wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* \

# Set display port to avoid crash
ENV DISPLAY=:99
