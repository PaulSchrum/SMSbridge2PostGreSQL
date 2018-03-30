'''
Accepts data from a ??? file consisting of multiple JSON objects where
the ??? file was generated from MongoDB via a data dump.
Parses the JSON objects and populates a feature class and two tables
with data from them.
'''
print 'started'
import arcpy
print 'imports complete'

mxd = None
mxdPath = r'D:\NCSU\201801 Spring 2018\GIS 590 Capstone Project\Sandbox\attempt 2\arcmapStuff\Testbed.mxd'
lyrStationsName = 'Stations'
tblGages = 'Gages'
tblStatuses = 'Statuses'

stationRequiredFields = [('stationName', 'STRING', '31'),
                          ('projectName', 'STRING', '31'),
                          ('WaterDepth', 'SINGLE', '')]

gagesRequiredFields = [('gageId', 'STRING', '31'),
                       ('gageModelName', 'STRING', '31'),
                       ('gageModelName', 'STRING', '31'),
                       ('assigned', 'STRING', '31'),
                       ('comments', 'STRING', '63'),
                       ('createdAt', 'DATE', ''),
                       ('title', 'STRING', '31')]

statusesRequiredFields = [('statusId', 'STRING', '31'),
                          ('gageId', 'STRING', '31'),
                          ('status', 'STRING', '31'),
                          ('startTime', 'DATE', ''),
                          ('endTime', 'DATE', ''),
                          ('updatedAt', 'DATE', ''),
                          ('updatedBy', 'STRING', '31')]



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

def ensureTableLayerHasFields(layerObj, fieldList):
    existingFields = arcpy.ListFields(layerObj.dataSource)
    names = [f.name for f in existingFields]
    for requiredField in fieldList:
        fieldName = requiredField[0]
        if fieldName not in names:
            fieldType = requiredField[1]
            fLen = requiredField[2]
            arcpy.AddField_management(layerObj, fieldName, fieldType,
                                      field_length=fLen)

    print existingFields

if __name__ == '__main__':
    mxd = arcpy.mapping.MapDocument(mxdPath)
    layers = arcpy.mapping.ListLayers(mxd)
    lyrIndex = getLayerIndex(layers, lyrStationsName)
    lyrStations = layers[lyrIndex]
    print lyrStations.name
    # print arcpy.GetCount_management(lyrStations), 'before deleteAllRows'
    # deleteAllRows(lyrStations)
    # print arcpy.GetCount_management(lyrStations), 'after deleteAllRows'

    ensureTableLayerHasFields(lyrStations, stationRequiredFields)
    print 'Done'




