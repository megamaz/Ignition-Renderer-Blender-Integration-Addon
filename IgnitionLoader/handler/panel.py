from bpy.types import (
    Panel,
    Operator
)
import bpy
from . import loader

# testing purposes! This won't be usable in the final code
class IgnitionNodePanelTest(Operator):
    """Test default ignition node"""
    bl_idname = "node.ignition"
    bl_label = "Create Default Ignition Node (Test)"
    bl_options = {'REGISTER'}

    def execute(self, context:bpy.context):
        
        loader.ignitionNode(None if "IgnitionDefault" not in bpy.data.node_groups.keys() else bpy.data.node_groups["IgnitionDefault"])
        
        return {"FINISHED"}
class FileHandlerPanel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Ignition"
    bl_label = "File Handler"

    def draw(self, context):
        layout = self.layout
        layout.operator(loader.IgnitionFileLoader.bl_idname)
    