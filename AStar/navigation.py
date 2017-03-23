# Haider Tiwana
# COMP 372: Artificial Intelligence
# Project 1: Navigating Memphis

import math
import sys
import pqueue as p

global DEBUG

DEBUG = False

class Location(object):
        def __init__(self, id, lat, lon):
                self.id = id;
                self.lat = lat;
                self.lon = lon;
                
class Road(object):
        def __init__(self, start_id, end_id, name, max_speed):
                self.start_id = start_id
                self.end_id = end_id
                self.name = name
                self.max_speed = max_speed
        
class Graph(object):
        def __init__(self):
                self.locations = {}
                self.roads = {}
                
        def add_location(self, id, lat, lon):
                loc = Location(id, lat, lon)
                self.locations[id] = loc # insert into dictionary
                # now we can look up any location by its ID
                
        def add_road(self, start_id, end_id, name, speed):
                rd = Road(start_id, end_id, name, speed)
                
                # first road seen from start_id?
                if start_id not in self.roads:
                        self.roads[start_id] = [ rd ] # insert new list into dictionary
                else:
                        self.roads[start_id].append(rd)

        def get_location(self, id):
                return self.locations[id]                       

        def get_roads(self, id):
                return self.roads[id]

class Node(object):
        def __init__(self, ID, f, g, h):
                self.ID = ID
                self.parent = None
                self.f = f
                self.h = h
                self.g = g
                
        # hashing functions to allow for object comparison between nodes
        def __eq__(self, other):
                if isinstance(other, self.__class__):
                        return self.ID == other.ID
                return NotImplemented


        def __hash__(self):
                return hash((self.ID))

# straight-line travel time from n to goal state: h(n)
def heuristicH(ID1, ID2, graph):
        h = 0
        location1 = graph.get_location(ID1)
        location2 = graph.get_location(ID2)
        h = (distSphere(location1.lat, location1.lon, location2.lat, location2.lon)/(65/60)) # 65 MPH
        return h

# travel distance from start state to node: g(n)
def heuristicG(ID1, ID2, graph):
        location1 = graph.get_location(ID1)
        location2 = graph.get_location(ID2)
        g = (distSphere(location1.lat, location1.lon, location2.lat, location2.lon))
        return g
      
def read_graph(filename):
        try:
                file = open(filename, "r")
        except:
                print("Bad filename")
                return None
                
        g = Graph()
        for line in file:
                pieces = line.strip().split("|")
                
                # parsing text and appending location to hash table
                if pieces[0] == "location":
                        id = int(pieces[1])
                        longitude = float(pieces[2])
                        latitude = float(pieces[3])
                        g.add_location(id, latitude, longitude)

                # parsing text and appending road to hash table
                elif pieces[0] == "road":
                        start = int(pieces[1])
                        end = int(pieces[2])
                        speed = int(pieces[3])
                        name = pieces[4]
                        g.add_road(start, end, name, speed)
                        g.add_road(end, start, name, speed)
                        
        return g

def distSphere(lat1, long1, lat2, long2):
 
        # Convert latitude and longitude to
        # spherical coordinates in radians.
        degrees_to_radians = math.pi/180.0
         
        # phi = 90 - latitude
        phi1 = (90.0 - lat1)*degrees_to_radians
        phi2 = (90.0 - lat2)*degrees_to_radians
         
        # theta = longitude
        theta1 = long1*degrees_to_radians
        theta2 = long2*degrees_to_radians
         
        cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
        math.cos(phi1)*math.cos(phi2))
        arc = math.acos( cos )

        # return number in miles
        return arc * 3960

def aStar(begID, endID, graph):

        nodeCount = 0

        # empty set of states
        explored = []
        rList = []

        # new node corresponding to the initial state
        node = Node(begID, 0, 0, 0)

        # a priority queue of nodes sorted by f(n)
        frontier = p.PQueue()
        # initialized to contain only one node
        frontier.enqueue(node, node.f)

        # loop indefinitely
        while not frontier.empty():

                # node = pop(frontier)
                current = frontier.dequeue()

                # if isGOAL(node.state), return solution
                if(current.ID == endID):
                        print("\nRouting from ", begID, "to", endID)
                        print("\nTotal travel time is", current.g, "minutes.")
                        while(current.parent != None):
                                rList.append(current.ID)
                                current = current.parent
                        rList.append(current.ID)
                        rList.reverse()
                        print("Number of nodes expanded:", nodeCount)
                        print("Path found is: ")
                        print(rList[0], "(starting location)")
                        for i in range(1, len(rList)):
                                myRoad = graph.roads[rList[i]]
                                for item in myRoad:
                                        if(item.end_id == rList[i-1]):
                                                print(item.start_id, item.name)
                        return

                # add node.state to explored set
                explored.append(current)
                nodeCount = len(explored)

                listofRoads = graph.roads[current.ID]
                if DEBUG:
                        print("\nVisiting", str(current.ID) + ", g = " + str(current.g) + ", h = " + str(current.h) + ", f = " + str(current.f))

                # for each action in ACTIONS(node.state):
                for item in listofRoads:
                        child = Node(item.end_id, 0, current.g, 0)
                        # travel time in minutes from start state to node: g(n)
                        addCost = heuristicG(current.ID, child.ID, graph)/(item.max_speed/60)
                        child.g += addCost
                        # h(n)
                        child.h = heuristicH(child.ID, endID, graph)
                        # f(n) = g(n) + h(n)
                        child.f = child.g + child.h

                        child.parent = current

                        # add child node to frontier
                        if child not in explored and not frontier.contains(child):
                                frontier.enqueue(child, child.f)
                                if DEBUG:
                                        print("\tAdding "+ str(item.end_id) + ", g = " + str(child.g) + ", h = " + str(child.h) + ", f= " + str(child.f), "to the frontier.")

                        # replace child node state on frontier with the better one
                        elif frontier.contains(child) and (child.f < frontier.get_priority(child)):
                                other = child

                                other.f = frontier.get_priority(child)
                                frontier.change_priority(child, child.f)
                                if DEBUG:
                                        print("\tUpdating path cost for", child.ID, "on the frontier")
                                        print("\t\told: " + str(other.ID) + ", g = " + str(other.f - other.h) + ", h = " + str(other.h) + ", f = " + str(other.f))
                                        print("\t\tnew: " + str(child.ID) + ", g = " + str(other.g) + ", h = " + str(child.h) + ", f = " + str(other.g + other.h))
      


def main():
        filename = input("What is the filename of the map text file? ")
        g = read_graph(filename)
        
        if g:
                frontier = p.PQueue()
                while True:
                        id1 = int(input("Enter first location id or zero to quit "))
                        if id1 == 0: break
                        id2 = int(input("Enter second location id or zero to quit: "))
                        if id2 == 0: break

                        # call A* algorithm on locations
                        aStar(id1, id2, g)
                        break

main()
