from structs import *
import random
import math

if __name__ != '__main__':
	nodes = []
	nodes = initNodes_rand(nodes, numNodes)

#intialisationof all nodes
def initNodes_rand(nodes,numNodes):
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
def initNeighbours(nodes,numNodes,nMax):
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
	return nodes,nMax


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
		denom = nodes[i].q * nodes[i].neighbours[j].res   #denominator of cost formula
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
		T_temp = w1 * nodes[i].res / E_init + w2 * len(nodes[i].neighbours) / nMax + w3 * cMax / nodes[i].cost
	else:
		T_temp = 0
	#adding T(i) value to its node
	nodes[i].weight = T_temp
	
	return nodes