
import json
from collections import defaultdict
from frfSensorEntry import frfSensorEntry

import arcpy
print arcpy.env.workspace
mxd = arcpy.mapping.MapDocument(r"D:\NCSU\201801 Spring 2018\GIS 590 Capstone Project\Sandbox\attempt 2\arcmapStuff\Testbed.mxd")
print arcpy.mapping.ListLayers(mxd)
print arcpy.env.workspace

exit(0)

fileToOpn = r'D:\NCSU\201801 Spring 2018\GIS 590 Capstone Project\Sandbox\attempt 2\data\frf.json'

allData = []

with open(fileToOpn, 'r') as inFile:
    allLines = inFile.readlines()
    for aLine in allLines:
        rowDict = json.loads(aLine)
        allData.append(rowDict)

# allKeys = set()
# for aRow in allData:
#     allKeys = allKeys.union(set(aRow))

sumDict = defaultdict(lambda: [])
for aDict in allData:
    for key, val in aDict.iteritems():
        sumDict[key].append(val)

# allKeys = list(allKeys)
# for i in range(0, len(allKeys), 3):
#     print allKeys[i], allKeys[i+1], allKeys[i+2]

docCount = 0
allDataAsObjs = []
for aRow in allData:
    print
    rowObj = frfSensorEntry(aRow, docCount)
    allDataAsObjs.append(rowObj)
    docCount += 1
    rowObj.prettyPrint()

stationsDict = defaultdict(lambda: [])
for aStation in allDataAsObjs:
    stationsDict[(aStation.lat, aStation.lon)].append(aStation)
    # stationsDict[aStation.stationId].append(aStation)

latLonDicts = defaultdict(lambda: defaultdict(lambda : []))
for k, v in stationsDict.iteritems():
    for item in v:
        tDict = latLonDicts[k]
        latLonDicts[k][item.station].append(item)
        # latLonDicts[k].add(item.stationId)

# print latlons and their stations
print len(stationsDict)
for k, v in latLonDicts.iteritems():
    print k, v

# get gage to gageId matching
gageDict = defaultdict(lambda: [])
for aGage in allDataAsObjs:
    gageDict[aGage.gage].append(aGage.stationId)

for k,v in gageDict.iteritems():
    print k, v

projectDict = defaultdict(lambda: set())
for item in allDataAsObjs:
    projectDict[item.projectId].add(item.project)

print ' ---'
for k, v in projectDict.iteritems():
    print k, v

titles = set()
for item in allDataAsObjs:
    titles.add(item.title)
print titles

# sortedVals = sorted(sumDict.items(), key=lambda val: len(val))
# sortedLens = [(k, len(v)) for k, v in reversed(sortedVals)]
# print sortedLens

# Print all events per sensor, order by time not required.
gageDict = defaultdict(lambda: [])
for aGage in allDataAsObjs:
    gageDict[(aGage.gage, aGage.station)].append((aGage.start, aGage.status))

for gk, gv in gageDict.iteritems():
    if gk[1]!= 'CS01':
        continue
    print gk, ":"
    if gv is None:
        print "   None"
        continue

    try:
        # from https://stackoverflow.com/a/15837097/1339950
        gv.sort(key=lambda tpl: tpl[0])
        for val in gv:
            print "  ", val

    except:
        pass



