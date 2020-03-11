FROM python:3.7

WORKDIR /home

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r /requirements.txt

CMD ["python", "nekobot.py"]