'''
Intended to be run from the Python window of an arcMap session.
Only.
'''
import sys, arcpy
mxd = arcpy.mapping.MapDocument('CURRENT')
layrs = arcpy.mapping.ListLayers(mxd)
staLyr = layrs[0]
sys.path.append("C:\SourceCode\Python\SMSbridge2PostGreSQL")
# from BridgeMongo2PostGreSQL import deleteAllFields
# deleteAllFields(staLyr, True)

