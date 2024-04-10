FROM python:3.10.9
RUN apt-get -y update &&\
    apt-get upgrade -y &&\
    apt-get install -y git && \
    apt-get install -y python3-dev &&\
    apt-get update -y

RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
RUN pip install torch_geometric

RUN git clone https://github.com/PeterBourgonje/GOLF_multilingual
RUN pip install -r GOLF_multilingual/requirements.txt

ENTRYPOINT /bin/bash