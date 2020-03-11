FROM python:3.7

WORKDIR /root/NekoBot

COPY requirements.txt /tmp
RUN pip install -r requirements.txt
COPY . /tmp/myapp
RUN pip install /tmp/myapp

CMD ["python", "nekobot.py"]