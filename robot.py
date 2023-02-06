import pyrosim.pyrosim as pyrosim
import pybullet as p
from sensor import SENSOR
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
import constants as c

class ROBOT:

    def __init__(self, solutionID):
        self.robotId = p.loadURDF("body.urdf")
        self.solutionID = solutionID
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()

        brainFile = "brain" + str(self.solutionID) + ".nndf"
        self.nn = NEURAL_NETWORK(brainFile)
        os.system("rm " + brainFile)

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

    def Act(self):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName)*c.MOTOR_JOINT_RANGE
                self.motors[jointName.encode("utf-8")].Set_Value(desiredAngle, self.robotId)

    def Think(self):
        self.nn.Update()
        # self.nn.Print()

    def Get_Fitness(self):
        stateOfLinkZero = p.getLinkState(self.robotId,0)
        positionOfLinkZero = stateOfLinkZero[0]
        xCoordOfLinkZero = positionOfLinkZero[0]
        tmpFileName = "tmp" + str(self.solutionID) + ".txt"
        fitnessFileName = "fitness" + str(self.solutionID) + ".txt"
        file = open(tmpFileName, "w")
        file.write(str(xCoordOfLinkZero))
        file.close()
        os.system("mv " + tmpFileName + " " + fitnessFileName)
