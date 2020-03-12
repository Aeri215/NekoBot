#!/bin/bash

git reset --hard HEAD
git pull
docker rmi nekobot --force
docker build -t nekobot .
docker run -d nekobot