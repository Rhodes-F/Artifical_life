import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import random
import time
import constants as c

class SOLUTION:

    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID
        self.weights = np.random.rand(c.numSensorNeurons,c.numMotorNeurons)*2-1

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
        row1 = random.randint(0,c.numSensorNeurons-1)
        col1 = random.randint(0,c.numMotorNeurons-1)
        self.weights[row1, col1] = random.random()*2-1

    def Set_ID(self, newID):
        self.myID = newID

    def Get_Fitness(self):
        return self.fitness  

    # def Create_World(self):
        # length, width, height = 1, 1, 1
        # pyrosim.Start_SDF("world.sdf")
        # pyrosim.Send_Cube(name="Box", pos=[2, 2, 0.5] , size=[length, width, height])
        # pyrosim.End()     

    def Create_Body(self):
        length, width, height = 1, 1, 1
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 3] , size=[1, 1, 1])
            
        pyrosim.Send_Joint(name = "Torso_Leg", parent= "Torso", child = "Leg", type = "revolute", position = [0, 0, 2.5],jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="Leg", pos=[0, 0, -1] , size=[.3, .3, 2])

        pyrosim.Send_Joint(name = "Torso_FrontArm", parent= "Torso", child = "FrontArm", type = "revolute", position = [0.5, 0, 3],jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="FrontArm", pos=[0, 0, -0.5] , size=[.3, .3, 1])

        pyrosim.Send_Joint(name = "Torso_BackArm", parent= "Torso", child = "BackArm", type = "revolute", position = [-0.5, 0, 3],jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="BackArm", pos=[0, 0, -0.5] , size=[.3, .3, 1])

        pyrosim.Send_Joint(name = "Torso_RightArm", parent= "Torso", child = "RightArm", type = "revolute", position = [0,-.5, 3],jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="RightArm", pos=[0, 0, -0.5] , size=[.3, .3, 1])

        pyrosim.Send_Joint(name = "Torso_LeftArm", parent= "Torso", child = "LeftArm", type = "revolute", position = [0, .5, 3],jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="LeftArm", pos=[0, 0, -0.5] , size=[.3, .3, 1])

        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        # Create sensor neurons
        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "Leg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontArm")
        pyrosim.Send_Sensor_Neuron(name = 3 , linkName = "BackArm")
        pyrosim.Send_Sensor_Neuron(name = 4 , linkName = "RightArm")
        pyrosim.Send_Sensor_Neuron(name = 5 , linkName = "LeftArm")

        # Create motor neurons
        pyrosim.Send_Motor_Neuron(name = 6 , jointName = "Torso_Leg")
        pyrosim.Send_Motor_Neuron(name = 7 , jointName = "Torso_FrontArm")
        pyrosim.Send_Motor_Neuron(name = 8 , jointName = "Torso_BackArm")
        pyrosim.Send_Motor_Neuron(name = 9 , jointName = "Torso_RightArm")
        pyrosim.Send_Motor_Neuron(name = 10 , jointName = "Torso_LeftArm")

        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow,
                                    targetNeuronName = currentColumn+c.numSensorNeurons, 
                                    weight = self.weights[currentRow][currentColumn])
        pyrosim.End()