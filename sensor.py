import numpy as np
import constants as c
import pyrosim.pyrosim as pyrosim

class SENSOR:

    def __init__(self, linkName):
        self.linkName = linkName
        self.values = np.zeros(c.STEPS)
    
    def Get_Value(self, i):
        self.values[i] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
        if len(self.values)-1 == i:
            print(self.values)
            print(self.linkName)

    def Save_Values(self):
        filename = "data/" + self.linkName + "SensorValues.npy"
        np.save(filename, self.values)