FROM python:3.7

WORKDIR /home

RUN pip install --upgrade pip
RUN pip install -r /home/requirements.txt

CMD ["python", "nekobot.py"]