import sys
import os
import re
from csv import reader


# Class CSV2Vec():



def ReadCSVwithHeaders():
    with open('trajectories.csv', 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        headerKeys = next(csv_reader)
        headerDict = dict()
        for key in headerKeys:
            headerDict[key] = list()
        print(headerDict)
        # Iterate over each row in the csv using reader object
        for row in csv_reader:
            # row variable is a list that represents a row in csv
            # print(row)
            for val_ind in range(len(row)):
                headerDict[headerKeys[val_ind]].append(row[val_ind])
                # print(headerDict)
        print(headerDict)

def ReadCSVnoHeader():
    with open('trajectories.csv', 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        Keys = ["T", "Ship_X", "Ship_Y", "Ship_isActive",\
                "Drone1_X", "Drone1_Y", "Drone1_isActive",\
                "Drone2_X", "Drone2_Y", "Drone2_isActive"]
        AllVectorsDict = dict()
        i = 0
        for row in csv_reader:
            AllVectorsDict[Keys[i]] = row
            i = i+1
        # print(AllVectorsDict["Ship_X"])
        steps = len(AllVectorsDict["T"])
        # print(steps)
        for i in range(1,steps):
            print(i)


class CSV2Vec():

    # state space
    ship_pos = []
    drone1_pos = []
    drone2_pos = []
    explosions = []

    # predicates
    ship_active = 0
    d1_active = 0
    d2_active = 0

    dt = 0.01

    def __init__(self, csvfile):
        # state space
        self.ship_pos = []
        self.drone1_pos = []
        self.drone2_pos = []
        self.explosions = []
        self.T = []
        # predicates
        self.ship_active = 0
        self.d1_active = 0
        self.d2_active = 0
        self._parseCSV2vectors(csvfile)


    def GetShipTrajectory(self):
        return self.ship_pos

    def GetDrone1Trajectory(self):
        return self.drone1_pos

    def GetDrone2Trajectory(self):
        return self.drone2_pos

    def ExplosionsTiming(self):
        return self.explosions

    def _parseCSV2vectors(self, csvfile):
        with open(csvfile, 'r') as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj)
            Keys = ["T", "Ship_X", "Ship_Y", "Ship_isActive", \
                    "Drone1_X", "Drone1_Y", "Drone1_isActive", \
                    "Drone2_X", "Drone2_Y", "Drone2_isActive"]
            AllVectorsDict = dict()
            i = 0
            for row in csv_reader:
                AllVectorsDict[Keys[i]] = row
                i = i + 1
        self.T = AllVectorsDict["T"]
        steps = len(self.T)
        for i in range(1, steps):
            self.ship_pos.append(
                [AllVectorsDict["Ship_X"][i], AllVectorsDict["Ship_Y"][i], AllVectorsDict["Ship_isActive"][i]])
            self.drone1_pos.append(
                [AllVectorsDict["Drone1_X"][i], AllVectorsDict["Drone1_Y"][i], AllVectorsDict["Drone1_isActive"][i]])
            self.drone1_pos.append(
                [AllVectorsDict["Drone2_X"][i], AllVectorsDict["Drone2_Y"][i], AllVectorsDict["Drone2_isActive"][i]])
            self.explosions.append(0)









def main():
    CSVReader = CSV2Vec('trajectories.csv')

    # ReadCSVnoHeader()

if __name__ == "__main__":
    main()



