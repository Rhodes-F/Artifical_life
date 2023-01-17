import numpy
import matplotlib.pyplot


backLegSensorValues = numpy.load("data/backLegSensorValues.npy")
frontLegSensorValues = numpy.load("data/frontLegSensorValues.npy")
# targetAngles = numpy.load("data/targetAngles.npy")

matplotlib.pyplot.plot(backLegSensorValues,label = 'backLegSensorValues',linewidth=3)
matplotlib.pyplot.plot(frontLegSensorValues, label = 'frontLegSensorValues')
# matplotlib.pyplot.plot(targetAngles, label = 'targetAngles')

matplotlib.pyplot.legend(loc = 'upper right')
matplotlib.pyplot.show()