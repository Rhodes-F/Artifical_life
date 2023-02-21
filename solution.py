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
        self.nodes = []

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
        start_x = random.random()*c.MAX_SIZE+c.MIN_SIZE
        pyrosim.Start_URDF("body.urdf")

        color_name = "Blue"
        rgb = [0,0,1]
        if random.randint(0,1) == 1:
            self.sensors.append("0")
            color_name = "Green"
            rgb = [0,1,0]
        pyrosim.Send_Cube(name="0", pos=[0, 0, start_heigth/2] , 
        size=[start_x, start_y, start_heigth ], color_name=color_name, rgb=rgb)
        
        links = random.randint(1,c.NUM_LINKS)
        self.nodes.append([0,start_x, start_y, start_heigth,[0,0,0]])

        for i in range(10):
            self.make_node()

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

        pyrosim.End()

    def make_node(self):
        node  = self.nodes.pop()
        name = node[0]

        color_name = "Blue"
        rgb = [0,0,1]
        length, width, height = random.random()*c.MAX_SIZE+c.MIN_SIZE,random.random()*c.MAX_SIZE+c.MIN_SIZE,random.random()*c.MAX_SIZE+c.MIN_SIZE
        if random.randint(0,1) == 1:
            self.sensors.append(str(name+1))
            color_name = "Green"   
            rgb = [0,1,0]
        joint = str(name)+"_"+str(name+1)
        self.joints.append(joint)

        dir_pick = random.randint(0,2)
        if dir_pick == 1:
            dir = [0,.5,0]
            pos = self.multiply(self.add(node[4],dir),node[2])
        elif dir_pick == 2:
            dir = [.5,0,0]
            pos = self.multiply(self.add(node[4],dir),node[1])
        else:
            dir = [0,0,.5]
            pos = self.multiply(self.add(node[4],dir),node[3])


        pyrosim.Send_Joint(
            name = joint, 
            parent= str(name), 
            child = str(name+1), 
            type = "revolute", 
            position = [pos[0], pos[1],pos[2]],jointAxis = self.joint_axs(dir))
        pyrosim.Send_Cube(
            name=str(name+1), 
            pos= self.mult_some(dir,[length, width, height]),
            size=[length, width, height], 
            color_name=color_name, rgb=rgb)

        self.nodes.append([name+1,length, width, height,dir])



    def add(self,a,b):
        return [a[0]+b[0],a[1]+b[1],a[2]+b[2]]

    def multiply(self,a,b):
        return [a[0]*b,a[1]*b,a[2]*b]

    def mult_some(self,a,b):
        return [a[0]*b[0],a[1]*b[1],a[2]*b[2]]

    def joint_axs(self,a):
        if a == [.5,0,0]:
            return "0 1 0"
        else:
            return "1 0 0"