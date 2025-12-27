FROM python:3.13.11-slim-trixie

# The platform (CPU architecture)
# if not provided by a build-arg we take a default (ARM)
ARG PLATFORM=amd64
ENV PLATFORM=$PLATFORM

# Install our main Python requirements
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt

# Add the user and sudo support
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y \
        bash-completion \
        locales \
        sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Install locales and set the default
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen \
    && locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

USER $USERNAME
