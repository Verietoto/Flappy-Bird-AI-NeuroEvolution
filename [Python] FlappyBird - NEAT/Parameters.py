"""Setting up every parameters of game"""

import numpy as np
import pygame
import copy
from multiprocessing import Process, Queue
import time
import sys
from itertools import permutations
from glob import glob

##Screen Dimension
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

## Horizontal Game Speed
velocity = 4

## Vertical Game Speed
GRAVITATION = 0.20

##Intiail Bird Position
BirdPosition = (160,250)

## Evolution Algorithm Parameters
POPULATINO_SIZE = 1500
MUTATION_RATE = 0.2
PARENTNUMBER = 10

# Neural Network Shape. 2 Input, 1 Layers with 16 neuron, 2 output
shape = (2, 16, 2)
