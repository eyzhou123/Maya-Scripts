# Maya-Scripts
Python scripts to aid with modeling and rigging in Maya

#### 1) Auto Deterioration Script

This script has an interface and allows the user to apply random deterioration to a 3D model. The current types of deterioration are categorized as noise patches, dents, and breaking/cracks. The user is able to alter parameters for these categories and even save them as profiles to easily reuse on similar models. These profiles are saved to a text file and are read in on every use of the tool.
<img src="https://github.com/eyzhou123/Maya-Scripts/blob/master/example_images/deteriorate3.png" alt="Drawing" width="800" height="500"/>
<img src="https://github.com/eyzhou123/Maya-Scripts/blob/master/example_images/deteriorate1.png" alt="Drawing" width="400" height="250"/> <img src="https://github.com/eyzhou123/Maya-Scripts/blob/master/example_images/deteriorate2.png" alt="Drawing" width="400" height="250"/>

#### 2) Basic Zero-Out Script

This was one of my first scripts written in Maya. It simply builds a small interface that lists the objects in the scene, with buttons for zeroing out translate, rotate and scale values if they are not already zeroed out.
<img src="https://github.com/eyzhou123/Maya-Scripts/blob/master/example_images/inspect_scene.png" alt="Drawing" width="600" height="500"/>
#### 3) Circular Tiling Script

This was a small script that was used in my game "Silk and Stone". It was used for arranging objects in a circular pattern, which made modeling pagoda tiles, circular gates etc. very efficient. 
<img src="https://github.com/eyzhou123/Maya-Scripts/blob/master/example_images/tiling_example.png" alt="Drawing" width="800" height="450"/>

#### 4) Landscape Generator Script

This script has an interface and allows the user to first randomly generate terrain from a default plane. Then, the user may select models to use as a database, which the script will pull from when randomly populating the terrain with the models, taking into account the elevation differences. 
<img src="https://github.com/eyzhou123/Maya-Scripts/blob/master/example_images/landscape_generator1.png" alt="Drawing" width="800" height="450"/>
<img src="https://github.com/eyzhou123/Maya-Scripts/blob/master/example_images/landscape_generator2.png" alt="Drawing" width="800" height="450"/>
#### 5) Maya API Script Test

A small exercise with the Maya API to loop through vertices much quicker than with a for loop in Python.

#### 6) Skin Weight Averaging Script

This script was made to fix skinning issues for models that had disconnected pieces (for example, game models that had customizable features). Instead of mirroring skin weights, which would fail if some weights were 0, it averages the weights for smoother results.
<img src="https://github.com/eyzhou123/Maya-Scripts/blob/master/example_images/skinning_before.png" alt="Drawing" width="800" height="450"/>
<img src="https://github.com/eyzhou123/Maya-Scripts/blob/master/example_images/skinning_after.png" alt="Drawing" width="800" height="450"/>

#### 7) Zero Out Control Script

This small script zeros out a control to make a rig cleaner. It is a small task that would have had to be repeated many times while setting up a rig.
