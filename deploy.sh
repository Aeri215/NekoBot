#!/bin/bash

echo "Reset"
git reset --hard HEAD
echo "pull"
git pull
echo "rmi"
docker rmi nekobot --force
docker build -t nekobot .
docker run -d nekobot