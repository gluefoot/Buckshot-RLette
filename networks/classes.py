import torch
import torch.nn as nn
import numpy as np
from PIL import Image
import scipy
import torchvision.tv_tensors


FLAT_SIZE = 184832  # single-image flat dimension, apparently also the convolutions of the triple-image flattened? Anyway, == 32*76*76, shape of convolution outputs
ACTION_SIZE = 5  # UDLR + "select", for the case of Buckshot Roulette

device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)
print(f"Using {device} device")

class Encoder(nn.Module):

    def __init__(self):
        super(Encoder, self).__init__()
        # In original paper, 3 consecutive images is 1 observation
        # each image is 3-channel, 84x84
        self.convolutions = nn.Sequential(
            nn.Conv2d(9,32,kernel_size=3),  # 84x84 -> 82x82
            nn.ReLU(),
            nn.Conv2d(32,32,kernel_size=3),  # 82x82 -> 80x80
            nn.ReLU(),
            nn.Conv2d(32,32,kernel_size=3),  # 80x80 -> 78x78
            nn.ReLU(),
            nn.Conv2d(32,32,kernel_size=3),  # 78x78 -> 76x76
            nn.ReLU(),
        )

        self.fc = nn.Sequential(
            nn.Linear(FLAT_SIZE,FLAT_SIZE),  # flattening size for 3 channels initial input, 2^9 * 19^2 = 32*76*76
            nn.LayerNorm(FLAT_SIZE),
            nn.Tanh()
        )

    def forward(self, x):
        interim = self.convolutions(x)
        interim = interim.flatten()
        x_ = self.fc(interim)
        return x_
    
class Decoder(nn.Module):

    def __init__(self):
        super(Decoder, self).__init__()
        # In original paper, 3 consecutive images is 1 observation
        # each image is 3-channel, 84x84
        self.fc = nn.Sequential(
            nn.Linear(FLAT_SIZE,FLAT_SIZE),  # flattening size for 3 channels initial input, 2^9 * 19^2
            nn.ReLU()
        )

        self.deconvolutions = nn.Sequential(
            nn.ConvTranspose2d(32,32,(3,3)),
            nn.ReLU(),
            nn.ConvTranspose2d(32,32,(3,3)),
            nn.ReLU(),
            nn.ConvTranspose2d(32,32,(3,3)),
            nn.ReLU(),
            nn.ConvTranspose2d(32,9,(3,3)),
            nn.Sigmoid()
        )

    def forward(self, x):
        interim = self.fc(x)
        interim = torch.reshape(interim, (32, 76, 76))
        x_ = self.deconvolutions(interim)
        return x_

class Actor(nn.Module):

    def __init__(self):
        super(Actor, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(FLAT_SIZE, 1024),
            nn.ReLU(),
            nn.Linear(1024,1024),
            nn.ReLU(),
            nn.Linear(1024,ACTION_SIZE),
            nn.Tanh()
        )

    def forward(self, x):
        return self.fc(x)

class Critic(nn.Module):

    def __init__(self):
        super(Critic, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(FLAT_SIZE, 1024),
            nn.ReLU(),
            nn.Linear(1024,1024),
            nn.ReLU(),
            nn.Linear(1024,1)
        )

    def forward(self, x):
        return self.fc(x)
    
class Ensemble(nn.Module):

    def __init__(self):
        super(Critic, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(FLAT_SIZE, 512),
            nn.ReLU(),
            nn.Linear(512,512),
            nn.ReLU(),
            nn.Linear(512,FLAT_SIZE)
        )

    def forward(self, x):
        return self.fc(x)

if __name__ == "__main__":
    img = Image.open("Buckshot-RLette/testimg.png")
    singleton = torchvision.tv_tensors.Image(img, dtype=torch.float)
    data = torch.cat((singleton, singleton, singleton)).unsqueeze(0)
    encoder_net = Encoder()
    x = encoder_net.forward(data)
    decoder_net = Decoder()
    data_ = decoder_net.forward(x)
    
