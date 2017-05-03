import maya.cmds as cmds
import time
import maya.OpenMaya as OpenMaya

""" PYTHON VERSION
vtxWorldPosition = []
object = cmds.ls(sl=True)[0]
print "Object: " + object
vtxIndexList = cmds.polyEvaluate(object, vertex = True)

for v in xrange(num_verts):
    vert_name = object + '.vtx[' + str(v) + ']'
    vert_pos = cmds.xform(vert_name, query = True, translation = True)
    vtxWorldPosition.append(vert_pos)
    
print vtxWorldPosition
print "This takes", (time.time() - startTime), "seconds."
    
"""

### API version ###

selection = OpenMaya.MSelectionList() # create variable 'selection' of type 'MSelectionList'
#print selection # this will print an instance of type 'MSelectionList'
OpenMaya.MGlobal.getActiveSelectionList(selection) # 'selection' is where you want the output to be stored
iterSel = OpenMaya.MItSelectionList(selection, OpenMaya.MFn.kMesh) # class for iterating over items in 'MSelectionList'

while not iterSel.isDone():
    startTime = time.time()
    # get dagPath
    dagPath = OpenMaya.MDagPath()
    iterSel.getDagPath(dagPath)
    print dagPath.fullPathName()
    
    # create empty point array
    inMeshMPointArray = OpenMaya.MPointArray()
    
    # create function set and get points
    currentInMeshMFnMesh = OpenMaya.MFnMesh(dagPath)
    currentInMeshMFnMesh.getPoints(inMeshMPointArray, OpenMaya.MSpace.kWorld)
    
    # put each point in a list
    pointList = []
    
    for i in range(inMeshMPointArray.length()):
        pointList.append([inMeshMPointArray[i][0], inMeshMPointArray[i][1], inMeshMPointArray[i][2]])
    
    print pointList
    print "This takes", (time.time() - startTime), "seconds."
    iterSel.next()