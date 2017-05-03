import maya.cmds as cmds

sel = cmds.ls(selection = True)
ctrl = sel[0]
jnt = sel[1]

jntRot = cmds.xform(jnt, query = True, rotation = True)

dupTransform = cmds.duplicate(ctrl)
dupCurve = cmds.listRelatives(dupTransform, children=True)
cmds.delete(dupCurve)

cmds.parent(ctrl, dupTransform)