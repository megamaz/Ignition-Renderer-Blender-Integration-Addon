from bpy.types import (
    Panel
)
from . import loader

class IgnitionPanel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Ignition"
    bl_label = "File Handler"

    def draw(self, context):
        layout = self.layout
        layout.operator(loader.IgnitionFileLoader.bl_idname)
    