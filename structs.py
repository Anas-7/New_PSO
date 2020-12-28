import random

class Node:
    def __init__(self,x,y):
        #All the attributes of Node Class
        self.ind = 0	#Node index
        self.x = x    #x co-ordinate
        self.y = y    #y co-ordinate
        self.eres = 2	#Residual Energy
        self.q = 0 	# random Q
        self.weight = 0		#T(i)
        self.indg=0		#Index of grey node(if it is grey)
        self.alive = True	#Node alive or dead
        self.ordInd = -1	#index of ordNodes nodes(if ordNodes node)
        self.einit=2   #initial energy of the node (in Joules)
        self.neighbours = [] #Array for neighbours
        self.cost = 0
        self.ord = True # true when node is ordinary, false when backbone
        self.bbInd = -1
    
radius = 80	#radius of each node
numNodes = 300	# Total Number of nodes present
N = 5 # Backnode black(number of nodes from neighbours to be selected as black)
nMax = 0 #initialisation of nMax -> maximum number of neighbour among all nodes

#Initialization of constants
E_init = 2
Efs = 10 * 1e-12 #Pico Joule/bit/m2
k = 1000 #bits
EDA = 5 * 1e-9 #nJ/bit/signal
Eelec = 50 * 1e-9 #nJ/bit
Eamp = 0.0013 * 1e-12 #PJ/bit/m4
d0 = 90 #m

#fitness function constants
alpha = 0.35
beta = 0.45
gamma = 0.2
wmin = 0.4

#Initialization of weights used for calculating T(i)
w1 = 0.3
w2 = 0.4
w3 = 0.3

cMax = 0 #cost max


#Remaining
# costs = []	# list to store the cost used in T(i)
#initial list to store the values of T(i)
# wt_T = [1.0 for x in range(numNodes)]
# ordNodes=[]		#initalise list for ordinary nodes(used in backbone repair)
# backbone_nodes=[]	#initalise list for backbone nodes
# ctr=0	#count of BLACK nodes
# ctrg=0	#count of GREY nodes