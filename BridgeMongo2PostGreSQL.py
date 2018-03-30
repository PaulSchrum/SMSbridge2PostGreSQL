'''
Accepts data from a ??? file consisting of multiple JSON objects where
the ??? file was generated from MongoDB via a data dump.
Parses the JSON objects and populates a feature class and two tables
with data from them.
'''

import arcpy

lyrStations = 'Stations'
tblGages = 'Gages'
tblStatuses = 'Statuses'





