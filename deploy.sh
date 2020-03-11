#!/bin/bash

git pull
docker rmi nekobot
docker build -t nekobot .
docker run nekobot