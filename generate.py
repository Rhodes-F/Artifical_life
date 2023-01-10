import pyrosim.pyrosim as pyrosim

def Create_World():
    pyrosim.Start_SDF("world.sdf")
    length = 1
    width = 1
    height = 1

    x = -1.6   
    y = 0
    z = .5
    pyrosim.Send_Cube(name="box", pos=[x,y,z] , size=[length,width,height])

    pyrosim.End()

def Create_Robot():
    pyrosim.Start_URDF("body.urdf")


    pyrosim.Send_Cube(name="Torso", pos=[0,0,1.5] , size=[1,1,1])
    pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [-.5,0,1])
    pyrosim.Send_Cube(name="BackLeg", pos=[-.5,0,-.5] , size=[1,1,1])
    pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [.5,0,1])
    pyrosim.Send_Cube(name="FrontLeg", pos=[.5,0,-.5] , size=[1,1,1])

    pyrosim.End()

# Create_World()
Create_Robot()