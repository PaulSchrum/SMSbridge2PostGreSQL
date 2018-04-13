'''
Station class represents a sensor platform station.
All data is expected to come from a json entity which was originally created
   via a MongoDB json dump from FRF's SMS database.
'''

import os, json
from frfObjectBase import FrfObjectBase

requiredFields = [('_id', 'STRING', '31'),
                  ('project', 'STRING', '31'),
                  ('projectId', 'STRING', '31'),
                  ('stationName', 'STRING', '31'),
                  ('stationNumber', 'STRING', '31'),
                  ('stationLoc', 'STRING', '63'),
                  ('owner', 'STRING', '31'),
                  ('description', 'STRING', '127'),
                  ('status', 'STRING', '31'),
                  ('lat', 'STRING', '31'),
                  ('lon', 'STRING', '31'),
                  ('waterDepth', 'STRING', '31'),
                  ('createdAt', 'STRING', '31'),
                  ('createdBy', 'STRING', '31')
                  ]

def getStationsFieldList():
    '''
    Retrieves the list of fields to be updated for a Station Row.
    Using this every time ensures that the order of fields is always the same.
    '''
    retList = ['SHAPE@XY']
    retList.extend([val[0] for val in requiredFields])
    return retList

fieldNameNumberDict = {}
for index, value in enumerate(getStationsFieldList()):
    fieldNameNumberDict[value] = index

class Station(FrfObjectBase):
    def __init__(self, rowStr):
        aDict = json.loads(rowStr)
        self._id = aDict['_id']
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
        if self.createdAt is not None:
            self.createdAt = self.createdAt['$date']

    def createOrUpdateRow(self):
        '''
        :return: List containing all values of this station
        '''
        retList = [(self.lon, self.lat)] # corresponds to 'SHAPE@XY'
        for fieldName in getStationsFieldList()[1:]:
            aValue = self.__dict__[fieldName]
            retList.append(aValue)
        return retList


def GetAllStationsDict(pathFN):
    returnDict = {}
    with open(pathFN, 'r') as theFile:
        allLines = theFile.readlines()

    for aRow in allLines:
        aStation = Station(aRow)
        returnDict[aStation._id] = aStation

    return returnDict



if __name__ == '__main__':
    testDir = 'Data/FRFdata'
    cwd = os.getcwd()
    testFullPath = os.path.join(cwd, testDir)
    stationsFile = os.path.join(testFullPath, 'stations.json')

    allStationsDict = GetAllStationsDict(stationsFile)
    print allStationsDict


