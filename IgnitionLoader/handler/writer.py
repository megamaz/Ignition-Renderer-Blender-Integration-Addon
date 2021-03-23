import bpy, os, json, random
from bpy_extras.io_utils import ExportHelper


class IgnitionFileWriter(bpy.types.Operator, ExportHelper):
    """Will write the current blend file to a .ignition file"""
    bl_idname = "ignition.writer"
    bl_label = "Save as Ignition File"
    bl_options = {"REGISTER"}

    filename_ext = ".ignition"

    filepath = "" # remove undefined variable error
    def execute(self, context):
        
        folder = '\\'.join(self.filepath.split("\\")[:-1])
        ignitionSavedFileName = self.filepath.split("\\")[-1].split(".")[0]
        blendJson = {"materials":[], "lights":[], "meshes":[]}
        
        # RENDERER SETTINGS
        blendJson["Renderer"] = {}
        blendJson["Renderer"]["resolution"] = [bpy.data.scenes[0].render.resolution_x, bpy.data.scenes[0].render.resolution_y]
        blendJson["Renderer"]["maxDepth"] = bpy.data.scenes[0].cycles.max_bounces
        blendJson["Renderer"]["tileWidth"], blendJson["Renderer"]["tileHeight"] = 128, 128 # Blender does not have a setting for tile size

        for link in bpy.data.worlds[0].node_tree.links:
            if link.from_node.type == "TEX_ENVIRONMENT":
                # copy HDRI
                with open(link.from_node.image.filepath_from_user(), 'rb') as copyBytes:
                    newLoc = f"{folder}\\{ignitionSavedFileName}_assets\\HDRI.{link.from_node.image.filepath.split('.')[-1]}"
                    currentHDRIBytes = copyBytes.read()
                    if not os.path.exists(newLoc):
                        os.mkdir('\\'.join(newLoc.split("\\")[:-1]))
                    open(newLoc, 'wb').write(currentHDRIBytes)
                blendJson["Renderer"]["envMap"] = f"./{ignitionSavedFileName}_assets\\HDRI.{link.from_node.image.filepath.split('.')[-1]}"

        for node in bpy.data.worlds[0].node_tree.nodes:
            if node.type == "BACKGROUND":
                blendJson["Renderer"]["hdriMultiplier"] = node.inputs[1].default_value

        # CAMERA SETTINGS
        blendJson["Camera"] = {}
        blendJson["Camera"]["fov"] = bpy.data.cameras[bpy.data.scenes[0].camera.name].angle
        blendJson["Camera"]["pos"] = [bpy.data.scenes[0].camera.location[0],
                                     -bpy.data.scenes[0].camera.location[2],
                                      bpy.data.scenes[0].camera.location[1]]
        
        # oh boy here we go
        # ok so to get the point at which the camera
        # is looking at, I have to do 5 things;
        # 1. Create new empty
        # 2. Parent empty to camera (without inverse)
        # 3. Move empty -1 on Z axis
        # 4. Unparent empty and keep transform
        # 5. Get empty location, that's the point the camera is loooking at.
        # awfully complicated.

        # step 1
        objName = ' '.join([chr(random.randint(0,255)) for x in range(10)])
        print(objName)
        bpy.ops.object.empty_add(type='PLAIN_AXES') # empty is now selected
        bpy.context.object.name = objName # randomly generated name for later
        # step 2
        bpy.context.object.select_set(False)
        bpy.data.objects[objName].select_set(True)
        bpy.data.scenes[0].camera.select_set(True)

        bpy.ops.object.parent_no_inverse_set() # empty object now is parented to camera
        for obj in bpy.context.selected_objects:
            if obj.name != objName: # that's why we needed a random name
                obj.select_set(False)
        
        # Step 3
        bpy.context.object.location[2] -= 1

        # Step 4
        bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')



        

        # JSON -> IGNITION
        ignitionFile = ""
        for key in blendJson.keys():
            if type(blendJson[key]) == list:
                continue
            ignitionFile += f'{key}\n{{\n'
            for values in blendJson[key]:
                if type(blendJson[key][values]) == list:
                    ignitionFile += f"\t{values} "
                    for c in blendJson[key][values]:
                        ignitionFile += f"{c} "
                    ignitionFile += "\n"
                    continue
                ignitionFile += f"\t{values} {blendJson[key][values]}\n"
            ignitionFile += "}"

        open(self.filepath, 'w').write(ignitionFile)


        return {"FINISHED"}