#!/bin/bash

git pull
docker rmi nekobot --force
docker build -t nekobot .
docker run -d nekobot