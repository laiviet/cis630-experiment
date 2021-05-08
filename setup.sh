#!/bin/bash

# Setup cuda

#wget https://us.download.nvidia.com/XFree86/Linux-x86_64/460.67/NVIDIA-Linux-x86_64-460.67.run
#chmod +x NVIDIA-Linux-x86_64-460.67.run
#sudo ./NVIDIA-Linux-x86_64-460.67.run


# Setup conda
wget https://repo.anaconda.com/miniconda/Miniconda3-py39_4.9.2-Linux-x86_64.sh
chmod +x Miniconda3-py39_4.9.2-Linux-x86_64.sh
./Miniconda3-py39_4.9.2-Linux-x86_64.sh


source ~/.bashrc
export PATH=/users/laiviet/miniconda3/bin:$PATH

# Setup conda environment
conda create -n py37 python=3.7
conda activate py37
conda install pytorch -c pytorch
conda install torchvision -c pytorch
pip install pytorch_lightning
conda activate py37
# Download experiments

sudo /usr/local/etc/emulab/mkextrafs.pl projects/
sudo chown laiviet:cis630dnn-PG0 projects
cd projects
git clone https://github.com/laiviet/cis630-experiment.git
cd cis630-experiment
mkdir data
cd data
mkdir tiny
cd tiny
wget http://nlp.uoregon.edu/download/miniimagenet/tiny/train.zip
unzip train.zip
rm train.zip
wget http://nlp.uoregon.edu/download/miniimagenet/tiny/dev.zip
unzip dev.zip
rm dev.zip
wget http://nlp.uoregon.edu/download/miniimagenet/tiny/test.zip
unzip test.zip
rm test.zip


# Run experiments
