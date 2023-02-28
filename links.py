import numpy as np
import pyrosim.pyrosim as pyrosim
import random
import constants as c

class Joint:
    def __init__(self, name, parent, child, type, pos, jointAxis, prev_dir,dir):
        self.name = name
        self.parent = parent
        self.child = child
        self.type = type
        self.position = pos
        self.jointAxis = jointAxis
        self.prev_dir = prev_dir
        self.dir = dir

class Cube:
    def __init__(self, name, pos, size, color_name, rgb):
        self.name = name
        self.pos = pos
        self.size = size
        self.color_name = color_name
        self.rgb = rgb
        

class Links: 



    def __init__(self, seed = None):
        self.weights = np.random.rand(100,100)*2-1
        self.sensors = []
        self.joints = []
        self.nodes = []
        self.cubes_to_send = []
        self.joints_to_send = []
        self.seed = seed
        self.myID = 1
        random.seed(self.seed)
        np.random.seed(self.seed)
        self.Create_Body()


    def get_sensor(self):
        return self.sensors
    def get_joint(self):
        return self.joints
    def get_node(self):
        return self.nodes

    def get_joints_to_send(self):
        return self.joints_to_send
    def get_cubes_to_send(self):
        return self.cubes_to_send

    def Mutate(self):
        row1 = random.randint(0,c.numSensorNeurons-1)
        col1 = random.randint(0,c.numMotorNeurons-1)
        self.weights[row1, col1] = random.random()*2-1
  

    def Create_Body(self):
        start_heigth= random.random()*c.MAX_SIZE+c.MIN_SIZE
        start_y = random.random()*c.MAX_SIZE+c.MIN_SIZE
        start_x = random.random()*c.MAX_SIZE+c.MIN_SIZE
        # pyrosim.Start_URDF("body.urdf")

        color_name = "Blue"
        rgb = [0,0,1]
        if random.randint(0,1) == 1:
            self.sensors.append("0")
            color_name = "Green"
            rgb = [0,1,0]

        links = random.randint(1,c.NUM_LINKS)
        self.cubes_to_send.append(Cube("0", [0,0,start_heigth/2], [start_x,start_y,start_heigth], color_name, rgb))
        self.nodes.append([0,start_x, start_y, start_heigth,[0,0,0]])

        for i in range(10):
            self.make_node()

        # return self.joints_to_send, self.cubes_to_send


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
        # random.seed(self.seed)
        # np.random.seed(self.seed)

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

        self.cubes_to_send.append(Cube(str(name+1),self.mult_some(dir,[length, width, height]),[length, width, height], 
                                       color_name, rgb))

        self.joints_to_send.append(Joint(joint,str(name),str(name+1),"revolute", [pos[0], pos[1],pos[2]],self.joint_axs(dir),node[4],dir))

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
        
l = Links(0)
# joints, cubes = l.Create_Body()

# for joint in joints:
#     print(joint.name, joint.parent, joint.child, joint.type, joint.position, joint.jointAxis)

# for cube in cubes:
#     print(cube.name, cube.pos, cube.size, cube.color_name, cube.rgb)

# print(l.get_joint())
# print(l.get_node())
# print(l.get_sensor())


