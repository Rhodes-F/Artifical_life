import numpy
from numpy import pi

amplitude_L, frequency_L, phaseOffset_L = pi/4, 10, pi/2
amplitude_R, frequency_R, phaseOffset_R = pi/4, 5, pi/2

import math

STEPS = 10000
GRAVITY = -9.8

AMPLITUDE = math.pi/4
FREQUENCY = 20
OFFSET = 0

MAXFORCE = 50

SLEEP_TIME = 0.005

NUM_GENERATIONS = 100

POPULATION_SIZE = 10


numSensorNeurons = 6
numMotorNeurons = 5

motorJointRange = .5

# assignment 6
NUM_LINKS = 10 
MAX_SIZE = 1 
MIN_SIZE = .01

random_seed = 13