FROM python:3.7

WORKDIR /root/NekoBot

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

CMD ["python", "nekobot.py"]