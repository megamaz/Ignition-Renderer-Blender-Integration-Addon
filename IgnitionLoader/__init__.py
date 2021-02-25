import bpy, os, math
from .handler import loader
from .handler import panel

bl_info = {
    "name": "Ignition Loader",
    "blender":(2, 80, 0),
    "category": "Import-Export",
}

classes = [
    loader.IgnitionFileLoader,
    panel.IgnitionPanel
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_object.append(panel.IgnitionPanel.draw)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)