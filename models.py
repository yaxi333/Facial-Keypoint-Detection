## TODO: define the convolutional neural network architecture

import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
# can use the below import should you choose to initialize the weights of your Net
import torch.nn.init as I


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        
        ## TODO: Define all the layers of this CNN, the only requirements are:
        ## 1. This network takes in a square (same width and height), grayscale image as input
        ## 2. It ends with a linear layer that represents the keypoints
        ## it's suggested that you make this last layer output 136 values, 2 for each of the 68 keypoint (x, y) pairs

        
        # As an example, you've been given a convolutional layer, which you may (but don't have to) change:
        # 1 input image channel (grayscale), 32 output channels/feature maps, 5x5 square convolution kernel

        ## Note that among the layers to add, consider including:
        # maxpooling layers, multiple conv layers, fully-connected layers, and other layers (such as dropout or batch normalization) to avoid overfitting
        # Input 1*224*224
        self.conv1 = nn.Conv2d(1, 32, 5) # Output (32, 220, 220)
        self.pool = nn. MaxPool2d(2,2)  # Output (32, 110, 110)
        self.drop1 = nn.Dropout(p=0.1)
        
        self.conv2 = nn.Conv2d(32, 64, 3) # Output (64, 108, 108) # After pool, output (64, 54, 54)
        self.drop2 = nn.Dropout(p=0.2)
        
        self.conv3 = nn.Conv2d(64, 128, 3) # Output (128, 52, 52) # After pool, output (128, 26, 26)
        self.drop3 = nn.Dropout(p=0.3)
        
                
        self.conv4 = nn.Conv2d(128, 256, 3)# Output (256, 24, 24)# Maxpooled Output = (256, 12, 12)
        self.drop4 = nn.Dropout(p=0.4)        
        
        
        self.conv5 = nn.Conv2d(256, 512, 3)# Output = (512, 10, 10)# Maxpooled Output = (512, 5, 5)
        self.drop5 = nn.Dropout(p=0.4)

        self.fc6 = nn.Linear(512*5*5, 4980)
        self.drop6 = nn.Dropout(p=0.4)
        
        self.fc7 = nn.Linear(4980, 2560)
        self.drop7 = nn.Dropout(p=0.4)
        
        self.fc8 = nn.Linear(2560, 1280)
        self.drop8 = nn.Dropout(p=0.4)

        self.fc9 = nn.Linear(1280, 136)
        
        

        
    def forward(self, x):
        ## TODO: Define the feedforward behavior of this model
        ## x is the input image and, as an example, here you may choose to include a pool/conv step:
        x = self.drop1(self.pool(F.relu(self.conv1(x))))
        x = self.drop2(self.pool(F.relu(self.conv2(x))))
        x = self.drop3(self.pool(F.relu(self.conv3(x))))
        x = self.drop4(self.pool(F.relu(self.conv4(x))))
        x = self.drop5(self.pool(F.relu(self.conv5(x))))
        x = x.view(x.size(0), -1) # 常出现在分类器之前，将前面多维度的tensor展平成一维，因为nn.Linear()要求输入输出都是一维
                          # 转换为 x.size(0)行的 size， view 用来reshape， -1 表示自动计算列数
        x = self.drop6(F.relu(self.fc6(x)))
        x = self.drop7(F.relu(self.fc7(x)))
        x = self.drop8(F.relu(self.fc8(x)))
        x = self.fc9(x)
        
        # a modified x, having gone through all the layers of your model, should be returned
        return x
