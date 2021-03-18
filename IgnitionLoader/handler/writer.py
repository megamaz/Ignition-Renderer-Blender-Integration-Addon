import bpy
from bpy_extras.io_utils import ExportHelper
from bpy.props import (
    FloatProperty
)
from pathlib import Path



class IgnitionFileWriter(bpy.types.Operator, ExportHelper):
    """Will write the current blend file to a .ignition file"""
    bl_idname = "ignition.writer"
    bl_label = "Save as Ignition File"
    bl_options = {"REGISTER"}

    scaleFactor: FloatProperty(
        name="Scale Factor",
        description="The amount to scale all values",
        default=1.0,
        min=1,
        options={}, # disable the animatable option.
        
    )
    filename_ext = ".ignition"

    filepath = "" # remove undefined variable error
    def execute(self, context):
        
        blendJson = {"materials":[], "lights":[], "meshes":[]}
        
        # RENDERER SETTINGS
        blendJson["Renderer"] = {}
        blendJson["Renderer"]["resolution"] = [bpy.data.scenes[0].render.resolution_x, bpy.data.scenes[0].render.resolution_x]
        blendJson["Renderer"]["maxDepth"] = bpy.data.scenes[0].cycles.max_bounces
        blendJson["Renderer"]["tileWidth"], blendJson["Renderer"]["tileHeight"] = 128, 128 # Blender does not have a setting for tile size

        for link in bpy.data.worlds[0].node_tree.links:
            if link.from_node.type == "TEX_ENVIRONMENT":
                print(Path.absolute(link.from_node.image.filepath))

        print(self.filepath)
        return {"FINISHED"}

