import pyrosim.pyrosim as pyrosim
import pybullet as p
from sensor import SENSOR
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
import constants as c

class ROBOT:

    def __init__(self, solutionID):
        
        self.solutionID = solutionID
        bodyFile = "body" + str(self.solutionID) + ".urdf"
        brainFile = "brain" + str(self.solutionID) + ".nndf"
        self.nn = NEURAL_NETWORK(brainFile)
        self.robotId = p.loadURDF(bodyFile)
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        bodyFile = "body" + str(self.solutionID) + ".urdf"
        brainFile = "brain" + str(self.solutionID) + ".nndf"
        self.nn = NEURAL_NETWORK(brainFile)
        self.robotId = p.loadURDF(bodyFile)
        os.system("rm " + brainFile)
        os.system("rm " + bodyFile)

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
                desiredAngle = self.nn.Get_Value_Of(neuronName) *c.motorJointRange
                self.motors[jointName.encode("utf-8")].Set_Value(desiredAngle, self.robotId)


    def Think(self):
        self.nn.Update()
        # self.nn.Print()

    def Get_Fitness(self):
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        basePosition = basePositionAndOrientation[0]
        xPosition = basePosition[0]
        tmpFileName = "tmp" + str(self.solutionID) + ".txt"
        fitnessFileName = "fitness" + str(self.solutionID) + ".txt"
        file = open(tmpFileName, "w")
        file.write(str(xPosition))
        file.close()
        os.system("mv " + tmpFileName + " " + fitnessFileName)


