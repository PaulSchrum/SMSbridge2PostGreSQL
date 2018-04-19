'''
Intended to be run from the Python window of an arcMap session.
Only.
'''
import sys, arcpy
mxd = arcpy.mapping.MapDocument(r"D:\SourceModules\Python\SMSbridge2PostGreSQL\Data\arcmapStuff\Testbed.mxd")
# mxd = arcpy.mapping.MapDocument("CURRENT")
layrs = arcpy.mapping.ListLayers(mxd)
staLyr = layrs[0]
sys.path.append(r"D:\SourceModules\Python\SMSbridge2PostGreSQL\BridgeMongo2PostGreSQL.py")
# sys.path.append(r"C:\SourceCode\Python\SMSbridge2PostGreSQL\BridgeMongo2PostGreSQL.py")
from BridgeMongo2PostGreSQL import deleteAllFields
deleteAllFields(staLyr, True)

