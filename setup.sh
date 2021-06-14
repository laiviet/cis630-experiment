#!/bin/bash

# Setup cuda

wget https://us.download.nvidia.com/XFree86/Linux-x86_64/460.67/NVIDIA-Linux-x86_64-460.67.run
chmod +x NVIDIA-Linux-x86_64-460.67.run
sudo ./NVIDIA-Linux-x86_64-460.67.run


# Setup conda
wget https://repo.anaconda.com/miniconda/Miniconda3-py39_4.9.2-Linux-x86_64.sh
chmod +x Miniconda3-py39_4.9.2-Linux-x86_64.sh
./Miniconda3-py39_4.9.2-Linux-x86_64.sh


source ~/.bashrc
export PATH=/users/laiviet/miniconda3/bin:$PATH

# Setup conda environment
conda create -n py39 python=3.9
conda activate py39
conda install pytorch==1.6.0 -c pytorch
conda install torchvision -c pytorch
pip install pytorch_lightning

# Download experiments

mkdir ~/resnet
cd ~/resnet


# Run experiments
