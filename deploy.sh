#!/bin/bash

git pull
docker build -t NekoBot .
docker run NekoBot