import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import random
import time
import constants as c
from links import Links





class SOLUTION:

    def __init__(self, nextAvailableID):
        self.seed = c.random_seed
        self.myID = nextAvailableID
        self.weights = np.random.rand(100,100)*2-1
        self.sensors = Links(self.seed).get_sensor()
        self.joints = Links(self.seed).get_joint()
        self.nodes = Links(self.seed).get_node()
        self.joints_to_send  = Links(self.seed).get_joints_to_send()
        self.cubes_to_send = Links(self.seed).get_cubes_to_send()
        random.seed(self.seed)
        np.random.seed(self.seed)

        self.links = Links(5)

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
        num = random.random()
        if num < 0.75:
            row1 = random.randint(0,c.numSensorNeurons-1)
            col1 = random.randint(0,c.numMotorNeurons-1)
            self.weights[row1, col1] = random.random()*2-1
        else:
            nums = [0,1,2]
            choice = random.choice(nums)
            if choice == 0:
                i = random.randint(0,len(self.cubes_to_send)-1)
                cube = self.cubes_to_send[i]
                if cube.name in self.sensors:
                    self.sensors.remove(cube.name)
                    self.cubes_to_send[i].color = "Blue"
                    self.cubes_to_send[i].rgb = [0,0,1]
                else:
                    self.sensors.append(cube.name)
                    self.cubes_to_send[i].color_name = "Green"
                    self.cubes_to_send[i].rgb = [0,1,0]
            elif choice ==1:
                i = random.randint(0,len(self.joints_to_send)-1)
                joint = self.joints_to_send[i]
                if joint.jointAxis == "0 1 0":
                    self.joints_to_send[i].jointAxis = "1 0 0"
                else:
                    self.joints_to_send[i].jointAxis = "0 1 0"
            elif choice ==2:
                i = random.randint(0,len(self.joints_to_send)-1)
                cube_change = self.joints_to_send[i].parent
                for cube in self.cubes_to_send:
                    if cube.name == cube_change:
                        prev_dir = self.joints_to_send[i].prev_dir
                        cube.size = self.mult_some(cube.size,[random.random()*2, random.random()*2, random.random()*2])
                        cube.pos = self.mult_some(cube.size,prev_dir)
                        dir = self.joints_to_send[i].dir
                        if dir ==[0,.5,0]:
                            pos = self.multiply(self.add(prev_dir,dir),cube.size[1])
                        elif dir == [.5,0,0]:
                            pos = self.multiply(self.add(prev_dir,dir),cube.size[0])
                        else:
                            pos = self.multiply(self.add(prev_dir,dir),cube.size[2])
                        
                        self.joints_to_send[i].pos = pos
                                        


                
    def add(self,a,b):
        return [a[0]+b[0],a[1]+b[1],a[2]+b[2]]

    def multiply(self,a,b):
        return [a[0]*float(b),a[1]*float(b),a[2]*float(b)]

    def mult_some(self,a,b):
        return [a[0]*b[0],a[1]*b[1],a[2]*b[2]]

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
        pyrosim.Start_URDF("body" + str(self.myID) + ".urdf")

        
        joints, cubes = self.joints_to_send, self.cubes_to_send

        for joint in joints:
            pyrosim.Send_Joint(name = joint.name, parent = joint.parent, child = joint.child, type = joint.type, position = joint.position, jointAxis = joint.jointAxis)
        for cube in cubes:
            pyrosim.Send_Cube(name = cube.name, pos = cube.pos, size = cube.size, color_name = cube.color_name, rgb = cube.rgb)
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

