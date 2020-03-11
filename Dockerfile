FROM python:3.7

WORKDIR /home

RUN easy_install pip
RUN pip install -r /home/requirements.txt

CMD ["python", "nekobot.py"]