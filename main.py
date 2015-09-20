__author__ = 'clchang'

class Node:
    def __init__(self, ID, power):
        self.x = ID
        self.power = power
        self.link = []

    def add_link(self, link, dist):
        self.link.append([[link, dist]])

    def update(self, need_power, father):
        if self.power >= need_power:
            return end



class Link:
    def __init__(self, n1, n2, distance):
        self.n1 = n1


power = 20.0    # necessary power
distance = 0.0  # max distance
nodeList = []

# initial node
for i in range(0,8):
    bus = Node(i,i)
    nodeList = nodeList + [bus]
    print(nodeList[i].x)

# add connection info (need to design)
for i in range(0,8):
    if i < 7:
        nodeList[i].add_link(i+1,5)
        nodeList[i+1].add_link(i,5)
    else:
        nodeList[i].add_link(i-1,5)

