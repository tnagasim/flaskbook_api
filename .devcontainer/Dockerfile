FROM mcr.microsoft.com/devcontainers/python:1.2.4-3.13-bookworm
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y tzdata && \
    ln -fs /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata
RUN apt-get update && apt-get install -y libgl1
