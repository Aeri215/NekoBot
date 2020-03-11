#!/bin/bash

git pull
docker build -t nekobot .
docker run nekobot