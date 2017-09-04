FROM ubuntu:17.04

RUN apt-get update && apt-get install -y tshark python3 python3-virtualenv
RUN rm -rf /var/lib/apt/lists/*

RUN adduser usb_parser

WORKDIR /home/usb_parser

RUN mkdir /home/usb_parser/usb_parser
RUN mkdir /home/usb_parser/.virtualenvs

COPY . /home/usb_parser/usb_parser/
RUN chown -R usb_parser:usb_parser /home/usb_parser/.

USER usb_parser

RUN python3 -m virtualenv --python=$(which python3) ~/.virtualenvs/usb_parser
RUN echo ". ~/.virtualenvs/usb_parser/bin/activate" >> ~/.bashrc
RUN . ~/.virtualenvs/usb_parser/bin/activate && pip install ipython && cd usb_parser && pip install -e .
