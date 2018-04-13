'''
Accepts data from a ??? file consisting of multiple JSON objects where
the ??? file was generated from MongoDB via a data dump.
Parses the JSON objects and populates a feature class and two tables
with data from them.
'''
print 'started'
import arcpy
import os, json
from station import Station
from station import requiredFields as staRequiredFields
from station import getStationsFieldList as staGetStationsFieldList
from gage import Gage
from gage import requiredFields as gageRequiredFields
print 'imports complete'

mxd = None
lyrStationsName = 'Stations'
tblGages = 'tbl_gages'
tblStatuses = 'tbl_statuses'


def deleteAllFields(layerObj, shouldRun=False):
    '''
    WARNING: Destructive Function. Use only for development
    Removes fields from a given feature class or db file through
    a layer object.
    Removes everything but OID and @Shape.
    :param layerObj: The layer to delete fields from
    :return: None
    '''
    if shouldRun == False:
        return

    if layerObj is None:
        return None
    lst = []
    try:
        lst = arcpy.ListFields(layerObj)
    except:
        lst = arcpy.ListFields(layerObj.dataSource)
    if len(lst) == 0:
        return None

    fieldList = [fld.name.upper() for fld in lst]
    fieldList = [fldName for fldName in fieldList
                 if not (fldName == 'OBJECTID' or
                    fldName == 'SHAPE')]
    if len(fieldList) == 0:
        return None
    arcpy.DeleteField_management(layerObj, fieldList)


def deleteAllRows(layerObj):
    '''
    Deletes all rows of a table or feature class.
    WARNING: This function deletes ALL ROWS of a table or feature class.
    If you call it, there is no oopsie.
    :param layerObj: The Layer to have all rows deleted from.
    :return: None
    '''
    with arcpy.da.UpdateCursor(layerObj, "OBJECTID") as tbl:
        for row in tbl:
            tbl.deleteRow()

def getLayerIndex(lyrList, layerName):
    lyrNames = [L.name for L in lyrList]
    return lyrNames.index(layerName)

def getLayersDict(mxd):
    returnDict = {}
    layers = arcpy.mapping.ListLayers(mxd)
    for lyr in layers:
        returnDict[lyr.name] = lyr
    return returnDict

def getGDBfromDataSource(layer):
    delim = '\\'

def ensureTableLayerHasFields(layerObj, fieldList):
    myDataSource = layerObj
    aType = type(layerObj)
    useless = 'hi'
    bType = type(useless)
    if not(isinstance(layerObj, basestring)):
        myDataSource = layerObj.dataSource
    existingFields = arcpy.ListFields(myDataSource)
    names = [f.name for f in existingFields]
    for requiredField in fieldList:
        fieldName = requiredField[0]
        if fieldName not in names:
            fieldType = requiredField[1]
            fLen = requiredField[2]
            arcpy.AddField_management(layerObj, fieldName, fieldType,
                                      field_length=fLen)

def initializeTables(mxd):
    lyrDict = getLayersDict(mxd)
    lyrStations = lyrDict[lyrStationsName]
    workingGdb = os.path.dirname(lyrStations.dataSource)

    try:
        ensureTableLayerHasFields(lyrStations, staRequiredFields)
    except:
        pass

    try:
        fullPath = os.path.join(workingGdb, tblGages)
        ensureTableLayerHasFields(fullPath, gageRequiredFields)
    except:
        pass

    print 'tables initialized'

def _getFirstOrDefault(aCollection):
    '''
    return the first item of a list or tuple.
    :param aCollection: The list or tuple to use
    :return: The first item in the list. If aCollection is
        None, it returns None. If the aCollection is empty,
        it returns None.
    '''
    if aCollection is None:
        return None

    # from https://stackoverflow.com/a/365934/1339950
    return next(iter(aCollection), None)

def ensureAllColumns(layerObj, theType=''):
    if theType == '': return
    if 'STATIO' in theType.upper():
        ensureTableLayerHasFields(layerObj, staRequiredFields)
    elif 'GAGE' in theType.upper():
        ensureTableLayerHasFields(layerObj, gageRequiredFields)

def readStationsJson(stationsFileName):
    stationsDict = {}
    with open(stationsFileName, 'r') as inFile:
        allLines = inFile.readlines()
        for aLine in allLines:
            # rowDict = json.loads(aLine)
            aStation = Station(aLine)
            stationsDict[aStation._id] = aStation

    return stationsDict

def getAllIds(layerObj):
    '''
    For the given layer object, return a set of all _id's in the
    Attribute Table underlying the layer.
    :param layerObj:
    :return: set of all _id values
    '''
    idSet = set()
    with arcpy.da.SearchCursor(layerObj, ['_id']) as cursor:
        for row in cursor:
            idSet.add(row[0])
    del cursor
    return idSet

def updateStations(stationsLayer, stationsDict):
    deleteAllRows(stationsLayer)

    fieldList = staGetStationsFieldList()

    # write the new stations to the Layer
    with arcpy.da.InsertCursor(stationsLayer, fieldList) as cursor:
        for stationID, aStation in stationsDict.iteritems():
            rowList = aStation.createOrUpdateRow()
            cursor.insertRow(rowList)
    del cursor

def readAllJsonDumps(stationsLayer, stationsName): #, gagesName):
    stationsDict = readStationsJson(stationsName)
    updateStations(stationsLayer, stationsDict)

if __name__ == '__main__':
    testDir = 'Data/arcmapStuff'
    cwd = os.getcwd()
    testFullPath = os.path.join(cwd, testDir)
    mapFileName = os.path.join(testFullPath, 'testBed.mxd')
    # frfDir = os.path.join(cwd, 'Data/FRFdata')
    frfDir = os.path.join(cwd, 'Data/SMS_json_v20180412')
    stationsFname = os.path.join(frfDir, 'stations.json')
    stationsJsonDump = os.path.join(testFullPath, stationsFname)

    mxd = arcpy.mapping.MapDocument(mapFileName)
    stationsLayer = _getFirstOrDefault(
        [L for L in arcpy.mapping.ListLayers(mxd)
            if L.name == 'Station'])
    # deleteAllFields(stationsLayer, shouldRun=True)
    stationFields = arcpy.ListFields(stationsLayer.dataSource)
    if len(stationFields) <= 2:
        ensureTableLayerHasFields(stationsLayer, staRequiredFields)
    # deleteAllRows(stationsLayer)
    readAllJsonDumps(stationsLayer, stationsJsonDump)

    # print arcpy.GetCount_management(stationsLayer), 'before deleteAllRows'
    # deleteAllRows(stationsLayer)
    # print arcpy.GetCount_management(stationsLayer), 'after deleteAllRows'

    print 'Done'




