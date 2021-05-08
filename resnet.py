import sys
import warnings
from pathlib import Path
from argparse import ArgumentParser

warnings.filterwarnings('ignore')

# torch and lightning imports
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models
from torch.optim import SGD, Adam
from torchvision import transforms
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader
import pytorch_lightning as ptl
from pytorch_lightning import loggers as ptl_loggers
from constant import DATASETS


# Here we define a new class to turn the ResNet model that we want to use as a feature extractor
# into a pytorch-lightning module so that we can take advantage of lightning's Trainer object.
# We aim to make it a little more general by allowing users to define the number of prediction classes.
class ResNetClassifier(ptl.LightningModule):
    def __init__(self, num_classes, resnet_version,
                 train_path, vld_path, test_path=None,
                 optimizer='adam', lr=1e-3, batch_size=256, transfer=False):
        super(ResNetClassifier, self).__init__()
        self.num_classes = num_classes
        self.batch_size = batch_size

        self.__dict__.update(locals())
        resnets = {
            18: models.resnet18, 34: models.resnet34,
            50: models.resnet50, 101: models.resnet101,
            152: models.resnet152
        }
        optimizers = {'adam': Adam, 'sgd': SGD}
        self.optimizer = optimizers[optimizer]
        # Using a pretrained ResNet backbone
        self.resnet_model = resnets[resnet_version](pretrained=False)
        # Replace old FC layer with Identity so we can train our own
        linear_size = list(self.resnet_model.children())[-1].in_features
        # replace final layer for fine tuning
        self.resnet_model.fc = nn.Linear(linear_size, num_classes)

        if transfer:
            for child in list(self.resnet_model.children())[:-1]:
                for param in child.parameters():
                    param.requires_grad = False

    def forward(self, X):
        X = self.resnet_model(X)
        return F.softmax(X, dim=1)

    def configure_optimizers(self):
        return Adam(self.parameters(), lr=self.lr)

    def train_dataloader(self):
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.RandomHorizontalFlip(0.3),
            transforms.RandomVerticalFlip(0.3),
            transforms.RandomApply([
                transforms.RandomRotation(180)
            ]),
            transforms.ToTensor(),
            transforms.Normalize((0.48232,), (0.23051,))
        ])
        pneumonia_train = ImageFolder(self.train_path, transform=transform)
        return DataLoader(pneumonia_train, batch_size=self.batch_size, shuffle=True,
                          num_workers=32, pin_memory=True)

    def training_step(self, batch, batch_idx):
        x, y = batch
        preds = self(x)
        y = F.one_hot(y, num_classes=self.num_classes).type(torch.FloatTensor).to(x.device)

        loss = F.binary_cross_entropy(preds, y)
        acc = (torch.argmax(y, 1) == torch.argmax(preds, 1)).type(torch.FloatTensor)
        acc = acc.mean()
        return {'train_loss': loss, 'train_acc': acc}

    def training_epoch_end(self, outputs) -> None:
        avg_loss = torch.stack([x['train_loss'].detach() for x in outputs]).mean()
        avg_acc = torch.stack([x['train_acc'].detach() for x in outputs]).mean()

        tensorboard_logs = {'train_loss': avg_loss, 'train_acc': avg_acc}
        return {'train_loss': avg_loss, 'train_acc': avg_acc, 'log': tensorboard_logs}

    def val_dataloader(self):
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize((0.48232,), (0.23051,))
        ])

        pneumonia_vld = ImageFolder(self.vld_path, transform=transform)

        return DataLoader(pneumonia_vld, batch_size=self.batch_size, shuffle=False,
                          num_workers=32, pin_memory=True)

    def validation_step(self, batch, batch_idx):
        x, y = batch
        preds = self(x)
        y = F.one_hot(y, num_classes=self.num_classes).type(torch.FloatTensor).to(x.device)
        loss = F.binary_cross_entropy(preds, y)
        acc = (torch.argmax(y, 1) == torch.argmax(preds, 1)).type(torch.FloatTensor)
        acc = acc.mean()
        return {'val_loss': loss, 'val_acc': acc}

    def validation_epoch_end(self, outputs):
        avg_loss = torch.stack([x['val_loss'] for x in outputs]).mean()
        avg_acc = torch.stack([x['val_acc'] for x in outputs]).mean()

        tensorboard_logs = {'val_loss': avg_loss, 'val_acc': avg_acc}
        return {'val_loss': avg_loss, 'val_acc': avg_acc, 'log': tensorboard_logs}

    def test_dataloader(self):
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize((0.48232,), (0.23051,))
        ])

        pneumonia_vld = ImageFolder(self.test_path, transform=transform)

        return DataLoader(pneumonia_vld, batch_size=self.batch_size, shuffle=False,
                          num_workers=32, pin_memory=True)

    def test_step(self, batch, batch_idx):
        x, y = batch
        preds = self(x)
        y = F.one_hot(y, num_classes=self.num_classes).type(torch.FloatTensor).to(x.device)

        loss = F.binary_cross_entropy(preds, y)
        acc = (torch.argmax(y, 1) == torch.argmax(preds, 1)).type(torch.FloatTensor)
        acc = acc.mean()
        return {'test_loss': loss, 'test_acc': acc}

    def test_epoch_end(self, outputs):
        avg_loss = torch.stack([x['test_loss'] for x in outputs]).mean()
        avg_acc = torch.stack([x['test_acc'] for x in outputs]).mean()

        tensorboard_logs = {'test_loss': avg_loss, 'test_acc': avg_acc}
        return {'test_loss': avg_loss, 'test_acc': avg_acc, 'log': tensorboard_logs}


if __name__ == '__main__':
    parser = ArgumentParser()
    # Required arguments
    parser.add_argument('--model', default=18, choices=[18, 34, 50, 101, 152], type=int)
    parser.add_argument('--num_classes', default=18, help='Number of classes to be learned.', type=int)
    parser.add_argument('--num_epochs', default=20, help='Number of Epochs to Run.', type=int)
    parser.add_argument('--dataset', default='tiny', choices=['mini', 'tiny', 'debug'])
    # Optional arguments
    parser.add_argument('-o', '--optimizer', help='PyTorch optimizer to use. Defaults to adam.', default='adam')
    parser.add_argument('-lr', '--learning_rate', help='Adjust learning rate of optimizer.', type=float, default=1e-3)
    parser.add_argument('-b', '--batch_size', help='Manually determine batch size. Defaults to 16.',
                        type=int, default=256)
    parser.add_argument('-tr', '--transfer',
                        help='Determine whether to use pretrained model or train from scratch. Defaults to True.',
                        action='store_true')
    parser.add_argument('-s', '--save_path', help='Path to save model trained model checkpoint.')
    parser.add_argument('-g', '--gpus', help='Enables GPU acceleration.', type=int, default=1)
    args = parser.parse_args()

    # # Instantiate Model

    dataset_constant = DATASETS[args.dataset]

    model = ResNetClassifier(dataset_constant['class'],
                             args.model,
                             dataset_constant['train'],
                             dataset_constant['dev'],
                             dataset_constant['test'],
                             args.optimizer,
                             args.learning_rate,
                             args.batch_size)

    gpus = 2
    nodes = 1

    tf_logger = ptl_loggers.TensorBoardLogger(f'logs/nodes-{nodes}.gpu-{gpus}/')

    trainer = ptl.Trainer(
        gpus=gpus,
        num_nodes=nodes,
        accelerator='ddp',
        num_sanity_val_steps=0,
        logger=tf_logger
    )
    trainer.fit(model)
    # Save trained model
    save_path = (args.save_path if args.save_path is not None else '/') + 'trained_model.ckpt'
    # trainer.save_checkpoint(save_path)
