# Haider Tiwana
# COMP 372: Artificial Intelligence
# Project 0
# Graph Warmup

# define basic structure of graph
class location:
    def __init__(self, uniqueID, longitude, latitude):
        self.uniqueID = uniqueID
        self.longitude = longitude
        self.latitude = latitude

class road:
    def __init__(self, startID, endID, speedLimit, roadName):
        self.startID = int(startID)
        self.endID = int(endID)
        self.roadName = roadName
        self.speedLimit = speedLimit

class myGraph:
    def __init__(self, locations_dict, roads_dict):
        self.locations_dict = locations_dict
        self.roads_dict = roads_dict

def main():

    # initialize hash tables
    locations_dict = {}
    roads_dict = {}
    gg = myGraph(locations_dict, roads_dict)

    # ask for input
    filename = input("Enter filename: ")
    file = open(filename, 'r')

    # parse file
    for line in file:
        line = line.split("|")

        # add location keys and objects to dictionary
        if line[0] == "location":
            addLocation = location(line[1], line[2], line[3])
            gg.locations_dict[addLocation.uniqueID] = addLocation
            
        # add road keys and objects to dictionary
        if line[0] == "road":
            addRoad = road(line[1],line[2], line[3], line[4]) # A -> B
            addRoad2 = road(line[2], line[1], line[3], line[4]) # B -> A
            
            # add A -> B
            if addRoad.startID in roads_dict:
                gg.roads_dict[addRoad.startID].append(addRoad)
            else:
                gg.roads_dict[addRoad.startID] = [addRoad]

            # add B -> A
            if addRoad.endID in roads_dict:
                gg.roads_dict[addRoad.endID].append(addRoad2)
            else:
                gg.roads_dict[addRoad.endID] = [addRoad2]

    # Ask for input or exit
    locNum = 1
    while(locNum != 0):
        locNum = int(input("Enter a location or zero to quit: "))

        if locNum == 0:
            print("Exiting...")
        else:
            print("Location ", locNum, " has edges leading to: ")

            listofRoads = gg.roads_dict[locNum]
            for item in listofRoads:
                print(item.endID, item.speedLimit, "mph", item.roadName, end="")
    
    file.close()
    
main()
