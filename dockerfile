FROM python:latest

WORKDIR /usr/app/src
COPY ./ ./

RUN pip install -r requirements.txt

CMD [ "python", "launcher/main.py"]