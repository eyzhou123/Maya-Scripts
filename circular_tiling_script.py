import maya.cmds as cmds
from functools import partial
import random

numToMake = 20
object = cmds.ls(selection = True)
width = cmds.getAttr("%s.distance" % (cmds.listRelatives("distanceDimension1", shapes = True)[0]))

for num in xrange(numToMake - 1):
    dupObj = cmds.duplicate(object)
    cmds.xform(dupObj[0], translation = [width, 0, 0], relative = True, objectSpace = True)
    cmds.xform(dupObj[0], rotation = [0, 360/numToMake, 0], relative = True)
    object = dupObj
