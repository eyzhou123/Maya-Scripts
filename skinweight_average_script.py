import maya.cmds as cmds
import maya.mel as mel

v1 = cmds.ls(sl=True)[0]
v2 = cmds.ls(sl=True)[1]

print v1
print v2

mesh1 = str(v1).split('.')[0]
mesh2 = str(v2).split('.')[0]
print mesh1
print mesh2

cluster1 = mel.eval('findRelatedSkinCluster ' + mesh1) 
cluster2 = mel.eval('findRelatedSkinCluster ' + mesh2) 
print cluster1
print cluster2

weight1 = cmds.skinPercent(cluster1, v1,  q = True, value = True)
weight2 = cmds.skinPercent(cluster2, v2, q = True, value = True)
"""print weight1
print weight2

print len(weight1)
print len(weight2)"""

joint_list =  cmds.ls(type = "joint")

w_average = []
for i in range(len(joint_list)):
    w1 = cmds.skinPercent(cluster1, v1, q=True, v=True, t=joint_list[i])
    w2 = cmds.skinPercent(cluster2, v2, q=True, v=True, t=joint_list[i])
    avg = (w1+w2)/2
    w_average.append((joint_list[i], avg))
    #w_average.append(avg)

#print "----AVERAGE----"
#print w_average

cmds.skinPercent(cluster1, v1, transformValue=w_average)
cmds.skinPercent(cluster2, v2, transformValue=w_average)

print "---------------------------------------------------------"

new_weight1 = cmds.skinPercent(cluster1, v1,  q = True, value = True)
new_weight2 = cmds.skinPercent(cluster2, v2, q = True, value = True)

print new_weight1
print new_weight2