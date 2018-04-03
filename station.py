'''
Station class represents a sensor platform station.
All data is expected to come from a json entity which was originally created
   via a MongoDB json dump from FRF's SMS database.
'''

import os, json

class Station():
    def __init__(self, rowStr):
        aDict = json.loads(rowStr)
        self.id = aDict['_id']
        self.project = aDict['project']
        self.projectId = aDict['projectId']
        self.stationName = aDict['stationName']
        self.stationNumber = aDict['stationNumber']
        self.stationLoc = aDict['stationLoc']
        self.owner = aDict['owner']
        self.description = aDict['description']
        self.status = aDict['status']
        self.lat = float(aDict['lat'])
        self.lon = float(aDict['lon'])
        self.waterDepth = aDict['waterDepth']
        self.createdAt = aDict['createdAt']
        self.createdBy = aDict['createdBy']

def GetAllStationsDict(pathFN):
    returnDict = {}
    with open(pathFN, 'r') as theFile:
        allLines = theFile.readlines()

    for aRow in allLines:
        aStation = Station(aRow)
        returnDict[aStation.id] = aStation

    return returnDict



if __name__ == '__main__':
    testDir = 'Data/FRFdata'
    cwd = os.getcwd()
    testFullPath = os.path.join(cwd, testDir)
    stationsFile = os.path.join(testFullPath, 'stations.json')

    allStationsDict = GetAllStationsDict(stationsFile)
    print allStationsDict


