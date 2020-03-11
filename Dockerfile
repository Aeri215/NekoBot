FROM python:3.7

WORKDIR /home

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt
COPY Commands /home/Commands
COPY mechanics /home/mechanics
COPY Static /home/Static
COPY nekobot.py /home/nekobot.py

RUN pip install -r requirements.txt

CMD ["python", "nekobot.py"]