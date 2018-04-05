'''
Accepts data from a ??? file consisting of multiple JSON objects where
the ??? file was generated from MongoDB via a data dump.
Parses the JSON objects and populates a feature class and two tables
with data from them.
'''
print 'started'
import arcpy
import os
from station import Station
from gage import Gage
print 'imports complete'

mxd = None
lyrStationsName = 'Stations'
tblGages = 'tbl_gages'
tblStatuses = 'tbl_statuses'

stationRequiredFields = [('stationName', 'STRING', '31'),
                          ('projectName', 'STRING', '31'),
                          ('WaterDepth', 'SINGLE', '')]

gagesRequiredFields = [('gageId', 'STRING', '31'),
                       ('gageModelName', 'STRING', '31'),
                       ('stationName', 'STRING', '31'),
                       ('assigned', 'STRING', '31'),
                       ('comments', 'STRING', '63'),
                       ('createdAt', 'DATE', ''),
                       ('title', 'STRING', '31')]

def _deleteAllFields_development(layerObj, shouldRun=False):
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
    if len(lst) == 0:
        return None

    fieldList = [fld.name.upper() for fld in lst]
    arcpy.DeleteField_management(layerObj, fieldList)


def deleteAllRows(layerObj):
    '''
    Deletes all rows of a table or feature class.
    WARNING: This function deletes ALL ROWS of a table or feature class.
    If you calls it, there is no oopsie.
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
        ensureTableLayerHasFields(lyrStations, stationRequiredFields)
    except:
        pass

    try:
        fullPath = os.path.join(workingGdb, tblGages)
        ensureTableLayerHasFields(fullPath, gagesRequiredFields)
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

if __name__ == '__main__':
    testDir = 'Data/arcmapStuff'
    cwd = os.getcwd()
    testFullPath = os.path.join(cwd, testDir)
    mapFileName = os.path.join(testFullPath, 'testBed.mxd')

    mxd = arcpy.mapping.MapDocument(mapFileName)
    stationsLayer = _getFirstOrDefault(
        [L for L in arcpy.mapping.ListLayers(mxd)
            if L.name == 'Station'])
    temp = arcpy.ListFields(stationsLayer.dataSource)
    _deleteAllFields_development(stationsLayer, shouldRun=True)
    # initializeTables(mxd)

    # print arcpy.GetCount_management(lyrStations), 'before deleteAllRows'
    # deleteAllRows(lyrStations)
    # print arcpy.GetCount_management(lyrStations), 'after deleteAllRows'

    print 'Done'




