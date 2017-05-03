import maya.cmds as cmds
from functools import partial

def testFunc(input, *args): # print the input
    print input

def getAllTransFromScene():
    meshTransList = []

    for eachTrans in cmds.ls(type="transform"):
        for eachChild in cmds.listRelatives(eachTrans, children=True, fullPath=True):
            if cmds.nodeType(eachChild)=="mesh":
                if eachTrans not in meshTransList:
                    meshTransList.append(eachTrans)
                    
    return meshTransList

def transformCheck(eachTrans): # use the return list to make buttons, eg: Fix Translate
    attrToCheck = [["translate", [(0,0,0)]], ["rotate", [(0,0,0)]], ["scale", [(1,1,1)]]]
    attrInvalidList = []
    
    for eachAttr in attrToCheck:
        if cmds.getAttr("%s.%s" %(eachTrans, eachAttr[0])) != eachAttr[1]:
            attrInvalidList.append(eachAttr[0])
    return attrInvalidList

def freezeTrans(channel, *args): # function to fix zero out
    #print channel
    if channel == "translate":
        cmds.makeIdentity(apply = True, translate = True)
    if channel == "rotate":
        cmds.makeIdentity(apply = True, rotate = True)
    if channel == "scale":
        cmds.makeIdentity(apply = True, scale = True)
       
def selectLabeledTrans(trans, *args):
    cmds.select(trans, replace = True)
    
def createWin():
    winName = "inspectSceneWindow"
    versionNum = 0.1
    
    if cmds.window(winName, exists = True):
        cmds.deleteUI(winName)
        
    cmds.window(winName, sizeable=True, titleBar=True, resizeToFitChildren=False, 
    menuBar=True, widthHeight = (450,500), title="Inspect Scene Window " + str(versionNum))
    cmds.scrollLayout(horizontalScrollBarThickness=16, verticalScrollBarThickness=16)
    cmds.columnLayout(columnAttach=('left',5), rowSpacing=10, columnWidth=250)
    
    #cmds.button(label = "Test", command = partial(testFunc, "hey"))
    meshTransList = getAllTransFromScene()
    #print meshTransList
    
    for eachTrans in meshTransList:
        cmds.rowLayout(numberOfColumns = 5, columnWidth5 = (50,75,75,75,75), columnAlign=(1,'center'))
        cmds.text(label = eachTrans)
        cmds.button(label = "Select", width = 150, command = partial(selectLabeledTrans, eachTrans))
        
        if transformCheck(eachTrans): # exists non zeroed out values
            for eachWrongAttr in transformCheck(eachTrans):
                cmds.button(label = "Fix " + eachWrongAttr, width = 150, command = partial(freezeTrans, eachWrongAttr))
            
        cmds.setParent("..")
    
    cmds.showWindow()


createWin()