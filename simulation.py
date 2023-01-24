from robot import ROBOT
from world import WORLD
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import constants as c

import time
import numpy as np
import constants as c


class SIMULATION:

    def __init__(self):

        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,c.GRAVITY)

        self.world = WORLD()
        self.robot = ROBOT()

    def Run(self):
        
        for i in range(c.STEPS):
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act(i)
            
            time.sleep(c.SLEEP_TIME)
    
    def __del__(self):
        p.disconnect()

