
import json
from collections import defaultdict

class frfSensorEntry:
    def __init__(self, inDict, docCount=0):
        inDict = defaultdict(lambda: '', inDict)
        self.id_ = inDict['_id']
        self.assigned = inDict['assigned']
        self.comments = inDict['comments']
        self.createdAt = inDict['createdAt']
        self.end = inDict['end']
        self.endTime = inDict['endTime']
        self.gage = inDict['gage']
        self.gageId = inDict['gageId']
        self.lat = inDict['lat']
        self.lon = inDict['lon']
        self.pictures = inDict['pictures']
        self.project = inDict['project']
        self.projectId = inDict['projectId']
        self.start = inDict['start']
        self.startTime = inDict['startTime']
        self.station = inDict['station']
        self.stationId = inDict['stationId']
        self.status = inDict['status']
        self.title = inDict['title']
        self.type = inDict['type']
        self.updatedAt = inDict['updatedAt']
        self.updatedBy = inDict['updatedBy']
        self.waterDepth = inDict['waterDepth']
        self.docCount = docCount

    def prettyPrint(self):
        print \
"""docCount: {6}
   Station: {0}
   Lat: {1}
   Lon: {2}
   Status: {3}  Start: {6} {7}
                 End:   {8} {9}
   Gage Id: {4}
   Title: {5}""". \
            format(self.station, self.lat, self.lon, self.status,
                   self.gageId, self.title, self.start, self.startTime,
                   self.end, self.endTime, self.docCount)


