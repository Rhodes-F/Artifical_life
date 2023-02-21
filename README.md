## Assignment 7

This project is part of CS 396-Artificial life at Northwestern Universiy. It began as a Ludobots project which is a reddit course that can be found [here](https://www.reddit.com/r/ludobots/) and uses pyrosim physics simulator to make the world environment and determine the interactions in the world. 

This assignment was to create a 3D  creature which I have done. Green boxes denote sensors and blue denotes sensorless boxes. 


Inorder to run this code first please clone the repository and enter the assignment7 branch. Then run main.py which will install the requirements and then run the search algorithm. The current search is set to run for 1 generation with a population size of 1 and have a maximum number of links of 10 with a max size being 1 and a min being .01 but this can be reconfigured in constants.py

For this assignment, the most challenging part was generating a body in 3 dimensions which randomly branched in all directions. The way that this was accomplished was by first making a single root node. This node was then used as a parent node and children were added in random directions. Each direction was weighted evenly. Each of these nodes coudl also have either 1, 2 or 3 children however the probability of having 1 child was much larger than either 2 or three. an example two dimensional body can be seen below. 


