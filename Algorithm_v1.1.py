__author__ = 'clchang'

import heapq    # 2nd nsmallest/nlargest

class Node:
    def __init__(self, ID, power):
        self.x = ID
        self.power = power
        self.dist = 0
        self.used = 0
        self.fatherID = 0
        self.otherPower = 0
        self.otherDist = 1000000000
        self.linkID = []
        self.linkDist = []
        # self.relayID = []
        # self.relayDist = []
        self.used = 0

    def add_link(self, link, dist):
        self.linkID.append(link)
        self.linkDist.append(dist)

    def delete_link(self, id):
        # i = self.linkID.index(id)
        if id in self.linkID:
            i = self.linkID.index(id)
            del self.linkDist[i]
            del self.linkID[i]

    def d2id(self, d):
        if d in self.linkDist:
            return self.linkID[self.linkDist.index(d)]

    def id2d(self, id):
        if id in self.linkID:
            return self.linkDist[self.linkID.index(id)]




power = 170.0    # necessary power
P = power
distance = 0.0  # max distance
# Topology: add connection info (need to design!!!!!!!!!)--------------------------------------

# Node [power] (IEEE 33 bus)
#     1   2   3   4   5   6   7   8   9  10
N = [ 4,  5,  6,  7, 10, 13,  2,  5,  6,  9,
     12, 16, 22, 31,  6, 11,  6,  9, 10, 22,
      5, 21, 14, 19, 11,  9,  9, 10, 13,  9,
      1,  2,  2]
N = [0] + N

# Links of IEEE 33 bus
L = [[0,1,10], [1,2,5], [2,3,5], [2,19,20], [3,4,20], [3,23,30], [4,5,7], [5,6,5],
     [6,7,4], [6,26,16],
     [7,8,3], [8,9,3], [9,10,10], [10,11,10], [11,12,2], [12,13,2],
     [13,14,2], [14,15,2], [15,16,2], [16,17,2], [17,18,2],
     [19,20,6], [20,21,3], [21,22,6],
     [23,24,7], [24,25,7],
     [26,27,3], [27,28,3], [28,29,3], [29,30,3], [30,31,3], [31,32,3], [32,33,3]]

# Node initialize
nodeList = [Node(i,N[i]) for i in range(0,len(N))]     # node 0 ~ N-1 (node 0 is the grid)
                                                # initialize Node(ID, power)
# Link
for c in L:
    nodeList[c[0]].add_link(c[1], c[2])
    nodeList[c[1]].add_link(c[0], c[2])


# for j in range(0, 5):
#     nodeList[j].add_link(j+1, 3)
#     nodeList[j+1].add_link(j, 3)
#
# nodeList[2].add_link(6, 1)
# nodeList[6].add_link(2, 1)
#
# for j in range(6, 9):
#     nodeList[j].add_link(j+1, 2)
#     nodeList[j+1].add_link(j, 2)

# print [nodeList[i].linkID for i in range(0,len(N))]
# ----------------------------------------------------------------------------------------------
# print("AA")



supplyNode = []
supplyPower = []
IDc = 0                 # IDc: current ID
nodeList[IDc].used = 1
IDf = 0                 # IDf: "father" of IDc
d0j = 0.0
temp = 0
d_ = 1000000000
p_ = 0

z = 0

while power > 0:
    print("--------------------------------------------------------------------------------------------------------------------")
    print ""

    # print(nodeList[IDc].linkID, nodeList[IDc].linkDist)

    # update link status (delete used links)
    for i in nodeList[IDc].linkID:
        if nodeList[i].used == 1:
            nodeList[IDc].delete_link(i)

    # print(IDc, nodeList[IDc].linkID)

    if len(nodeList[IDc].linkID) == 0:          # len(nodeList[IDc].linkID) = 0 --> end point, then just go back to father node
        if IDc in nodeList[IDf].linkID:
            nodeList[IDf].delete_link(IDc)

        print "End node", IDc, "jumps to", nodeList[IDc].fatherID

        IDc = nodeList[IDc].fatherID

    else:       # do basic process
        # 1. find the shortest link in IDc
        dmin = min(nodeList[IDc].linkDist)
        D = [nodeList[IDc].linkID[i] for i, j in enumerate(nodeList[IDc].linkDist) if dmin == j]
        # see enumerate function --> https://docs.python.org/2/library/functions.html#enumerate
        # the all IDs with shortest link i in set D
        # find its own power in D
        listPower = [nodeList[i].power for i in D]
        Pmax = listPower.index(max(listPower))
        idj = D[Pmax]
        del listPower[Pmax]
        del D[Pmax]

        idj2 = -1
        if len(D) > 0:
            Pmax2 = max(listPower)
            idj2 = D[listPower.index(Pmax2)]

        d0j = dmin + nodeList[IDc].dist
        # from now on, shortest_d is the shortest distance, and idj is the ID
        # temp is the position in D of power

        # print(shortest_d, nodeList[IDc].otherDist)

        d_ = nodeList[IDc].otherDist
        p_ = nodeList[IDc].otherPower

        print "Current ID", IDc, "has the links", nodeList[IDc].linkID, "with distances", nodeList[IDc].linkDist

        if d0j < d_ or (d0j == d_ and nodeList[idj].power > p_):
            if nodeList[IDc].used == 2:
                print IDc, "is the critical point and links to", idj
                print "Current other min distance:", nodeList[IDc].otherDist
                # print "goes down from ", IDc, " to ", idj

                if len(nodeList[IDc].linkID) > 1:
                    [x1, x2] = heapq.nsmallest(2, nodeList[IDc].linkDist)
                    d_ = nodeList[IDc].dist + x2

                nodeList[idj].otherDist = d_
                nodeList[idj].otherPower = p_
                nodeList[idj].fatherID = IDc

                nodeList[IDc].delete_link(idj)
                if IDc in nodeList[idj].linkID:
                    nodeList[idj].delete_link(IDc)

                if len(nodeList[IDc].linkID) == 0:
                    nodeList[IDc].used = 1

                if nodeList[idj].used == 0:
                    nodeList[idj].used = 1
                    nodeList[idj].dist = d0j

                    supplyNode.append(idj)
                    supplyPower.append(nodeList[idj].power)

                    power = power - nodeList[idj].power
                    print "Power is consumed", nodeList[idj].power, "at", idj


            elif nodeList[idj].used == 0:
                supplyNode.append(idj)
                supplyPower.append(nodeList[idj].power)

                print IDc, "links to", idj, "by adding distance", dmin
                print "Get power", nodeList[idj].power
                # print "Add distance", dmin
                print "Other min distance", nodeList[IDc].otherDist, "> current distance", d0j
                nodeList[idj].used = 1                  # new node is connected (used)
                nodeList[idj].dist = d0j                # update dist of new node
                power = power - nodeList[idj].power     # update total power info
                nodeList[idj].fatherID = nodeList[IDc].fatherID
                # nodeList[idj].fatherID = IDf
                if nodeList[IDc].used == 2:
                    if len(nodeList[IDc].linkID) > 1:
                        nodeList[idj].fatherID = IDc
                        IDf = IDc
                    elif len(nodeList[IDc].linkID) == 1:
                        nodeList[IDf].delete_link(IDc)

                nodeList[idj].otherDist = d_
                nodeList[idj].otherPower = p_

                if len(nodeList[IDc].linkID) > 1:    # if IDc is critical point which has 2 or more links
                    # nodeList[IDf].add_link(IDc, nodeList[IDc].dist-nodeList[IDf].dist)
                    nodeList[IDc].used = 2

                    nodeList[idj].fatherID = IDc
                    IDf = IDc
                    [x1, x2] = heapq.nsmallest(2, nodeList[IDc].linkDist)

                    if x2 + nodeList[IDc].dist < d_:
                        nodeList[idj].otherDist = x2 + nodeList[IDc].dist
                        d_ = nodeList[idj].otherDist
                        # other_d1 = nodeList[idj].otherDist
                        if idj2 == -1:
                            a = nodeList[IDc].d2id(x2)
                            # a = nodeList[IDc].find_e_of_linkList(x2, 2)
                            # b = nodeList[IDc].linkID[a]
                            nodeList[idj].otherPower = nodeList[a].power
                        else:
                            nodeList[idj].otherPower = nodeList[idj2].power
                        p_ = nodeList[idj].otherPower

                nodeList[IDc].delete_link(idj)
                nodeList[idj].delete_link(IDc)

            IDc = idj

            # print (IDc, power, nodeList[IDc].dist, nodeList[IDc].otherDist, nodeList[IDc].fatherID)      # test line: new node, current necessary power, and the max distance
            # print (IDc, power, nodeList[IDc].dist, d_, nodeList[IDc].fatherID)


        else:   # Jump to father. Build the virtual connection between IDf and idj
            print "Other distance < current min distance:", nodeList[IDc].otherDist, "<", d0j
            nodeList[IDc].used = 2

            nodeList[IDc].otherDist = 1000000000
            nodeList[IDc].otherPower = 0

            IDf = nodeList[IDc].fatherID
            [d_, d0j] = [d0j, d_]
            p_ = nodeList[idj].power

            print IDc, "jumps to", IDf
            # print("check: ", IDc, IDf, nodeList[IDf].linkID)
            if IDc not in nodeList[IDf].linkID:
                nodeList[IDf].add_link(IDc, d_ - nodeList[IDf].dist)

            IDc = IDf
            # print("jump to ", IDc)
            d_ = nodeList[IDc].dist + min(nodeList[IDc].linkDist)

            while d_ > nodeList[IDc].otherDist:
                print ""
                print ">>>> other distance < current min distance:", nodeList[IDc].otherDist, "<", d_

                if d_ > min(nodeList[IDc].linkDist):
                    a = nodeList[IDc].d2id(min(nodeList[IDc].linkDist))
                    p_ = nodeList[a].power
                    d_ = nodeList[IDc].dist + min(nodeList[IDc].linkDist)
                    print "Update new min distance d0j:", d_

                nodeList[IDc].otherDist = 1000000000
                nodeList[IDc].otherPower = 0

                IDf = nodeList[IDc].fatherID
                if IDc not in nodeList[IDf].linkID:
                    nodeList[IDf].add_link(IDc, d_ - nodeList[IDf].dist)

                print IDc, "jumps to", IDf
                IDc = IDf
                # print(nodeList[IDf].linkDist)
                # print("while jump to ", IDc, d_)

            # print("search from ", IDc, d_, nodeList[IDc].linkID)
            print ""
            print "Current ID", IDc, "has the link", nodeList[IDc].linkID, "with distance", nodeList[IDc].linkDist
            print "And other distance", nodeList[IDc].otherDist, "> min distance", d_

    print ""
    print "................."
    print ""


    print "Updated new necessary power:", power
    print "Next node:", IDc

    print "Updated new max distance:", d0j
    print "Updated new other min distance:", d_
    print ""

    print "Current node list which can supply power:", supplyNode
    print "Power list:", supplyPower
    print ""

print "!!!!!!!!!!!!!!!!!!!! Simulation End !!!!!!!!!!!!!!!!!!!!!!!!"
print ""

A = sum(supplyPower)
AP = sum(N)
print "All usable power is", AP
print "and the total supply power", A, "to offer the necessary power", P
print "by using the nodes", supplyNode