'''
Station class represents a sensor platform station.
All data is expected to come from a json entity which was originally created
   via a MongoDB json dump from FRF's SMS database.
'''

import os, json
from frfObjectBase import FrfObjectBase

class Station(FrfObjectBase):
    def __init__(self, rowStr):
        aDict = json.loads(rowStr)
        self.id = aDict['_id']
        self.project = aDict.get('project', None)
        self.projectId = aDict.get('projectId', None)
        self.stationName = aDict.get('stationName', None)
        self.stationNumber = aDict.get('stationNumber', None)
        self.stationLoc = aDict.get('stationLoc', None)
        self.owner = aDict.get('owner', None)
        self.description = aDict.get('description', None)
        self.status = aDict.get('status', None)
        self.lat = float(aDict.get('lat', '0.0'))
        self.lon = float(aDict.get('lon', '0.0'))
        self.waterDepth = aDict.get('waterDepth', '0.0')
        self.createdAt = aDict.get('createdAt', None)
        self.createdBy = aDict.get('createdBy', None)
        self._cleanUpNAs()

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


