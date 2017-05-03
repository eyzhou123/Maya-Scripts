import maya.cmds as cmds
from functools import partial
import random

# Get all the selected architecture pieces and store them into a list
def storeSelectedPieces(*args):
    global architectureList
    architectureList = []
    for eachTrans in cmds.ls(type="transform", selection=True):
            for eachChild in cmds.listRelatives(eachTrans, children=True, fullPath=True):
                if cmds.nodeType(eachChild)=="mesh":
                    if eachTrans not in architectureList:
                        architectureList.append(eachTrans)
    print architectureList
    if architectureList == []:
        cmds.warning("No pieces were stored.")
       

# Generate pieces by duplicating and placing at random vertex positions on the chosen plane
# Use the plane vertex height information to place the object at the right height
def makeRandomPieces(intFieldValue, planeNameField, *args):
    numToMake = cmds.intField(intFieldValue, query=True, value=True)
    planeName = cmds.textField(planeNameField, query=True, text=True)
    print planeName
    if architectureList != []:
        print "Generating " + str(numToMake) + " pieces..."
        for numToGenerate in xrange(numToMake):
            # Get random index in architecture list
            randInd = random.randint(0, len(architectureList) - 1)
            numVerts = cmds.polyEvaluate(planeName, vertex = True)
            randVert = random.randint(0, numVerts - 1)
            randVertName = planeName + ".vtx[" + str(randVert) + "]"
            vertPos = cmds.xform(randVertName, query = True, worldSpace = True, translation = True)
         
            dupPiece = cmds.duplicate(architectureList[randInd])
            cmds.xform(dupPiece[0], rotation = [0, random.randint(0, 360), 0], relative = True)
            
            currentPos = cmds.getAttr(dupPiece[0] + '.translate')[0]
            cmds.move(vertPos[0],vertPos[1]+currentPos[1],vertPos[2], dupPiece[0], absolute=True)
    else:
        cmds.error("Store pieces first.")

# Generate terrain by randomizing the y coordinate of all vertices in the selected plane
def randomizePlaneVerts(minElField, maxElField, *args):  
    minY = cmds.intField(minElField, query=True, value=True)
    maxY = cmds.intField(maxElField, query=True, value=True) 
    if cmds.ls(selection = True) != []:
        # Generate terrain
        terrainPlane = cmds.ls(selection = True)[0]
        numVerts = cmds.polyEvaluate(terrainPlane, vertex = True)
        print terrainPlane
        for vert in xrange(numVerts):
            randY = random.uniform(minY, maxY)
            vertName = terrainPlane + ".vtx[" + str(vert) + "]"
            currentVertPos = cmds.xform(vertName, query = True, worldSpace = True, translation = True)
            #print currentVertPos
            cmds.polyMoveVertex(vertName, translateY=randY)
        cmds.polySmooth(terrainPlane, kb=1 )
        numVerts = cmds.polyEvaluate(terrainPlane, vertex = True)
    else:
        cmds.error("Select a plane to use.")

# UI
def createWin():
    winName = "GenerateTerrainWindow"
    versionNum = 0.1
   
    if cmds.window(winName, exists = True):
        cmds.deleteUI(winName)
        
    cmds.window(winName, sizeable=True, titleBar=True, resizeToFitChildren=False, 
    menuBar=True, widthHeight = (450,500), title="Generate Landscape Window " + str(versionNum))
    cmds.scrollLayout(horizontalScrollBarThickness=16, verticalScrollBarThickness=16)
    cmds.columnLayout(columnAttach=('left',5), rowSpacing=10, columnWidth=250)
    
    # Start of widgets
    
    # ----- Terrain Generation ----- #
    cmds.text(label = "------------------------------ Terrain Generator ------------------------------", width = 500)
    
    cmds.rowLayout(numberOfColumns = 5, columnWidth5 = (50,75,75,75,75), columnAlign=(1,'center'))
    cmds.text(label = " Min elevation: ", width = 150)
    minElField = cmds.intField(value = -5, editable = True)
    cmds.setParent("..")
    
    cmds.rowLayout(numberOfColumns = 5, columnWidth5 = (50,75,75,75,75), columnAlign=(1,'center'))
    cmds.text(label = " Max elevation: ", width = 150)
    maxElField = cmds.intField(value = 10, editable = True)
    cmds.setParent("..")
    
    cmds.rowLayout(numberOfColumns = 5, columnWidth5 = (50,75,75,75,75), columnAlign=(1,'center'))
    cmds.button(label = "Generate Terrain", width = 150, command = partial(randomizePlaneVerts, minElField, maxElField))
    cmds.text(label = " Select the plane that you wish to use, then click 'Generate Terrain'")
    cmds.setParent("..")
    
    # ----- Object Generation ----- #
    cmds.text(label = "------------------------------ Object Generator ------------------------------", width = 500)
    
    cmds.rowLayout(numberOfColumns = 5, columnWidth5 = (50,75,75,75,75), columnAlign=(1,'center'))
    cmds.button(label = "Store Pieces", width = 150, command = partial(storeSelectedPieces))
    cmds.text(label = " Select the architecture objects that you wish to include, then click 'Store Pieces'")
    cmds.setParent("..")
    
    cmds.rowLayout(numberOfColumns = 5, columnWidth5 = (50,75,75,75,75), columnAlign=(1,'center'))
    cmds.text(label = " # objects to generate: ", width = 150)
    intFieldVal = cmds.intField(value = 5, minValue = 0, maxValue = 50, editable = True)
    cmds.setParent("..")
    
    cmds.rowLayout(numberOfColumns = 5, columnWidth5 = (50,75,75,75,75), columnAlign=(1,'center'))
    cmds.text(label = " Name of ground plane: ", width = 150)
    planeNameField = cmds.textField(text = "ground_plane", editable = True)
    cmds.setParent("..")
    cmds.button(label = "Generate Architecture", width = 150, command = partial(makeRandomPieces, intFieldVal, planeNameField))
    
    
    cmds.text(label = "------------------------------------------------------------------------------", width = 500)
  
    cmds.showWindow()


createWin()

   