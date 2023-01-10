import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("boxes.sdf")
l = 0
while l <5:
    j= 0
    while j <5:
        i=0
        length = 1
        width = 1
        height = 1
        while i <10:
            x = 0 + j
            y = 0 + l
            z = .5 + i
            pyrosim.Send_Cube(name="Boxes", pos=[x,y,z] , size=[length,width,height])
            length = .9 * length
            width = .9 * width
            height = .9 * height
            i = i + 1
        j+=1
    l+=1
pyrosim.End()