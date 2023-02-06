import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import random
import time
import constants as c

class SOLUTION:

    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID
        self.weights = np.random.rand(c.NUM_SENSOR_NEURONS,c.NUM_MOTOR_NEURONS)*2-1

    def Start_Simulation(self, directOrGUI):
        self.Create_Body()
        self.Create_Brain()
        systemCommand = "python3 simulate.py " + directOrGUI + " " + str(self.myID) + " 2&>1 &"
        os.system(systemCommand)

    def Wait_For_Simulation_To_End(self):
        fitnessFileName = "fitness" + str(self.myID) + ".txt"
        while not os.path.exists(fitnessFileName):
            time.sleep(0.01)

        file = open(fitnessFileName, "r")
        self.fitness = float(file.read())
        file.close()
        # print(self.fitness)
        os.system("rm " + fitnessFileName)
    
    def Mutate(self):
        row1 = random.randint(0,c.NUM_SENSOR_NEURONS-1)
        col1 = random.randint(0,c.NUM_MOTOR_NEURONS-1)
        self.weights[row1, col1] = random.random()*2-1

    def Set_ID(self, newID):
        self.myID = newID

    def Get_Fitness(self):
        return self.fitness  

    @(staticmethod)
    def Create_World():
        # length, width, height = 1, 1, 1
        pyrosim.Start_SDF("world.sdf")
        # pyrosim.Send_Cube(name="Box", pos=[2, 2, 0.5] , size=[length, width, height])
        pyrosim.End()   

    @staticmethod
    def Create_Body():
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1] , size=[1, 1, 1])
        
        # Back leg
        pyrosim.Send_Joint(name = "Torso_BackLeg", parent= "Torso", child = "BackLeg", type = "revolute", position = [0, -0.5, 1], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="BackLeg", pos=[0, -0.5, 0] , size=[0.2, 1, 0.2])
        pyrosim.Send_Joint(name = "BackLeg_LowerBackLeg", parent= "BackLeg", child = "LowerBackLeg", type = "revolute", position = [0, -1, 0], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="LowerBackLeg", pos=[0, 0, -0.5] , size=[0.2, 0.2, 1])

        # Front leg
        pyrosim.Send_Joint(name = "Torso_FrontLeg", parent= "Torso", child = "FrontLeg", type = "revolute", position = [0, 0.5, 1], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="FrontLeg", pos=[0, 0.5, 0] , size=[0.2, 1, 0.2])
        pyrosim.Send_Joint(name = "FrontLeg_LowerFrontLeg", parent= "FrontLeg", child = "LowerFrontLeg", type = "revolute", position = [0, 1, 0], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="LowerFrontLeg", pos=[0, 0, -0.5] , size=[0.2, 0.2, 1])

        # Right leg
        pyrosim.Send_Joint(name = "Torso_RightLeg", parent= "Torso", child = "RightLeg", type = "revolute", position = [0.5, 0, 1], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="RightLeg", pos=[0.5, 0, 0] , size=[1, 0.2, 0.2])
        pyrosim.Send_Joint(name = "RightLeg_LowerRightLeg", parent= "RightLeg", child = "LowerRightLeg", type = "revolute", position = [1, 0, 0], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="LowerRightLeg", pos=[0, 0, -0.5] , size=[0.2, 0.2, 1])

        # Left leg
        pyrosim.Send_Joint(name = "Torso_LeftLeg", parent= "Torso", child = "LeftLeg", type = "revolute", position = [-0.5, 0, 1], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="LeftLeg", pos=[-0.5, 0, 0] , size=[1, 0.2, 0.2])
        pyrosim.Send_Joint(name = "LeftLeg_LowerLeftLeg", parent= "LeftLeg", child = "LowerLeftLeg", type = "revolute", position = [-1, 0, 0], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="LowerLeftLeg", pos=[0, 0, -0.5] , size=[0.2, 0.2, 1])

        pyrosim.End()
          
    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        sensorLinkNames = ["LowerBackLeg", "LowerFrontLeg", "LowerLeftLeg", "LowerRightLeg"]
        motorJointNames = ["Torso_BackLeg", "Torso_FrontLeg", "Torso_LeftLeg", "Torso_RightLeg", "BackLeg_LowerBackLeg", "FrontLeg_LowerFrontLeg", "LeftLeg_LowerLeftLeg", "RightLeg_LowerRightLeg"]
        for i in range(c.NUM_SENSOR_NEURONS):
            pyrosim.Send_Sensor_Neuron(name = i , linkName = sensorLinkNames[i])

        for j in range(c.NUM_MOTOR_NEURONS):
            pyrosim.Send_Motor_Neuron(name = j+c.NUM_SENSOR_NEURONS, jointName = motorJointNames[j])

        for currentRow in range(c.NUM_SENSOR_NEURONS):
            for currentColumn in range(c.NUM_MOTOR_NEURONS):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow,
                                    targetNeuronName = currentColumn+c.NUM_SENSOR_NEURONS, 
                                    weight = self.weights[currentRow][currentColumn])
        pyrosim.End()