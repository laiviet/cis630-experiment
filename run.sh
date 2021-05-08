#!/bin/bash

#conda activate py37

export master=node-0
export MASTER_PORT=12345
export CUDA_VISIBLE_DEVICES=0,1
export NCCL_SOCKET_IFNAME=eno33
export GLOO_SOCKET_IFNAME=eno33
export NCCL_DEBUG=INFO
export NCCL_DEBUG_SUBSYS=ALL

NODE=1
GPU=2
WORLD_SIZE=$(expr $NODE \* $GPU)
export WORLD_SIZE=$WORLD_SIZE
if [[ $HOSTNAME == "node-0.test-code.cis630dnn-pg0.clemson.cloudlab.us" ]] ; then
  echo "NOde 0"
  NODE_RANK=0 LOCAL_RANK=0 python resnet.py --gpu $GPU --node $NODE &
fi

if [[ $HOSTNAME == "node-1.test-code.cis630dnn-pg0.clemson.cloudlab.us" ]] ; then
  echo "NOde 1"
  NODE_RANK=1 LOCAL_RANK=0 python resnet.py  --gpu $GPU --node $NODE &
fi
