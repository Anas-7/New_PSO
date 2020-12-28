from structs import *
import random
import math
import collections
import operator
random.seed(11)
#intialisation of all nodes
def initNodes_rand(nodes):
	for i in range(numNodes):
		#Generating random co-ordinates for Nodes
		x = random.randint(0, 400)
		y = random.randint(0, 400)
		#making objects of Node Class
		n = Node(x, y)
		n.ind = i 	#index of node
		nodes.append(n)		#adding the node to a list
	
	for i in range(numNodes):	#for every node
		nodes = costNode(i, nodes) 	# cost(i) initialization
	for i in range(numNodes):	#for every node
		nodes = weight(i, nodes)	#calculating T(i) using cost
	
	#returning a list with all nodes initialised
	return nodes

	

#Assigning neighbours of all the nodes
def initNeighbours(nodes):
	global nMax
	for i in range(numNodes):
		#counting number of neighbour for every node
		count = 0
		for j in range(numNodes):
			#if the index of both nodes are different
			if i != j:
				#if the nodes are overlapping(are close enough)
				if ((nodes[i].x - nodes[j].x) ** 2 + (nodes[i].y - nodes[j].y) ** 2 < radius ** 2):
					count += 1
					#adding that node as a neighbour
					nodes[i].neighbours.append(nodes[j])
		#nMax is maximum number of neighbour among all nodes
		if count > nMax:
			nMax = count
	return nodes, nMax


#Calculating cost requied for T(i)
def costNode(i, nodes):
	global cMax
	#co-ordinates of nodes
	xi = nodes[i].x
	yi = nodes[i].y
	cost = 0	#initial cost
	for j in range(len(nodes[i].neighbours)):		#len -1 as last index is not a node(it's the count of no. of neighbours)\
		#using the formula given in the paper
		#calculating the cost

		#Calculating ETx(i) and adding it to list
		#𝐸𝑇𝑥(𝑖) denotes the energy cost of node 𝑖 in transmitting one bit of message
		dist = math.sqrt(((xi - nodes[i].neighbours[j].x) ** 2 + (yi - nodes[i].neighbours[j].y) ** 2))
		if(dist <= d0):
			eTemp = k * (Eelec + Efs * (dist ** 2))
		else:
			eTemp = k * (Eelec + Eamp * (dist ** 4))
		m = 46.357
		c = -9.642
		rssi = -m * math.log10(dist) + c
		nodes[i].q = (10 ** (rssi/10))/1000

		num = eTemp * E_init	#E_init->inital energy|numerator of cost formula
		denom = nodes[i].q * nodes[i].neighbours[j].eres   #denominator of cost formula
		assert(denom != 0)
		cost += math.sqrt(num / denom)	#calculaing cost
	
	nodes[i].cost = cost	#adding cost to a list
	#calculating maximum cost
	if cMax < cost:
		cMax = cost
	return nodes

#Calculating T(I)
def weight(i, nodes):
	if nodes[i].cost != 0:	#if cost is not 0
		#Calculating T(i) for the node
		T_temp = w1 * nodes[i].eres / E_init + w2 * len(nodes[i].neighbours) / nMax + w3 * cMax / nodes[i].cost
	else:
		T_temp = 0
	#adding T(i) value to its node
	nodes[i].weight = T_temp
	
	return nodes

#initial colour assigned to each node
col = [0 for x in range(numNodes)]
# 0 -> WHITE
# 1 -> BLACK
# 2 -> GREY


#FORMATION OF BACKBONE

#STEP 1 of Backbone Formation
#used in STEP 2 for getting the start index for backbone nodes
def step1( nodes):
	ind = 0		#index of black nodes
	maxWt = 0	#Storing the Maximum T(i) 
	for i in range(numNodes):	#for every value of T(i)	
		#calculating the maximum T(i)
		if nodes[i].weight	 > maxWt:
			ind = i   #storing index for black nodes
			maxWt = nodes[i].weight	
	#assigning black colour for that index
	col[ind] = 1
	return ind

#STEP 2 of Backbone Formation
def step2(nodes, stInd):
	queue = collections.deque()		#queue stores all the black nodes
	ctr2 = 0	#count of number of grtey nodes
	ctr = 0		#count of number of black nodes

	queue.append(nodes[stInd])	#adding the 1st node as black node(we get this value from STEP 1)
	while(len(queue) != 0):		#till all the nodes are not coloured black or grey
		
		#sorting the neighbours of the black node according to it's T(i) value
		nl = sorted(nodes[queue[0].ind].neighbours, key = operator.attrgetter("weight"), reverse = True)
		#nl.append(neighbours[queue[0].ind][-1])		#adding the neighbour with maximum T(i) in the list

		#storing the neighbours of the black node
		nodes[queue[0].ind].neighbours = nl

		#N is the number of nodes from neighbours that must be selected as black| Others are marked as grey
		nTemp = N
		
		#for the 1st element of the queue(black nodes list)
		for i in range(len(nodes[queue[0].ind].neighbours)):
			if col[nodes[queue[0].ind].neighbours[i].ind] == 0:	#if the neighbour of that node is white
				if nTemp > 0:	#for the first nTemp elements assign it as black 
					ctr += 1	#increasing count of black nodes
					col[nodes[queue[0].ind].neighbours[i].ind] = 1	#assigning the color as that index as black
					queue.append(nodes[queue[0].ind].neighbours[i])	#adding the new black node formed in the queue
					nTemp -= 1	#decreasing the count of nTemp
				else:	#for the remaining elements mark it as grey
					#counting and assigning of GREY nodes
					ctr2 += 1
					col[nodes[queue[0].ind].neighbours[i].ind] = 2
		#removing the black node which was just used from the queue
		queue.popleft()

#STEP 1 of Backbone Formation
def step3(nodes):

	stInd = step1(nodes)	#getiing the start index from STEP 1
	step2( nodes, stInd)	#performing STEP 2 using the start index
	for i in range(numNodes):	#for all Nodes
		if col[i] == 0:		#if color is WHITE
			step2(nodes, i)	#Performing STEP 2
	for i in range(numNodes):	#for all nodes
		if col[i] == 1:		#if color is BLACK
			flag = False	#making flag as False
			for j in range(len(nodes[i].neighbours) ):	#in all the neighbours of the specific node
				if col[nodes[i].neighbours[j].ind] != 1:	#
					flag = True
			if(not flag):
				col[i] = 2	#color assigned as GREY


ctr=0	#count of BLACK nodes
ctrg=0	#count of GREY nodes


def testing_b(nodes, ordNodes, backbone_nodes):
	global ctr 		#count of BLACK nodes
	global ctrg 	#count of GREY nodes
	for i in range(numNodes):	#for every Node
		if col[i] == 1:		#if the color is BLACK
			backbone_nodes.append(nodes[i])	#Adding it to backbone node list
			nodes[i].eres+=2
			nodes[i].einit+=2	
			nodes[i].bbInd = ctr
			ctr += 1	#increment of count of BLACK nodes
			nodes[i].ord=False
			nodes[i].ordInd=-1

		else:	#else if the node is GREY
			nodes[i].ordInd = ctrg	#assigning the nodes as Ordinary node and giving its index
			nodes[i].bbInd = -1
			ordNodes.append(nodes[i])	#adding that node in ordinary nodes(all GREY nodes)
			ctrg+=1		#incrementing the count of GREY nodes
			
	return nodes, ordNodes, backbone_nodes

#assigning the nodes head
def assign_head(backbone_nodes, ordNodes):
	diction={}	#dictionary(hash map) that stores the cluster head of all ordinary nodes
	for i in range(len(ordNodes)):	#for all the ordinary nodes(Grey Nodes)
		mini=math.inf 	#initialize minimum as infinity
		for j in range(len(backbone_nodes)):	#for all the backbone nodes
			temp=(ordNodes[i].x - backbone_nodes[j].x) ** 2 + (ordNodes[i].y - backbone_nodes[j].y)**2	#calculating the distance between ordinary(grey) and backbone(black) nodes
			
			if (temp< mini):	#checking if distance is minimum
				mini=temp 		#assigning the minimum distance
				minnode=backbone_nodes[j]	#assigning that backbone node as the closest node
		diction[ordNodes[i]]=minnode	#for that ordinary node, storing its best cluster head
	return diction		#returning diction

if __name__ != '__main__':
	nodes = []
	nodes = initNodes_rand(nodes)
	ordNodes=[]		#initalise list for ordinary nodes(used in backbone repair)
	backbone_nodes=[]	#initalise list for backbone nodes
	nodes=initNodes_rand(nodes)	#calling the initisation of nodes function
	nodes, nMax=initNeighbours(nodes)	#callint the assigning of neighbours function
	step3( nodes)	#Calling STEP 3 for backbone formation| After this function the backbone nodes will be created
	nodes, ordNodes, backbone_nodes=testing_b( nodes, backbone_nodes, ordNodes)	#calling the function which adds the Black and Grey node in lists
	print(ctr)
	print(ctrg)
