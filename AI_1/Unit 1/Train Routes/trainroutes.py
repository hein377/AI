import sys
from math import pi , acos , sin , cos
from heapq import heappush, heappop
import time
import tkinter

#Global Variables
nodes_lat_long = {}                    #{ nodeID(str) : (latitude(str), longitude(str)) }
nodes_names = {}                       #{ cityname(str) : nodeID(str) }
nodes_edges_distances = {}             #{ nodeID(str) : [ (edge(str), distance(float)) ] }
start_node, start_city = "", ""
end_node, end_city = "", ""

def calcd(node1, node2):
   # all assumed to be in decimal degrees
   y1, x1 = node1           # y1 = lat1, x1 = long1
   y2, x2 = node2           # y2 = lat2, x2 = long2

   R   = 3958.76    # miles = 6371 km
   y1 *= pi/180.0
   x1 *= pi/180.0
   y2 *= pi/180.0
   x2 *= pi/180.0

   # approximate great circle distance with law of cosines
   return acos( sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1) ) * R

def findDistance(nodeID, edgeID):
    nodelat, nodelong = nodes_lat_long.get(nodeID)
    edgelat, edgelong = nodes_lat_long.get(edgeID)
    return calcd( (float(nodelat), float(nodelong)) , (float(edgelat), float(edgelong)) )

data_structure_start = time.perf_counter()
with open("rrNodes.txt") as f:
    for line in f:
        line_list = line.strip().split(' ')                  #line_list = [nodeID, latitude, longitude]
        nodes_lat_long.update({ line_list[0] : (line_list[1], line_list[2]) })
    
with open("rrNodeCity.txt") as f:
    for line in f:
        cityName, line_list = "", line.strip().split(' ')                  #line_list = [nodeID, cityName]
        for i in range(1, len(line_list)):
            cityName += line_list[i] + " "
        nodes_names.update({ cityName.strip() : line_list[0] })

def addEdge(nodeID, edgeID):
    distance = findDistance(nodeID, edgeID)
    if(nodeID not in nodes_edges_distances): nodes_edges_distances.update({ nodeID : [ (edgeID, distance) ] })
    else: nodes_edges_distances.get(nodeID).append((edgeID, distance))

with open("rrEdges.txt") as f:
    for line in f:
        line_list = line.strip().split(' ')                  #line_list = [nodeID, edgeID]
        addEdge(line_list[0], line_list[1])
        addEdge(line_list[1], line_list[0])
data_structure_end = time.perf_counter()

def get_edges(nodeID):
    return nodes_edges_distances.get(nodeID)

def dijkstra(start_node, end_node):
    fringe, closed, start_node = [], set(), (0, start_node)            #start_node = (depth, nodeID)
    heappush(fringe, start_node)
    while(len(fringe) != 0):
        node = heappop(fringe)
        depth, nodeID = node
        if nodeID == end_node: return depth
        if nodeID not in closed:
            closed.add(nodeID)
            for edgeID, distance in get_edges(nodeID):
                if edgeID not in closed:
                    temp = (depth+distance, edgeID)
                    heappush(fringe, temp)
    return None

def heuristic(start_node, end_node):
    return findDistance(start_node, end_node)

def a_star(start_node, end_node):
    fringe, closed, start_node = [], set(), (heuristic(start_node, end_node), 0, start_node)            #start_node = (f, depth, nodeID) where f = heuristic(nodeID) + depth
    heappush(fringe, start_node)
    while(len(fringe) != 0):
        node = heappop(fringe)
        f, depth, nodeID = node
        if nodeID == end_node: return depth
        if nodeID not in closed:
            closed.add(nodeID)
            for edgeID, distance in get_edges(nodeID):
                if edgeID not in closed:
                    temp = (depth+distance+heuristic(edgeID, end_node), depth+distance, edgeID)
                    heappush(fringe, temp)
    return None

start_node = nodes_names.get(start_city:=sys.argv[1])
end_node = nodes_names.get(end_city:=sys.argv[2])
print("Time to create data structure: %s" % (data_structure_end-data_structure_start))

start = time.perf_counter()
print("%s to %s with Dijkstra: %s in " % (start_city, end_city, dijkstra(start_node, end_node)), end = '')
end = time.perf_counter()
print(str(end-start) + " seconds.")

start = time.perf_counter()
print("%s to %s with A*: %s in " % (start_city, end_city, a_star(start_node, end_node)), end = '')
end = time.perf_counter()
print(str(end-start) + " seconds.")
