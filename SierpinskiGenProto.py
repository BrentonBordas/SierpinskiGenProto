#--------------------------------------------------------#
# Title: SierpinskiGen Prototype                         #
# Author: Brenton Bordas                                 #
# Contributors:                                          #
#--------------------------------------------------------#
bl_info = {
 "name": "SierpinskiGen Prototype",
 "description": "Creates a Sierpinski based on user input.",
 "author": "Brenton Bordas",
 "version": (0.1, 0),
 "blender": (2, 75, 0),
 "location": "View3D > Add",
 "warning": "Under Experimental Testing",
 "tracker_url": "",
 "support": "TESTING",
 "category": "Object"
}

import bpy,os.path,subprocess,io,sys,csv,re
from bpy.props import FloatVectorProperty, IntProperty

#TODO:
#-tweak parsing some more
#-Introduce multithreading
#-Fix resize attribute in Java

#Useful calls:
#-bpy.context.scene.cursor_location = (0.0, 0.0, 0.0)
#-cursor = scene.cursor_location


#------------------Blender class object and Execute------------------#


class SierpinskiGenerator(bpy.types.Operator):
 """Creates a Sierpinski based on user input"""
 bl_idname = "object.siergen_proto"
 bl_label = "SierpinskiGen Prototype"
 bl_options = {'REGISTER', 'UNDO'}
 
 #Size Property.
 #properties are global variables held by the class they belong to
 size = FloatVectorProperty(
  name="Size",
  default=(0.0, 0.0, 0.0),
  subtype='XYZ',
  description="Resize Values"
 )
 
 #Level Property
 level = IntProperty(
  name="Level",
  default=(0),
  description="Level of Recursion"
 )
 
 #controls how the operator is called, 
 #in this case it forces a window popup with user input options
 def invoke(self, context, event):
  window_manager = context.window_manager
  return window_manager.invoke_props_dialog(self)
  
 def execute(self, context):
  #get path to jar
  jar_path = get_path()
  
  #build property string, encode it for transfer
  props_out = "[a:"+str(self.size[0])+",b:"+str(self.size[1])+",c:"+str(self.size[2])+",level:"+str(self.level)+"]"
  out_string = str(props_out).encode('UTF-8')
  
  #---Depricated Call---#
  #execute jar (File Dump Style)
  #subprocess.call(['java', '-jar', jar_path + '\\SierpinskiGen.jar'], shell=False)
  
  #execute jar, open pipe to it
  process = subprocess.Popen(['java', '-jar', jar_path + '\\SierpinskiGen.jar'], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
  
  #send and get pipe messages
  process.communicate(out_string)
  input = process.communicate()[0]
  input_string = str(input)
  
  #kill the process after it performed it's task
  process.kill()
  
  #get the scene (reduces typing)
  scene = context.scene
  
  # check poll() to avoid exception.
  if bpy.ops.object.mode_set.poll():
   bpy.ops.object.mode_set(mode='EDIT')

  #parse through generated xml file (or Piped Input)
  #d = parse_xml((jar_path + '\\xmlGenFile.xml'))
  d = parse_xml_inputPipe(input_string)
  
  #convert vert and face strings into arrays
  vert_array = eval(d.get('vertice_list'))
  face_array = eval(d.get('face_list'))
  
  #Create the object
  bpy.ops.view3d.snap_cursor_to_center()
  object_data = bpy.data.meshes.new(d.get('object'))
  object_data.from_pydata(vert_array, [], face_array)
  object_data.update()
  
  object = bpy.data.objects.new(d.get('object'), object_data)
  object.data = object_data
  scene.objects.link(object)
  scene.update()
  
  # check poll() to avoid exception.
  if bpy.ops.object.mode_set.poll():
   bpy.ops.object.mode_set(mode='OBJECT')
  
  return {'FINISHED'}


#------------------Custom functions------------------#


#retrieves os dependent path to THIS file
def get_path():
  path = os.path.dirname(os.path.abspath(__file__))
  return path

#---Depricated Function---#
#Used to parse xml file, combines file into one string then calls get_xml_object on it. 
#Then retrieves individual pieces from object.
def parse_xml(xml_file):
 combined_string = ''

 #open file, then combine all lines in file to single string
 with open(xml_file, 'r') as outfile:
  for line in outfile:
   combined_string += line
  combined_string = re.sub(r'\s+', '', combined_string)
  second_combined_string = re.sub(r'objectname', 'object name', combined_string)

  #retrieves object from xml
  obj_attrs = get_xml_object(second_combined_string)
  
 #return all the dictionary elements in attr
  return {'object':obj_attrs.get('object'), 'vertice_list':obj_attrs.get('vertice_list'), 'face_list':obj_attrs.get('face_list')}
  
#Used to parse piped input to Python, combines file into one string then calls get_xml_object on it. 
#Then retrieves indivdual pieces from object.
def parse_xml_inputPipe(pipe_string):
 first_combined_string = ''
 
 first_combined_string = re.sub(r'\s+', '', pipe_string)
 second_combined_string = re.sub(r'\'', '', first_combined_string)
 third_combined_string = re.sub(r'^b<', '<', second_combined_string)
 fourth_combined_string = re.sub(r'objectname', 'object name', third_combined_string)

 #retrieves object from xml
 obj_attrs = get_xml_object(fourth_combined_string)
 
 #return all the dictionary elements in attr
 return {'object':obj_attrs.get('object'), 'vertice_list':obj_attrs.get('vertice_list'), 'face_list':obj_attrs.get('face_list')}

#Used to retrieve objects from xml file
#Currently can only successfully retrieve a single object
def get_xml_object(xml_string):
 obj = re.search('.*<object name="(.*)">.*<vertices>(.*)</vertices>.*<faces>(.*)</faces>.*</object>.*', xml_string)
 return {'object':obj.group(1), 'vertice_list':obj.group(2), 'face_list':obj.group(3)}

 
#------------------Blender registration and menu functions------------------#


def menu_func(self, context):
 self.layout.operator(SierpinskiGenerator.bl_idname)

def register():
 bpy.utils.register_class(SierpinskiGenerator)
 bpy.types.INFO_MT_add.append(menu_func)

def unregister():
 bpy.utils.unregister_class(SierpinskiGenerator)
 bpy.types.INFO_MT_add.remove(menu_func)

if __name__ == "__main__":
 register()
 bpy.ops.object.simple_operator('INVOKE_DEFAULT')