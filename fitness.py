import math
import random
from shapely.geometry import * #shapely is a library to find union of two overlapping areas
random.seed(10)

from coverage import *

# fitness function f1 to check for residual energy
def fx1_func(X,ordNodes,i): 
	# 
	sum_temp = 0 #temporary sum variable
	fX1 = 0      #value to return 
	for j in range(numOrdNodes): #traverse through ordinary nodes
		sum_temp += X[i][j] * ordNodes[j].eres #sum of residual energy of alive ordinary nodes
	fX1 = 1 - (sum_temp / (numOrdNodes * E_init))	#subtract the sum_temp value from 1 to make fX1 a minimization function
	return fX1 

# fitness function f2 to check for centered degree
def fx2_func(X,ordNodes,particles):
    fx2_temp=[]						#list to store normalised values of fX2

    fX2 = [0 for x in range(nPart)] #list to store actual values of fX2
    for ii, i in enumerate(X):      #traverse through X
        sum_f = 0
        for j in range(numOrdNodes): #traverse through ordinary nodes
            sum_temp = 0
            count_never_used_before = 0
            tx = particles[ii].x	#store the x coordinate of the particle in tx
            ty = particles[ii].y	#store the y coordinate of the particle in ty
            for ki,k in enumerate(nodes[ordNodes[j].ind].neighbours) :	# traverse through the neighbours of 
                if k.ord == True:
                    count_never_used_before+=1
                    dis_ij = math.sqrt((tx - k.x) ** 2 + (ty - k.y) ** 2) #distance between sensor node and it's neighbour
                    dis_sinkj = math.sqrt((tx - sink_x) ** 2 + (ty - sink_y) ** 2) #distance between sensor node and sink node
                    sum_temp += (dis_sinkj - dis_ij) ** 2 # square of difference between the two distances is added to sum
            if count_never_used_before !=0:
                sum_f += math.sqrt(sum_temp /count_never_used_before)  #this sum divided by the total number of neighbours is added to final sum
        fX2[ii] = sum_f # this value is the value of the fitness function
    fx2_temp = [float(i)/sum(fX2) for i in fX2] # normalisation of the fitness function fX2
    return fx2_temp

#fitness function f3 to measure redundant area of overlap
def fx3_func(X,ordNodes,i):
	fx3 = 0		
	sum_f = 0
	dummy1 = Point(0, 0).buffer(0)	#dummy point of radius zero
	dummy2 = Point(0, 0).buffer(0)	#dummy point of radius zero
	union_area = dummy1.union(dummy2)	#dummy1 and dummy2 used to initialize union_area
	for j in range(numOrdNodes):	#traverse through ordinary nodes
		if(X[i][j] == 1):			#if node is awake
			sum_f += 3.14 * (radius ** 2)	# add the area to sum_f
			a = Point(ordNodes[j].x, ordNodes[j].y).buffer(radius) #area of ordinary sensor node
			union_area = union_area.union(a) #union of that sensor node with the current union
	try:
		fx3 = sum_f / union_area.area # dividing summation with union
	except:
		fx3 = 0		# error on division by 0 i.e when union area is zero (doesn't enter the for loop)
	return fx3

if __name__ == "__main__":
    #temp=fx2_func(X,ordNodes,particles)
    for i in range(len(X)):
        #alpha*fx1_func(X,ordNodes,i) + beta*temp[i] + gamma*fx3_func(X,ordNodes,i)
        print(fx3_func(X,ordNodes,i))