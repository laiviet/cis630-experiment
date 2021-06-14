#!/bin/bash

CONTAINER_IMG=pytorchlightning/pytorch_lightning:latest-py3.7-torch1.6
CONTAINER_NAME=cuda

docker stop $CONTAINER_NAME
docker container rm $CONTAINER_NAME

docker run -it --name $CONTAINER_NAME \
               --memory 64g \
               --shm-size 16g \
               --ipc=host \
               --network=host \
               --hostname=$HOSTNAME \
               -v /disk/vietl/.miniconda3/:/disk/vietl/.miniconda3/ \
               -v /home/users/vietl/projects/cis630:/root/cis630 \
               --gpus all \
               $CONTAINER_IMG