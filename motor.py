import constants as c
import numpy as np
import pyrosim.pyrosim as pyrosim
import pybullet as p

class MOTOR:

    def __init__(self, jointName):
        self.jointName = jointName
        self.Prepare_To_Act()

    def Prepare_To_Act(self):
        self.amplitude = c.AMPLITUDE
        self.offset = c.OFFSET
        self.frequency = c.FREQUENCY
        # if (self.jointName == b"Torso_FrontLeg"): self.frequency = c.FREQUENCY/2

        targetX = np.linspace(0, 2*np.pi, c.STEPS)
        self.motorValues = self.amplitude*np.sin(self.frequency*targetX + self.offset)

    def Set_Value(self,desiredAngle, robotId):
        pyrosim.Set_Motor_For_Joint(
            bodyIndex = robotId,
            jointName = self.jointName,
            controlMode = p.POSITION_CONTROL,
            targetPosition = desiredAngle,
            maxForce = c.MAXFORCE)

    def Save_Values(self):
        filename = "data/" + self.jointName + "MotorValues.npy"
        np.save(filename, self.motorValues)