'''
Station class represents a sensor platform station.
All data is expected to come from a json entity which was originally created
   via a MongoDB json dump from FRF's SMS database.
'''

import os, json
from frfObjectBase import FrfObjectBase

class Gage(FrfObjectBase):
    def __init__(self, rowStr):
        aDict = json.loads(rowStr)
        self.id = aDict['_id']
        self.projectId = aDict.get('projectId', None)
        self.station =  aDict.get('station', None)
        self.stationId =  aDict.get('stationId', None)
        self.gageNumber =  aDict.get('gageNumber', None)
        self.gageName =  aDict.get('gageName', None)
        self.gageType =  aDict.get('gageType', None)
        self.serialNumber =  aDict.get('serialNumber', None)
        self.barCode =  aDict.get('barCode', None)
        self.manufacturer =  aDict.get('manufacturer', None)
        self.model =  aDict.get('model', None)

        self.firmwareVersion =  aDict.get('firmwareVersion', None)

        self.lat = float( aDict.get('lat','0.0'))
        self.lon = float( aDict.get('lon', '0,0'))

        try:
            self.depth =  float(aDict['depth']['nominalDepth'])
        except:
            self.depth = 0.0

        self.description = aDict.get('description', None)
        self.createdAt =  aDict.get('createdAt', None)
        self.createdBy =  aDict.get('createdBy', None)
        self._cleanUpNAs()


def GetAllGagesDict(pathFN):
    returnDict = {}
    with open(pathFN, 'r') as theFile:
        allLines = theFile.readlines()

    for aRow in allLines:
        aStation = Gage(aRow)
        returnDict[aStation.id] = aStation

    return returnDict

if __name__ == '__main__':
    testDir = 'Data/FRFdata'
    cwd = os.getcwd()
    testFullPath = os.path.join(cwd, testDir)
    stationsFile = os.path.join(testFullPath, 'gages.json')

    allGagesDict = GetAllGagesDict(stationsFile)
    for gageKey, aGage in allGagesDict.iteritems():
        print gageKey
        aGage.prettyPrint()
        print


