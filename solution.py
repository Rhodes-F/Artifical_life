import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import random
import time
import constants as c

class SOLUTION:

    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID
        self.weights = np.random.rand(100,100)*2-1
        self.sensors = []
        self.joints = []

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
        start_heigth= random.random()*c.MAX_SIZE+c.MIN_SIZE
        start_y = random.random()*c.MAX_SIZE+c.MIN_SIZE
        pyrosim.Start_URDF("body.urdf")
        color_name = "Blue"
        rgb = [0,0,1]
        if random.randint(0,1) == 1:
            self.sensors.append("0")
            color_name = "Green"
            rgb = [0,1,0]
        pyrosim.Send_Cube(name="0", pos=[0, 0, start_heigth/2] , 
        size=[random.random()*c.MAX_SIZE+c.MIN_SIZE, start_y, start_heigth ], color_name=color_name, rgb=rgb)
        
        end_pos = start_y/2
        lasty = 0
        links = random.randint(1,c.NUM_LINKS)
        for i in range(links):
            color_name = "Blue"
            rgb = [0,0,1]
            length, width, height = random.random()*c.MAX_SIZE+c.MIN_SIZE,random.random()*c.MAX_SIZE+c.MIN_SIZE,random.random()*c.MAX_SIZE+c.MIN_SIZE
            if random.randint(0,1) == 1:
                self.sensors.append(str(i+1))
                color_name = "Green"   
                rgb = [0,1,0]
            joint = str(i)+"_"+str(i+1)
            self.joints.append(joint)
            pyrosim.Send_Joint(name = joint, parent= str(i), child = str(i+1), type = "revolute", position = [0, end_pos,height/2 - lasty/2],jointAxis = "1 0 0")
            pyrosim.Send_Cube(name=str(i+1), pos=[0, width/2, 0], size=[length, width, height], color_name=color_name, rgb=rgb)
            end_pos = width
            lasty = height

        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        for i in range(len(self.sensors)):
            pyrosim.Send_Sensor_Neuron(name = i, linkName = self.sensors[i])
    
        for i in range(len(self.joints)):
            pyrosim.Send_Motor_Neuron(name = i+len(self.sensors), jointName = self.joints[i])
        
        for i in range(len(self.sensors)):
            for j in range(len(self.joints)):
                pyrosim.Send_Synapse(sourceNeuronName = i,
                                    targetNeuronName = j+len(self.sensors), 
                                    weight = self.weights[i][j])      

        # for currentRow in range(c.numSensorNeurons):
        #     for currentColumn in range(c.numMotorNeurons):
        #         pyrosim.Send_Synapse(sourceNeuronName = currentRow,
        #                             targetNeuronName = currentColumn+c.numSensorNeurons, 
        #                             weight = self.weights[currentRow][currentColumn])
        pyrosim.End()