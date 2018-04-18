'''
Accepts data from .json files consisting of multiple JSON objects where
the .json file was generated from MongoDB via a data dump.
Parses the JSON objects and populates a feature class and two tables
with data from them.

The feature store may be of either kind, gdb or PostGres database. They are accessed
through map layers via arcpy, so adapting API calls to what kind of feature store
is taken care of by arcpy.

From the command line ...
To run prepared test scenarios (under if __name__ == '__main__), call this module
with alone with no parameters.

To run the module on the dataset of your choosing, call the module with the full
path to the map document you want to operate on, such as
   python BridgeMongo2PostGreSQL "C:\scratch\My Map.mxd"
'''
print 'started'
import arcpy
import os, json
from station import Station
from gage import Gage
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

def ensureTableLayerHasFields(layerObj, requiredFieldList):
    myDataSource = layerObj.dataSource
    existingFields = arcpy.ListFields(myDataSource)
    existFNames = [f.name for f in existingFields]
    for requiredField in requiredFieldList:
        fieldName = requiredField[0]
        if fieldName not in existFNames:
            fieldType = requiredField[1]
            fLen = requiredField[2]
            try:
                arcpy.AddField_management(layerObj, fieldName, fieldType,
                                      field_length=fLen)
            except:
                i = 0

def initializeTables(mxd):
    lyrDict = getLayersDict(mxd)
    lyrStations = lyrDict[lyrStationsName]
    workingGdb = os.path.dirname(lyrStations.dataSource)

    try:
        ensureTableLayerHasFields(lyrStations,
                                  Station.getRequiredFieldsTuples())
    except:
        pass

    try:
        fullPath = os.path.join(workingGdb, tblGages)
        ensureTableLayerHasFields(fullPath,
                                  Gage.getRequiredFieldsTuples())
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
    if layerObj is None: return
    if 'STATIO' in theType.upper():
        ensureTableLayerHasFields(layerObj, Station.getRequiredFieldsTuples())
    elif 'GAGE' in theType.upper():
        ensureTableLayerHasFields(layerObj, Gage.getRequiredFieldsTuples())

def readStationsJson(stationsFileName):
    if stationsFileName is None: return {}
    stationsDict = {}
    try:
        with open(stationsFileName, 'r') as inFile:
            allLines = inFile.readlines()
            for aLine in allLines:
                aStation = Station(aLine)
                stationsDict[aStation._id] = Station(aLine)
    except:
        return {}

    return stationsDict

def readGagesJson(gagesFileName):
    if gagesFileName is None: return {}
    gagesDict = {}
    try:
        with open(gagesFileName, 'r') as inFile:
            allLines = inFile.readlines()
            for aLine in allLines:
                aGage = Gage(aLine)
                gagesDict[aGage._id] = aGage
    except:
        return {}

    return gagesDict

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
    if stationsLayer is None or len(stationsDict) == 0:
        return

    fieldList = Station.getRequiredFieldNames()
    ensureAllColumns(stationsLayer, 'stations')
    deleteAllRows(stationsLayer)

    # write the new stations to the Layer
    with arcpy.da.InsertCursor(stationsLayer, fieldList) as cursor:
        for stationID, aStation in stationsDict.iteritems():
            rowList = aStation.createOrUpdateRow()
            cursor.insertRow(rowList)
    del cursor

def updateGages(gagesTable, gagesDict):
    if gagesTable is None or len(gagesDict) == 0:
        return

    fieldList = Gage.getRequiredFieldNames()
    ensureAllColumns(gagesTable, 'gages')
    deleteAllRows(gagesTable)

    # write the new stations to the Layer
    with arcpy.da.InsertCursor(gagesTable, fieldList) as cursor:
        for gageID, aGage in gagesDict.iteritems():
            try:
                cursor.insertRow(aGage.createOrUpdateRow())
            except Exception as ex:
                i = 0
    del cursor

def bridgeAllJsonDumpsToArcTables(stationsLayer, stationsJsonName,
                     gagesTable, gagesJsonName):
    '''
    This is the main function of the module. Call this to do what you want to do.
    Given the parameters, bridge the data from the MongoDb Json dump file (which is the
    input) to the ArcGIS tables behind the layers.
    :param stationsLayer: Map Layer of the Stations feature class to populate
    :param stationsJsonName: File name of the MongoDb Json Dump to be bridged for Station data
    :param gagesTable: Table View of the Gages table to populate
    :param gagesJsonName: File name of the MongoDb Json Dump to be bridged for Gage data
    :return: None
    '''
    stationsDict = readStationsJson(stationsJsonName)
    updateStations(stationsLayer, stationsDict)
    gagesDict = readGagesJson(gagesJsonName)
    updateGages(gagesTable, gagesDict)

def getTableByName(theMxd, tableName):
    '''
    Given a map document object and the name of a table view in that map,
    return the tableView object.
    :param theMxd: The Map Document Object where to find the table view.
    :param tableName: The name (string) of the Table View.
    :return:
    '''
    tbls = arcpy.mapping.ListTableViews(theMxd)
    return _getFirstOrDefault(
        [tbl for tbl in tbls if tbl.name == tableName])

def getLayerByName(theMxd, layerName):
    '''
    Given a map document object and the name of a table view in that map,
    return the tableView object.
    :param theMxd: The Map Document Object where to find the table view.
    :param layerName: The name (string) of the Table View.
    :return:
    '''
    lyrs = arcpy.mapping.ListLayers(theMxd)
    return _getFirstOrDefault(
        [lyr for lyr in lyrs if lyr.name == layerName])

if __name__ == '__main__':

    testDir = 'Data/arcmapStuff'
    cwd = os.getcwd()
    testFullPath = os.path.join(cwd, testDir)
    mapFileName = os.path.join(testFullPath, 'testBed.mxd')

    # swap the next two lines commented status to test different file sets.
    # frfDir = os.path.join(cwd, 'Data/FRFdata')
    frfDir = os.path.join(cwd, 'Data/SMS_json_v20180412')
    stationsFname = os.path.join(frfDir, 'stations.json')

    stationsJsonDump = os.path.join(testFullPath, stationsFname)
    gagesFname = os.path.join(frfDir, 'gages.json')
    gagesJsonDump = os.path.join(testFullPath, gagesFname)

    # mxd = arcpy.mapping.MapDocument(mapFileName)
    # stationsLayer = _getFirstOrDefault(
    #     [L for L in arcpy.mapping.ListLayers(mxd)
    #         if L.name == 'Station'])
    #
    mxd = arcpy.mapping.MapDocument(mapFileName)

    stationsLayer = getLayerByName(mxd, 'Station')
    gagesTable = getTableByName(mxd, 'tbl_gages')

    bridgeAllJsonDumpsToArcTables(stationsLayer, stationsJsonDump,
                     gagesTable, gagesJsonDump)

    # print arcpy.GetCount_management(stationsLayer), 'before deleteAllRows'
    # deleteAllRows(stationsLayer)
    # print arcpy.GetCount_management(stationsLayer), 'after deleteAllRows'

    print 'Done'




