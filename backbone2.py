from fitness import *

def backbone_repair(ordNodes,nodes, backbone_nodes, temp,col):
    #ordNodes - list containing ordinary nodes
    #nodes - list containing all the nodes 
    #numNodes - total no of nodes
    #backbone_nodes - list containing backbone nodes
    #ctr - number of backbone nodes
    #ctrg - number of ordinary nodes
    #temp - index of the dead node
    #col - array of colors of nodes, 0-> white, 1 ->black, 2->grey
    candidates=[] #list to store neighbouring nodes of the dead backbone node who are grey in color
    n_of_n=[] #array which stores the neighbours of the above grey nodes
    new_backbone=[] #new array which consists of only the new nodes added to the backbone and not the whole backbone
    backbone_nodes.remove(nodes[temp]) #temp is the index of the dead node, that node is removed from the existing backbone
    ctr-=1  #decrease the total number of nodes in the backbone by 1
    for i in range(0,len(nodes[temp].neighbours)):  #for loop to traverse through the neighbours of the dead node
        if col[nodes[temp].neighbours[i].ind]==2: #if the ith neighbour of the dead node is grey in color
            candidates.append(nodes[temp].neighbours[i]) #add that neighbour to the list of candidates for repair
    for i in range(len(candidates)):  #for loop to traverse through the candidates
        if candidates[i].alive == False: #if candidate is dead then don't consider it
            continue 
        flag=False
        n_of_n=nodes[candidates[i].ind].neighbours #if candidate is alive, store all it's neighbours in the array n_of_n
        test=False
        for m1 in range(len(n_of_n)):
            if n_of_n[m1].ord==True:
                test=True
                break
        if test==False:
            for m in range(len(X)):
                X[m][candidates[i].ind]=0
        for j in range(0,len(n_of_n)): #traverse through the neighbours of this candidate
            n3=nodes[n_of_n[j].ind].neighbours #n3 stores the neighbours of each neighbour of the candidate
            for k in range(len(n_of_n)): #for loop to traverse through the neighbours of the candidate
                if k!=j: #if neighbour is not equal to itself 
                    n4=nodes[n_of_n[k].ind].neighbours #n4 stores the neighbours of the above obtained node
                    if n_of_n[j] not in n4 and n_of_n[j].alive==True and n_of_n[k].alive==True: #if the 2 neighbours of the candidate nodes are not previously connected, candidate becomes the replacement
                        candidates[i].eres+=2 #increase the residual energy of the candidate 
                        candidates[i].einit+=2 #increase the initial energy of the candidate
                        backbone_nodes.append(candidates[i]) #add the candidate to the list of backbone nodes
                        if candidates[i] in ordNodes: 
                            ordNodes.remove(candidates[i]) #remove the candidate from the list of ordinary nodes
                            ctrg-=1		
                            print("hello")					#decrease the count of ordinary nodes by 1
                        new_backbone.append(candidates[i]) #add the candidate to the list of newly added nodes to the backbone
                        ctr+=1 								#increase the number of backbone nodes by 1
                        return ordNodes,backbone_nodes
        
    return ordNodes,backbone_nodes  #return the ordinary nodes, backbone nodes and the count of ordinary nodes

