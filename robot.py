import pyrosim.pyrosim as pyrosim
import pybullet as p
from sensor import SENSOR
from motor import MOTOR

class ROBOT:

    def __init__(self):
        self.robotId = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
    
    def Prepare_To_Sense(self):
        self.sensors = {}

        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Sense(self, i):
        for sensor_name in self.sensors:
            self.sensors[sensor_name].Get_Value(i)

    def Prepare_To_Act(self):
        self.motors = {}

        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Act(self, i):
        for motor_name in self.motors:
            self.motors[motor_name].Set_Value(i, self.robotId)

    def Save_Values(self):
        for sensor_name in self.sensors:
            self.sensors[sensor_name].Save_Values()
        for motor_name in self.motors:
            self.motors[motor_name].Save_Values()