# CIS 630 Experiment: Comparison Hardware Configuration  and Deployment Model

This is the source code that I used in the CIS 630 project.

The data can be downloaded from ``https://www.image-net.org/``. After that, the training and development should be placed in two folders:

```
data/tiny/train/
data/tiny/dev/
data/tiny/test/
```
In each folder of these folders, there should be multiple subfolders, each of them contains images of a single image class. (This is a very common way to oraganize data in Computer Vision).

## Requirement

Hardware: Nvidia RTX 2080Ti

OS: Ubuntu 18.04

Software: Python3, Pytorch 1.6.0 , Pytorch Lightning. PyTorch Lighting does not seem to work properly wwith newer PyTorch. So please stick to PyTorch 1.6.0


## Installation

This will install the python environment for PyTorch. You might need to install CUDA driver and Nvidia Docker 2 if this settup does not work on your distro.


```
./setup.sh
./create_docker.sh
```


## Run the experiment

The experiment result is automatically uploaded to comet.ml. You should edit the Comet API key according to your API key.

The experiment set up should be configured in advance in ``run.sh``. You can configure the number of nodes, number of GPUs, batch size, epoch, model size.


And make sure, to change the hostname of the master node, and the worker ndoes that you run on accordingly,

To run the experiment, you should run this on all nodes.
```
./run.sh
```

## Credits

The source code is developed from the ResNet version of https://github.com/Stevellen/ResNet-Lightning



