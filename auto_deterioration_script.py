import maya.cmds as cmds
from functools import partial
import random
import os, sys

# helper for noisePatch, eg: when given '.vtx[1:4]', returns [1,2,3,4]
def separateVertexInterval(start, end):
    separated = [start, end]
    for count in xrange(end-start):
        separated.append(start+count)
    return separated
    
# helper for noisePatch, gives neighbor vertices as list of vertex indices
def getNeighbors(object, vert):
    vert_name = object + ".vtx[" + str(vert) + "]"
    edges = cmds.polyListComponentConversion(vert_name, toEdge = True)
    neighbors = cmds.polyListComponentConversion( edges, toVertex = True)
    neighbors_ints = []
    for n in neighbors:
        value = n[n.find("[")+1:n.find("]")]
        if len(value.split(":")) == 1:
            #if int(value.split(":")[0]) != vert:
            neighbors_ints.append(int(value.split(":")[0]))
        else:
            separated = separateVertexInterval(int(value.split(":")[0]), int(value.split(":")[1]))
            print separated
            neighbors_ints = neighbors_ints + separated
    return neighbors_ints    

# helper for noisePatch, shift vertex position randomly
def applyNoise(object, vert, amount):
    noise_x = random.uniform(0, amount)
    noise_y = random.uniform(0, amount)
    noise_z = random.uniform(0, amount)
    cmds.polyMoveVertex(object + ".vtx[" + str(vert) + "]", 
        translateX = noise_x, translateY = noise_y, 
        translateZ = noise_z)

def noisePatches(num_patches_field, patch_size_field, noise_amount_field, *args):
    if (len(cmds.ls(sl=True)) == 0):
        cmds.error("You must have an object selected.")
    else:
        object = cmds.ls(sl=True)[0]
        print "Object: " + object
        num_verts = cmds.polyEvaluate(object, vertex = True)
        object_pos = cmds.xform(object, query = True, worldSpace = True, translation = True)
        object_scale = cmds.xform(object, query = True,relative=True, scale = True)
        
        num_decay_spots = cmds.intField(num_patches_field, query=True, value=True)
        num_decay_neighbors = cmds.intField(patch_size_field, query=True, value=True)
        noise_radius = cmds.floatField(noise_amount_field, query=True, value=True)
        
        spots = []
        new_spots = []
        for spot in range(num_decay_spots):
            # choose random vertex to be decay center, keep track
            rand_vert = random.randint(0, num_verts)
            print "Rand Vert Chosen: " + str(rand_vert)
            spots.append(rand_vert)
            
            applyNoise(object, rand_vert, noise_radius)
            
        iterations = 2 # keep at 2 for shorter run time
        for i in xrange(iterations):
            for spot in spots:
                print "spot: " + str(spot)
                neighbors = getNeighbors(object, spot)
                for n in range(min(num_decay_neighbors, len(neighbors))):
                    n = neighbors[random.randint(0, len(neighbors)-1)]
                    new_spots.append(n)
                    print "New neighbor: " + str(n)
                    # apply less noise for neighbors spread effect
                    applyNoise(object, n, noise_radius - 0.1*i)
                print spots
                print new_spots
            spots = new_spots
            new_spots = []

# helper for generateDents, finds avg face normals and calculate new inwards position
def findNewPosition(object, vert, push_dist):
    vert_name = object + '.vtx[' + str(vert) + ']'
    cmds.select(vert_name, replace = True)
    faces = cmds.polyListComponentConversion(vert_name, toFace = True)
    normals = cmds.polyInfo(faces, faceNormals = True)
    x_avg = 0
    y_avg = 0
    z_avg = 0
    for norm in normals:
        label, vertex, x, y, z = norm.split()
        x_avg += float(x)
        y_avg += float(y)
        z_avg += float(z)
    x_avg = x_avg/len(normals)
    y_avg = y_avg/len(normals)
    z_avg = z_avg/len(normals)
    print x_avg, y_avg, z_avg
    vert_pos = cmds.xform(vert_name, query = True, translation = True)
    print "-----"
    print vert_pos
    new_x = vert_pos[0] + -x_avg * push_dist
    new_y = vert_pos[1] + -y_avg * push_dist
    new_z = vert_pos[2] + -z_avg * push_dist
    print new_x, new_y, new_z
    print "------"
    return [new_x, new_y, new_z]
    
# helper for generateDents, moves vertex to new inward position
def pushVertexIn(object, vert, new_x, new_y, new_z):
    vert_name = object + '.vtx[' + str(vert) + ']'
    print "---"
    print vert_name
    cmds.xform(vert_name, translation = [new_x, new_y, new_z])
        
def generateDentsWrapper(dent_size_field, push_dist_field, dent_num_field, *args):
    if (len(cmds.ls(sl=True)) == 0):
        cmds.error("You must have an object selected.")
    else:
        dent_num = cmds.intField(dent_num_field, query=True, value=True)
        for i in range(dent_num):
            generateDents(dent_size_field, push_dist_field)
        
def generateDents(dent_size_field, push_dist_field):
    object = cmds.ls(sl=True)[0]
    print "Object: " + object
    num_verts = cmds.polyEvaluate(object, vertex = True)
    object_pos = cmds.xform(object, query = True, worldSpace = True, translation = True)
    object_scale = cmds.xform(object, query = True,relative=True, scale = True)
    
    dent_size = cmds.intField(dent_size_field, query=True, value=True)
    push_dist = cmds.floatField(push_dist_field, query=True, value=True) 
    
    rand_vert = random.randint(0, num_verts)
    neighbors = getNeighbors(object, rand_vert)

    new_positions = []
    dent_size = min(dent_size, len(neighbors))
    for i in range(dent_size):
        new_pos = findNewPosition(object, neighbors[i], push_dist)
        new_positions.append(new_pos)
    cmds.select(clear = True)
    for i in range(dent_size): # do this after finding all the new positions, so new positions don't throw off calculation of subsequent verts
        cmds.select(object + '.vtx[' + str(neighbors[i]) + ']', add=True)
        pushVertexIn(object, neighbors[i], new_positions[i][0], new_positions[i][1],new_positions[i][2])
    cmds.select(object, replace=True)

def slicePieces(visualize_field, *args):
    if (len(cmds.ls(sl=True)) == 0):
        cmds.error("You must have an object selected.")
    else:
        object = cmds.ls(sl=True)[0]
        print "Object: " + object
        num_verts = cmds.polyEvaluate(object, vertex = True)
        object_pos = cmds.xform(object, query = True, worldSpace = True, translation = True)
        object_scale = cmds.xform(object, query = True,relative=True, scale = True)
        visualize_flag = cmds.checkBox(visualize_field, query = True, value = True)
        
        object_latest = cmds.ls(sl=True)[0]
        object_pos = cmds.xform(object_latest, query = True, worldSpace = True, translation = True)
        object_scale = cmds.xform(object_latest, query = True,relative=True, scale = True)
        bbox = cmds.exactWorldBoundingBox(object_latest)
        min_sc_rad = int(min(bbox[3]-bbox[0], bbox[4]-bbox[1], bbox[5]-bbox[2])/2) # minimum scale radius
        num_edges = cmds.polyEvaluate(object_latest, edge = True)
        
        # get random slice plane position and rotation
        slice_plane_pos = [object_pos[0] + random.randint(0, min_sc_rad), 
            object_pos[1] + random.randint(0, min_sc_rad), 
            object_pos[2] + random.randint(0, min_sc_rad)]
        plane_rotx = random.randint(0,90)
        plane_roty = random.randint(0,90)
        plane_rotz = random.randint(0,90)
        print "Cut plane rotations: " +  str(plane_rotx), str(plane_roty), str(plane_rotz)
        
        if visualize_flag:
            # ---- DEBUGGING: DRAW CUT PLANE ---- #
            cmds.polyPlane(n='plane_visual', w=20, h=20)
            cmds.xform('plane_visual', worldSpace = True, translation = slice_plane_pos, rotation = (90+plane_rotx, plane_roty, plane_rotz))
            # ----------------------------------- #
        
        # slice the mesh
        cmds.polyCut(object_latest,extractFaces=1, pc = slice_plane_pos,  
            constructionHistory=1, rx=plane_rotx,ry=plane_roty, rz=plane_rotz)
        
        new_num_edges = cmds.polyEvaluate(object_latest, edge = True)
        
        # fill the openings of the resulting pieces and separate the mesh 
        cmds.select(object_latest + '.e[' + str(num_edges) + ':' + str(new_num_edges) + ']')
        cmds.polyCloseBorder()
        cmds.polySeparate(object_latest)
        
        pieces = cmds.ls(selection = True)
        cmds.xform(pieces[0], centerPivots = 1) 
        
        for i in xrange(1, len(pieces)): # center pivot for each piece
            cmds.xform(pieces[i], centerPivots = 1)
            piece_pos = cmds.xform(pieces[i], query = True, translation = True, worldSpace = True)

# change param values if a new profile is selected
def assignParams(dent_size_field, dent_depth_field, patch_size_field, noise_amount_field, item):
    if (item != "Custom"):
        print "Using " + item + " Profile..."
        cmds.intField(dent_size_field, edit = True, value=profiles[item][0])
        cmds.floatField(dent_depth_field, edit = True, value=profiles[item][1])
        cmds.intField(patch_size_field, edit = True, value=profiles[item][2])
        cmds.floatField(noise_amount_field, edit = True, value=profiles[item][3])     
    else:
        cmds.intField(dent_size_field, edit = True, value=0)
        cmds.floatField(dent_depth_field, edit = True, value=0)
        cmds.intField(patch_size_field, edit = True, value=0)
        cmds.floatField(noise_amount_field, edit = True, value=0)

def saveProfile(profile_name_field, profile_menu, dent_size_field, dent_depth_field, patch_size_field, noise_amount_field, *args):
    profile_name = cmds.textField(profile_name_field, query=True, text=True)
    cmds.textField(profile_name_field, edit=True, text="")
    if (profile_name == ""):
        cmds.error("Please provide a profile name.")
    else:
        print "Creating " + profile_name + " profile..."
        dent_size = cmds.intField(dent_size_field, query = True, value=True)
        dent_depth = cmds.floatField(dent_depth_field, query = True, value=True)
        patch_size = cmds.intField(patch_size_field, query = True, value=True)
        noise_amount = cmds.floatField(noise_amount_field, query = True, value=True)
        #print dent_size, dent_dpeth, patch_size, noise_amount
        profiles[profile_name] = [dent_size, dent_depth, patch_size, noise_amount]
        cmds.menuItem(label=profile_name, parent = profile_menu)
        
        output = open('/Users/eyzhou/Desktop/profiles.txt', 'a')
        output.write(profile_name + "," + str(dent_size) + "," + str(dent_depth) + "," + str(patch_size) + "," + str(noise_amount) + "\n")
        output.close()

# UI
def createWin():
    winName = "AutoDeteriorationTool"
    versionNum = 0.1
   
    if cmds.window(winName, exists = True):
        cmds.deleteUI(winName)
    
    cmds.window(winName, sizeable=True, titleBar=True, resizeToFitChildren=False, 
    menuBar=True, widthHeight = (450,500), title="Auto Deterioration Tool " + str(versionNum))
    cmds.scrollLayout(horizontalScrollBarThickness=16, verticalScrollBarThickness=16)
    cmds.columnLayout(columnAttach=('left',5), rowSpacing=10, columnWidth=250)
    
    # Start of widgets

    cmds.text(label = "* Be sure to select an object before performing any of the below actions.", width = 500)
    
    # ----- Dent Creator ----- # #PROBLEM WITH MULTIPLE DENTS!!!!!!!!!!!!!!!!!!!!
    cmds.text(label = "------------------------------ Dent Creator -------------------------------", width = 500)
    
    cmds.rowLayout(numberOfColumns = 5, columnWidth5 = (50,75,75,75,75), columnAlign=(1,'center'))
    cmds.text(label = " Num Dents: ", width = 150)
    dent_num_field = cmds.intField(value = 1, editable = True)
    cmds.setParent("..")
    
    cmds.rowLayout(numberOfColumns = 5, columnWidth5 = (50,75,75,75,75), columnAlign=(1,'center'))
    cmds.text(label = " Dent Size: ", width = 150)
    dent_size_field = cmds.intField(value = 0, editable = True)
    cmds.setParent("..")
    
    cmds.rowLayout(numberOfColumns = 5, columnWidth5 = (50,75,75,75,75), columnAlign=(1,'center'))
    cmds.text(label = " Dent Depth: ", width = 150)
    dent_depth_field = cmds.floatField(value = 0, editable = True)
    cmds.setParent("..")
    
    cmds.rowLayout(numberOfColumns = 5, columnWidth5 = (50,75,75,75,75), columnAlign=(1,'center'))
    cmds.button(label = "Generate Dent", width = 150, command = partial(generateDentsWrapper, dent_size_field, dent_depth_field, dent_num_field))
    cmds.setParent("..")
    
    
    # ----- Noise Patch Generation ----- #
    cmds.text(label = "------------------------------ Noise Generator ------------------------------", width = 500)
    
    cmds.rowLayout(numberOfColumns = 5, columnWidth5 = (50,75,75,75,75), columnAlign=(1,'center'))
    cmds.text(label = " Num Noise Patches: ", width = 150)
    num_patches_field = cmds.intField(value = 1, minValue = 0, maxValue = 50, editable = True)
    cmds.setParent("..")
    
    cmds.rowLayout(numberOfColumns = 5, columnWidth5 = (50,75,75,75,75), columnAlign=(1,'center'))
    cmds.text(label = " Patch Size: ", width = 150)
    patch_size_field = cmds.intField(value = 0, minValue = 0, maxValue = 50, editable = True)
    cmds.setParent("..")
    
    cmds.rowLayout(numberOfColumns = 5, columnWidth5 = (50,75,75,75,75), columnAlign=(1,'center'))
    cmds.text(label = " Noise Amount: ", width = 150)
    noise_amount_field = cmds.floatField(value = 0, minValue = 0, maxValue = 50, editable = True)
    cmds.setParent("..")
    
    cmds.button(label = "Generate Noise", width = 150, command = partial(noisePatches, num_patches_field, patch_size_field, noise_amount_field))
    
    
    # ----- Break Off Pieces ----- #
    cmds.text(label = "------------------------------ Mesh Slicer ----------------------------------", width = 500)
    visualize_field = cmds.checkBox( label='Visualize Slice Plane', value = False)
    cmds.button(label = "Slice Mesh", width = 150, command = partial(slicePieces, visualize_field))
    
    # ----- Profile Selector ----- #
    cmds.text(label = "************************************** LOAD A PROFILE ****************************************", width = 500)
    profile_menu = cmds.optionMenu(label='Select Profile', changeCommand=partial(assignParams, dent_size_field, dent_depth_field, patch_size_field, noise_amount_field))
    cmds.menuItem( label='Custom' )
    for profile in profiles:
        cmds.menuItem( label=profile )
    
    cmds.rowLayout(numberOfColumns = 5, columnWidth5 = (50,75,75,75,75), columnAlign=(1,'center'))
    cmds.text(label = " Name of New Profile: ", width = 150)
    profile_name_field = cmds.textField(text = "", width = 150, editable = True)
    cmds.button(label = "Save Profile", width = 150, command = partial(saveProfile, profile_name_field, profile_menu, dent_size_field, dent_depth_field, patch_size_field, noise_amount_field))
    cmds.setParent("..")
    
    cmds.text(label = "--------------------------------------------------------------------------------", width = 500)
    
    cmds.showWindow()

# Read in saved profiles text file
# Profiles saved in following format: NAME -> [dent size, dent depth, patch size, noise amount]
profiles = {}
input = open('/Users/eyzhou/Desktop/profiles.txt', 'r') 
lines = input.readlines() 
for line in lines:
    #print line
    data = line.split('\n')[0]
    data = data.split(',')
    profiles[data[0]] = [int(data[1]), float(data[2]), int(data[3]), float(data[4])]
    
createWin()


