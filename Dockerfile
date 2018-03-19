FROM ubuntu:latest

RUN apt-get update && apt-get install -y tshark python3 python3-virtualenv
RUN rm -rf /var/lib/apt/lists/*

RUN adduser gallimaufry

WORKDIR /home/gallimaufry

RUN mkdir /home/gallimaufry/gallimaufry
RUN mkdir /home/gallimaufry/.virtualenvs

COPY . /home/gallimaufry/gallimaufry/
RUN chown -R gallimaufry:gallimaufry /home/gallimaufry/.

USER gallimaufry

RUN python3 -m virtualenv --python=$(which python3) ~/.virtualenvs/gallimaufry
RUN echo ". ~/.virtualenvs/gallimaufry/bin/activate" >> ~/.bashrc
RUN . ~/.virtualenvs/gallimaufry/bin/activate && pip install ipython && cd gallimaufry && pip install -e .
