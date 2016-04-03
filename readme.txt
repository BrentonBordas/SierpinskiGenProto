#------------------------------------------------#
# Title: Sierpinski Generator for Blender        #
# Code Authors: Brenton Bordas, Dr. Krish Pillai #
# Contributors:                                  #
#------------------------------------------------#

Preface

This is a module created for Blender that generates a sierpinski triangle via the combined usage
of both a python script and java application.

The purpose of this module was to provide an exercise of standard module creation, Blender
manipulation, and interprocess communication.

This module has only been tested for Blender Version 2.75, and it's functionality is not guaranteed
for any other version.

Installation

1. Install python script (SierpinskiGenProto.py) from within Blender via the File->User Preferences->Addon menu.
 1.a. Click the "Install from file" option located on the bottom of the "Addon" panel and choose the script file
2. Activate the addon within the Addon menu by clicking the check box at the end of the addon's title
3. Manually place the Java Application (SierpinskiGen.java) into the Blender scripts\addons folder, the location of
   which varies from OS to OS. The standard locations are as follows:
 3.a. Windows 7: C:\Users\%username%\AppData\Roaming\Blender Foundation\Blender\%blender version number%\scripts\addons
   Note: The AppData folder is located within the installing user's main directory, but may be hidden by default.
   If this is the case, click the "Organize" drop down menu located at the upper left hand bar and choose
   "Folder and search options". From within this panel (Folder Options) click the "View" tab and navigate
   to the "Hidden files and folders" option and choose the "Show hidden files, folders, and drives" option.
 3.b. Linux: /home/$user/.blender/$blender version number/scripts/addons/m3addon

How to use

If correctly installed, a new option should be available to in the "Add" menu on the lower bar
while one is currently in "Object Mode". The new option is labelled "SierpinskiGen Prototype" and,
if clicked, displays an option menu requesting input.

Input options:
 Size (X,Y,Z): The X,Y, and Z sizes for the full object(Broken, see "Current Issues")
 Level: The number of times the object is subdivided into smaller tetrahedrons
 (A Level above 4 is currently discouraged, see "Current Issues")
 
After giving desired input, click ok and a Sierpinski object will be created. A new, temporary,
menu will popup on the left hand side which will allow one to modify the input values in realtime. 


Current Issues

1. Size input values currently move the object along the X,Y,Z axis instead if resizing object
2. Levels of recursion above 6 currently crashes Blender, with 5 and 6 taking a long delay before generation

