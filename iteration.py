

import numpy as np

import random
import math
import time
import matplotlib.pyplot as plt

from backbone2 import *
#The library below is for interactive graph. To be used only if the user wants to see changes in the graph after every 10 iterations.
plt.ion()
#Declaring the parameters for graph according to matplotlib syntax.
fig, ax = plt.subplots(1,1,figsize=(8,8))

#The 3 commands below are if the user wants to plot the position of the nodes and use the interactive graph.
#This sets the limit on x-axis as 400
plt.xlim((0,400))
#This sets the limit on y-axis as 400
plt.ylim((0,400))
#This is for setting the sink node at (200,200)
plt.scatter(200,200,c='y',marker='v',s=200)

numIter=201 #Set the number of rounds for which the simulation has to be run.

fX = [0 for x in range(nPart)] #Initialise the total fitness function
fgbest=math.inf #Initialise the global best value of fitness function.
fpbest=[math.inf for i in range(nPart)] #Initialise the local best value of fitness function for each particle.
xgbest=[] #Initialise the global best value amongst all X[i].
xpbest=[[] for i in range(nPart)] #Initialise the local best value of X[i], i.e., global local value of each particle.


#Initiliase the parameters for PSO.
# wmax=0.9
# wmin=0.4
# c1=0.4
# c2=0.4


def crossover(a,b): #This function is sued for applying the crossover operator.
    temp=[] #The output of crossover is defined as an empty list initially.
    for i in range(len(a)):
        y=random.random() #If the value of y is less than 0.5 then bit of 'a' gets appended or else bit of 'b' gets appended.
        if y<=0.5:
            temp.append(a[i])
        else:
            temp.append(b[i])
    return temp

diction=assign_head(backbone_nodes,ordNodes) #Import the dictionary which has the key as ordinary node and value as the cluster head
                                                             #  to which the ordinary node is assigned to.

xener = [] #Initialise an empty list which stores the number of rounds for energy at certain intervals.
yener = [] #Initialise an empty list which stores the energy at certain intervals.
xdead = [] #Initialise an empty list which stores the number of rounds for ratio of alive nodes to total nodes at certain intervals.
ydead = [] #Initialise an empty list which stores the ratio of alive nodes to total nodes at certain intervals.
deadnodecount=0
#Start the iterations
t=-1
while t<900:

    t+=1
    print("iteration number ",t)
    # F2(X) is called and the values for each particle is stored in list called temp
    temp=fx2_func(X,ordNodes,particles)
    for i in range(len(X)): #Store the value of the total fitness function in the list fX 
        #Multiply the values of each fitness function with their multiplication constants.
        fX[i]=alpha*fx1_func(X,ordNodes,i) + beta*temp[i] + gamma*fx3_func(X,ordNodes,i)
        if fX[i]<fpbest[i]: #Check if the local best needs to be updated.
            fpbest[i]=fX[i]
            xpbest[i]=X[i] 
            if fX[i]<fgbest: #If a new local best is found then we check is it better than the global best.
                fgbest=fX[i]
                xgbest=X[i]
    
    
    for i in ordNodes: #Subtract the energy
        if(i.alive == True and xgbest[i.ordInd] == 1): #Check if the ordinary node is not dead and awake.
            bb=diction[i] #Access the cluster head of that ordinary node
            dist=math.sqrt((i.x-bb.x)**2 + (i.y-bb.y)**2) #Find the distance between the ordinary node and cluster head
            if dist>d0:
                eTemp = k * (Eelec + Eamp * (dist ** 4))
            else:
                eTemp = k * (Eelec + Efs * (dist ** 2))

            if i.eres>=0: #Check if the residual energy of the ordinary node is greater than 0.
                i.eres-=eTemp #Subtract the cost of transmission of message to cluster head.
                if i.eres<=0: #If the energy drops to 0 then the ordinary node is dead.
                    i.eres=0
                    i.alive = False

            dist2=math.sqrt((bb.x-sink_x)**2 + (bb.y-sink_y)**2) #Find the distance between the cluster head and sink node.
            if dist2>d0:
                eTemp2 = k * (Eelec + Eamp * (dist2 ** 4))
            else:
                eTemp2 = k * (Eelec + Efs * (dist2 ** 2))
            if(nodes[bb.ind].eres>=0): #Check if the residual energy of the backbone node is greater than 0.
                nodes[bb.ind].eres -= eTemp #Subtract the cost of receival of message from sensor node
                if(nodes[bb.ind].eres<=0): #If the energy drops to 0 then the backbone node is dead and we have to repair it.
                    nodes[bb.ind].eres=0
                    nodes[bb.ind].alive = False
                    #The function below return the updated list of ordinary nodes and backbone nodes
                    ordNodes,backbone_nodes=backbone_repair(ordNodes,nodes, backbone_nodes,bb.ind,col)
                    #The function below assigns new cluster heads to each ordinary node as a new backbone is formed.
                    diction=assign_head(backbone_nodes,ordNodes)
                else:
                    nodes[bb.ind].eres -= eTemp2 #Subtract the cost of transmission of message to sink node.
                    if(nodes[bb.ind].eres<=0): #If the energy drops to 0 then the backbone node is dead and we have to repair it.
                        nodes[bb.ind].eres=0
                        nodes[bb.ind].alive = False
                        #The function below return the updated list of ordinary nodes and backbone nodes
                        ordNodes,backbone_nodes=backbone_repair(ordNodes,nodes, backbone_nodes,bb.ind,col)
                        #The function below assigns new cluster heads to each ordinary node as a new backbone is formed.
                        diction=assign_head(backbone_nodes,ordNodes)
    
    if t%10==0: #Whenever this condition is true the state of the network will be captured and stored for different graphs.
        
        enertot = 0 #Initialise the variable which will store the total energy of all nodes combined.
        for i in nodes: #Calculate the total energy
            enertot += (i.eres)
        # yener.append(enertot/(len(nodes)*nodes[0].einit)) #Append the value in the list which holds values for y axis of (total energy) vs (rounds) graph. 
        yener.append(enertot)
        xener.append(t) #Append the value in the list which holds values for x axis of (total energy) vs (rounds) graph.
        deadnodecount = 0 #Initialise the variable which will store the total number of dead nodes.
        for i in nodes: #Iterate through all the nodes.
            if i.alive==False: #If node is dead then add it to deadnodecount
                deadnodecount+=1
        ydead.append((len(nodes)-deadnodecount)/len(nodes)) #Append the value in the list which holds
                                                            # values for y axis of (ratio of alive nodes to dead nodes) vs (rounds) graph. 
        xdead.append(t) #Append the value in the list which holds
                        # values for x axis of (ratio of alive nodes to dead nodes) vs (rounds) graph.
        
        plt.plot(xener,yener,'r+-') #Plot the list of values for (total energy) vs (rounds) graph.
        plt.savefig("energraph2.png") #Save the graph of (total energy) vs (rounds) at current iteration.
        plt.clf() #Clear the graph for the next plot.
        plt.plot(xdead,ydead,'r+-') #Plot the list of values for (ratio of alive nodes to dead nodes) vs (rounds) graph.
        plt.savefig("deadgraph.png") #Save the graph of (ratio of alive nodes to dead nodes) vs (rounds) graph.
        plt.clf() #Clear the graph for the next plot.
        
        
        #The code below is to be used only when a live graph of the total nodes present on the 
        # (400,400) grid is needed.
        #Sleeping nodes = BLUE
        #Awake nodes = RED
        #Backbone nodes = BLACK
        #Dead nodes = YELLOW with a BLACK outline
        #Sink node = A large YELLOW triangle
        
        for i in ordNodes: #Iterate through all the ordinary nodes
            if (i.alive==True): #Check if the node is alive
                if(xgbest[i.ordInd] == 0): #Check if the node is in sleep state. Mark the colour of sleeping nodes as BLUE.
                    plt.scatter(i.x,i.y,c='b') #Plot the point on the graph
                else: #Check if the node is in awake state. Mark the colour of sleeping nodes as RED.
                    plt.scatter(i.x,i.y,c='r') #Plot the point on the graph

        xcords = [i.x for i in backbone_nodes if i.alive==True] #Store the x coordinates of the backbone nodes which are alive.
        ycords = [i.y for i in backbone_nodes if i.alive==True ] #Store the y coordinates of the backbone nodes which are alive.
        plt.scatter(xcords, ycords, c='k') #Plot the points for the backbone nodes as BLACK. 
        xc2=[i.x for i in nodes if i.alive==False] #Store the x coordinates of the nodes which are dead.
        yc2=[i.y for i in nodes if i.alive==False] #Store the y coordinates of the nodes which are dead.
        plt.scatter(xc2, yc2, facecolors='y', edgecolors='k') #Plot the points for the dead nodes as YELLOW with BLACK outline
        fig.canvas.draw() #Plot the graph. Make sure that the line plt.ion() is not commented at the start of the file.
        fig.canvas.flush_events() #Clear the graph for the next plot.

    for i in range(len(X)): #We will calculate the new positions of all the particles.
        r1=random.random()
        #w=wmin+(wmax-wmin)*(numIter-t)/numIter #The formula for computing the inertia. As number of iterstions increases the inertia decreases
        if fX[i] != fpbest[i]:
            w=wmin+math.exp(-abs(fX[i]-fgbest)/abs(fX[i]-fpbest[i]))
        else:
            w=wmin
        #DETERMINE Xi FOR NEXT ITERATION
        if r1<w: #This condition was given in the paper
            #MUTATION
            random.shuffle(X[i]) #We shuffle the values of particle 'i', i.e., we 'mutate' the values.
        r2=random.random() #We generate a random value.
        if r2<c1: 
            X[i]=crossover(X[i],xpbest[i]) #Apply crossover operation on the particle values and local best values.
        r3=random.random()
        if r3<c2:
            X[i]=crossover(X[i],xgbest) #Apply crossover operation on the particle values and global best values.

#Prints the total number of dead nodes at end of all iterations.
print("Total number of dead nodes are: ")
deadnodes = 0 #Initialise the variable which will store the total number of dead nodes.
for i in range(len(nodes)): #Iterate through all the nodes.
    if nodes[i].alive==False: #If node is dead then add it to deadnodes
        deadnodes+=1
print(deadnodes)