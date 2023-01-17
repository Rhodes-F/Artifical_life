import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy
from numpy import pi
import random
import matplotlib.pyplot

amplitude_L, frequency_L, phaseOffset_L = pi/4, 10, pi/2
amplitude_R, frequency_R, phaseOffset_R = pi/4, 10, pi/2
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
# p.loadSDF("world.sdf")
pyrosim.Prepare_To_Simulate(robotId)
backLegSensorValues = numpy.zeros(1000)
frontLegSensorValues = numpy.zeros(1000)
targetAngles_L = numpy.sin(phaseOffset_L+numpy.linspace(0, frequency_L*2*pi, 1000))*amplitude_L
targetAngles_R = numpy.sin(phaseOffset_R+numpy.linspace(0, frequency_R*2*pi, 1000))*amplitude_R
for i in range(1000):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotId,
        jointName = b'Torso_BackLeg',
        controlMode = p.POSITION_CONTROL,
        targetPosition = targetAngles_L[i],
        maxForce = 25)
    pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotId,
        jointName = b'Torso_FrontLeg',
        controlMode = p.POSITION_CONTROL,
        targetPosition =  targetAngles_R[i],
        maxForce = 25)
    time.sleep(1./100.)
    # print(i)
numpy.save("data/backLegSensorValues", backLegSensorValues)
numpy.save("data/frontLegSensorValues", frontLegSensorValues)
# numpy.save("data/targetAngles", targetAngles)
p.disconnect()