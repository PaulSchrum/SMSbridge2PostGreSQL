'''
Gage class represents a a gage or sensor.
All data is expected to come from a json entity which was originally created
   via a MongoDB json dump from FRF's SMS database.
'''

import os, json
from frfObjectBase import FrfObjectBase as B

requiredFields = [('mongo_id', 'STRING', '31'),
                  ('stationId', 'STRING', '31'),
                  ('gageNumber', 'STRING', '31'),
                  ('gageName', 'STRING', '31'),
                  ('gageType', 'STRING', '63'),
                  ('lat', 'STRING', '31'),
                  ('lon', 'STRING', '31'),
                  ('owner', 'STRING', '63'),
                  ('serialNumber', 'STRING', '63'),
                  ('barCode', 'STRING', '31'),
                  ('manufacturer', 'STRING', '31'),
                  ('model', 'STRING', '31'),
                  ('firmwareVersion', 'STRING', '31'),
                  ('depth', 'STRING', '31'),
                  ('description', 'STRING', '255'),
                  ('createdAt', 'STRING', '31'),
                  ('createdBy', 'STRING', '31'),
                  ]


class Gage(B):
    def __init__(self, rowStr):
        aDict = json.loads(rowStr)
        self.mongo_id = aDict[B._map('mongo_id')]
        self.stationId =  aDict.get('stationId', None)
        self.gageNumber =  aDict.get('gageNumber', None)
        self.gageName =  aDict.get('gageName', None)
        self.gageType =  aDict.get('gageType', None)
        self.lat = float(aDict.get('lat', '0.0'))
        self.lon = float(aDict.get('lon', '0.0'))
        self.owner =  aDict.get('owner', None)
        self.serialNumber =  aDict.get('serialNumber', None)
        self.barCode =  aDict.get('', None)
        self.manufacturer =  aDict.get('manufacturer', None)
        self.model =  aDict.get('model', None)
        self.firmwareVersion =  aDict.get('firmwareVersion', None)
        self.depth =  aDict.get('depth', None)
        if self.depth is not None and isinstance(self.depth, dict): # it is another json object, so unpack
            try:
                tempD = json.loads(self.depth)
                self.depth = tempD.values()[0]
            except Exception as ex:
                self.depth = None

        self.description =  aDict.get('description', None)
        self.createdAt =  aDict.get('createdAt', None)
        self.createdBy =  aDict.get('createdBy', None)

        self._cleanUpNAs()
        if self.createdAt is not None:
            self.createdAt = self.createdAt['$date']

    @staticmethod
    def getRequiredFieldsTuples():
        return requiredFields

    @staticmethod
    def getRequiredFieldNames():
        retList = ['SHAPE@XY']
        retList.extend([val[0] for val in requiredFields])
        return retList

    def createOrUpdateRow(self):
        '''
        :return: List containing all values of this gage to be
                used in creating a new gage row.
        '''
        retList = [(self.lon, self.lat)] # corresponds to 'SHAPE@XY'
        for fieldName in Gage.getRequiredFieldNames()[1:]:
            aValue = self.__dict__[fieldName]
            retList.append(aValue)
        return retList


def GetAllGagesDict(pathFN):
    returnDict = {}
    with open(pathFN, 'r') as theFile:
        allLines = theFile.readlines()

    for aRow in allLines:
        aStation = Gage(aRow)
        returnDict[aStation.id] = aStation

    return returnDict

# def getGagesFieldList():
#     '''
#     Retrieves the list of fields to be updated for a Gage Row.
#     Using this every time ensures that the order of fields is always the same.
#     '''
#     retList = [val[0] for val in requiredFields]
#     return retList


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


