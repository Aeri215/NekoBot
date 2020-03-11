FROM python:3.7

WORKDIR /root/NekoBot

RUN pip install -r requirements.txt

CMD ["python", "nekobot.py"]