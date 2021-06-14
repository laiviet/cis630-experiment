#!/bin/bash

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/disk/vietl/.miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/disk/vietl/.miniconda3/etc/profile.d/conda.sh" ]; then
        . "/disk/vietl/.miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/disk/vietl/.miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

export MASTER_ADDR=legendary2.cs.uoregon.edu
export MASTER_PORT=12346
export CUDA_VISIBLE_DEVICES=1,3
#export NCCL_SOCKET_IFNAME=eno33
#export GLOO_SOCKET_IFNAME=eno33
#export NCCL_DEBUG=INFO
#export NCCL_DEBUG_SUBSYS=ALL

conda activate ds


NODE=2
GPU=2
BATCH_SIZE=128
EPOCH=40
MODEL=18
export LOCAL_RANK=0
export WORLD_SIZE=$(expr $NODE \* $GPU)

export LD_LIBRARY_PATH=/home/users/vietl/tmp/nccl/build/lib:$LD_LIBRARY_PATH

for SEED in 1 2 3 4 5 ; do
  if [[ $HOSTNAME == "legendary2" ]] ; then
    echo "LD2"
    export NODE_RANK=0
  elif [[ $HOSTNAME == "legendary1" ]] ; then
    echo "LD1"
    export NODE_RANK=1
  fi
  python resnet.py --model $MODEL --gpu $GPU --node $NODE --batch_size $BATCH_SIZE --num_epochs $EPOCH --seed $SEED

done



